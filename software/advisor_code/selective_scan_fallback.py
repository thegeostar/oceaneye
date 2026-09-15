# OceanEye: pure-PyTorch replacement for `selective_scan_cuda_core.fwd`.
#
# Why this file exists: Prof. Wang shipped the selective-scan operator as prebuilt
# .so files compiled against torch 2.2 + CUDA 11. This laptop has an RTX 5060
# (sm_120), which CUDA 11 cannot drive at all, so torch must be >= 2.7 + CUDA 12.8 —
# and all 39 libtorch symbols the .so needs were removed from torch's C++ ABI in
# between. Rebuilding needs nvcc from the CUDA 12.8 toolkit (~3 GB); the pip
# `nvidia-cuda-nvcc-cu12` wheel ships only ptxas, and Ubuntu's apt toolkit is 12.0,
# which predates sm_120. So the operator is reimplemented here in plain PyTorch.
#
# Inference only. Backward is not implemented — we never retrain.

import os

import torch
import torch.nn.functional as F

# How many channels are held in flight at once. 192 MB -> 1.57 GB peak for the
# whole model, measured by bench_scan.py; raising it does not get any faster,
# it only eats VRAM. Lower it if something else is using the GPU.
_BLOCK_BYTES = int(os.environ.get("OCEANEYE_SCAN_BLOCK_BYTES", 192 << 20))

# Sequence positions scanned together at the inner level. bench_scan.py measures
# a shallow optimum at 8-16 and clear degradation either side: below 8 the carry
# scan gets too long, above 16 the wide passes cost more than the carry saves.
_CHUNK = int(os.environ.get("OCEANEYE_SCAN_CHUNK", 16))


def _scan_(a, h):
    """In-place inclusive scan of  h_t = a_t * h_{t-1} + h_t  along the last axis.

    Hillis-Steele over the associative pair (a, h), whose composition is
        (a1, h1) then (a2, h2)  ==  (a1*a2,  a2*h1 + h2)
    so after a step at offset k the pair at t maps h_{t-2k} to h_t. That takes
    ceil(log2(L)) steps instead of L.

    It also never exponentiates a positive number. The tempting closed form,
    x_t = exp(s_t) * cumsum(exp(-s_j) * b_j) with s = cumsum(delta*A), is one
    fused cumsum and no loop at all — but it is unusable here, not merely risky:
    the running |s| in this model reaches 113 within 8 steps, and float32 exp()
    overflows at 88.7. Measured, not assumed; see the note in HOW_TO_RUN.md.
    """
    k, l = 1, a.shape[-1]
    while k < l:
        a_prev = a[..., :-k].clone()
        h_prev = h[..., :-k].clone()
        h[..., k:].addcmul_(a[..., k:], h_prev)   # must fold h before a is changed
        a[..., k:].mul_(a_prev)
        k *= 2


def _chunked_scan(a, h):
    """Same scan as _scan_, but structured so the wide passes are few.

    Running _scan_ straight down a 15360-long sequence needs log2(L) = 14 passes
    over the whole (b, d, n, l) state — 0.75 GB per tensor here — and the card
    has ~250 GB/s. Measured: 438 ms for one such call, i.e. no faster than the
    Python loop it replaced. It stopped being launch-bound and became
    bandwidth-bound instead.

    So scan in two levels. Cut the sequence into chunks of _CHUNK, scan inside
    every chunk at once (log2(_CHUNK) wide passes), then scan only the per-chunk
    carries — a tensor _CHUNK times smaller — and fold each chunk's incoming
    carry back in with one more pass. Wide passes drop from 14 to about 4.

    Returns the scanned h; `a` is consumed.
    """
    l = a.shape[-1]
    pad = -l % _CHUNK
    if pad:
        a = F.pad(a, (0, pad), value=1.0)   # identity: decay 1, input 0, so the
        h = F.pad(h, (0, pad), value=0.0)   # tail carries state through untouched
    lead = a.shape[:-1]

    a = a.view(*lead, -1, _CHUNK)           # (..., nchunk, _CHUNK)
    h = h.view(*lead, -1, _CHUNK)
    _scan_(a, h)                            # every chunk, independently, at once

    # After that pass a[..., c, t] is the decay from the start of chunk c to t,
    # and h[..., c, t] is that chunk's result assuming it started from zero. The
    # true state at the end of chunk c obeys X_c = a[c,-1] * X_{c-1} + h[c,-1],
    # which is the same recurrence one level up and _CHUNK times shorter.
    ac = a[..., -1].clone()
    hc = h[..., -1].clone()
    _scan_(ac, hc)                          # hc[..., c] is now X_c

    carry = F.pad(hc[..., :-1], (1, 0), value=0.0)   # chunk c starts from X_{c-1}
    h.addcmul_(a, carry.unsqueeze(-1))

    h = h.reshape(*lead, -1)
    return h[..., :l] if pad else h


def selective_scan_pytorch(u, delta, A, B, C, D=None, delta_bias=None,
                           delta_softplus=False):
    """Same maths as selective_scan_cuda_core.fwd, runs anywhere.

    u          (b, d, l)     input sequence
    delta      (b, d, l)     per-step timestep
    A          (d, n)        state matrix, strictly negative
    B, C       (b, g, n, l)  input/output projections, g groups over d channels
    D          (d,)          skip connection, optional
    delta_bias (d,)          optional
    returns    (b, d, l)

    The recurrence is x_t = a_t * x_{t-1} + b_t with a_t = exp(delta_t * A).
    Because A < 0 and delta > 0 every a_t lies in (0, 1], so folding them can
    only decay towards zero — it cannot blow up.
    """
    dtype_in = u.dtype
    u, delta = u.float(), delta.float()
    A, B, C = A.float(), B.float(), C.float()

    if delta_bias is not None:
        delta = delta + delta_bias.float().view(1, -1, 1)
    if delta_softplus:
        delta = F.softplus(delta)

    b, d, l = u.shape
    n = A.shape[1]
    g = B.shape[1]
    assert d % g == 0, f"channels {d} not divisible by groups {g}"
    dg = d // g

    # Split the channel axis into (group, channel-within-group) so B and C
    # broadcast over their group. The obvious repeat_interleave to (b, d, n, l)
    # costs 755 MB per tensor on the longest sequence here, to store 16 MB of
    # distinct values.
    u = u.view(b, g, dg, l)
    delta = delta.view(b, g, dg, l)
    A = A.view(g, dg, n)
    B = B.view(b, g, 1, n, l)
    C = C.view(b, g, 1, n, l)

    # Walk the channels in blocks so one block's state tensor stays near
    # _BLOCK_BYTES. The state is (b, g, c, n, l) — n times bigger than the
    # input, which is what makes the long sequences expensive.
    per_channel = b * g * n * l * 4
    step = max(1, min(dg, _BLOCK_BYTES // max(per_channel, 1)))

    out = u.new_empty(b, g, dg, l)
    for i in range(0, dg, step):
        j = min(i + step, dg)
        dt = delta[:, :, i:j].unsqueeze(3)                        # (b,g,c,1,l)
        a = torch.exp(dt * A[:, i:j].unsqueeze(0).unsqueeze(-1))  # (b,g,c,n,l)
        h = dt * B * u[:, :, i:j].unsqueeze(3)                    # (b,g,c,n,l)
        h = _chunked_scan(a, h)
        out[:, :, i:j] = (h * C).sum(dim=3)
        del a, h

    out = out.view(b, d, l)
    if D is not None:
        out = out + u.view(b, d, l) * D.float().view(1, -1, 1)
    return out.to(dtype_in)


def _self_check():
    """Compare the parallel scan against a plain step-by-step loop."""
    torch.manual_seed(0)
    # l deliberately not a power of two, g > 1 so the broadcast is exercised
    b, d, l, n, g = 2, 12, 37, 4, 3
    u = torch.randn(b, d, l)
    delta = torch.rand(b, d, l) + 0.1
    A = -torch.rand(d, n) - 0.1             # must be negative
    B = torch.randn(b, g, n, l)
    C = torch.randn(b, g, n, l)
    D = torch.randn(d)
    delta_bias = torch.randn(d) * 0.1

    got = selective_scan_pytorch(u, delta, A, B, C, D, delta_bias,
                                 delta_softplus=True)

    # naive reference: literal one-step-at-a-time recurrence
    dl = F.softplus(delta + delta_bias.view(1, -1, 1))
    Bx = B.repeat_interleave(d // g, dim=1)
    Cx = C.repeat_interleave(d // g, dim=1)
    x = torch.zeros(b, d, n)
    ref = torch.zeros(b, d, l)
    for t in range(l):
        a = torch.exp(dl[:, :, t].unsqueeze(-1) * A.unsqueeze(0))
        x = a * x + dl[:, :, t].unsqueeze(-1) * Bx[:, :, :, t] * u[:, :, t].unsqueeze(-1)
        ref[:, :, t] = (x * Cx[:, :, :, t]).sum(-1)
    ref = ref + u * D.view(1, -1, 1)

    err = (got - ref).abs().max().item()
    assert err < 1e-4, f"parallel scan disagrees with the naive loop: {err}"

    # and again with the channel blocking forced on, so that path is covered too
    global _BLOCK_BYTES
    saved, _BLOCK_BYTES = _BLOCK_BYTES, 1
    blocked = selective_scan_pytorch(u, delta, A, B, C, D, delta_bias,
                                     delta_softplus=True)
    _BLOCK_BYTES = saved
    berr = (blocked - ref).abs().max().item()
    assert berr < 1e-4, f"blocked path disagrees with the naive loop: {berr}"

    print(f"self-check OK (max abs error {err:.2e}, blocked {berr:.2e})")


if __name__ == "__main__":
    _self_check()
