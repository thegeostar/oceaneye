"""Pure-PyTorch selective scan for the Mamba (VSSM) layers.

Computes the same result as the compiled `selective_scan_cuda_core.fwd` kernel with plain
PyTorch operations, so the model runs without building a CUDA extension. Forward pass only.

    python selective_scan_fallback.py   # compare against a step-by-step reference
"""
import os

import torch
import torch.nn.functional as F

# Memory budget for the scan state of one block of channels. Lower it to reduce peak VRAM.
_BLOCK_BYTES = int(os.environ.get("OCEANEYE_SCAN_BLOCK_BYTES", 192 << 20))

# Sequence positions per chunk in the two-level scan.
_CHUNK = int(os.environ.get("OCEANEYE_SCAN_CHUNK", 16))


def _scan_(a, h):
    """In-place inclusive scan of  h_t = a_t * h_{t-1} + h_t  along the last axis.

    Hillis-Steele over the associative pair (a, h), whose composition is
        (a1, h1) then (a2, h2)  ==  (a1*a2,  a2*h1 + h2)
    so it takes ceil(log2(L)) steps instead of L. Unlike a closed-form cumsum of
    exp(-s), it never exponentiates a growing sum, so it cannot overflow float32.
    """
    k, l = 1, a.shape[-1]
    while k < l:
        a_prev = a[..., :-k].clone()
        h_prev = h[..., :-k].clone()
        h[..., k:].addcmul_(a[..., k:], h_prev)   # must fold h before a is changed
        a[..., k:].mul_(a_prev)
        k *= 2


def _chunked_scan(a, h):
    """Two-level version of _scan_ that makes fewer passes over the full state.

    Scans inside every chunk of _CHUNK positions at once, then scans the per-chunk
    carries (a tensor _CHUNK times smaller) and folds each carry back into its chunk.
    A flat scan of a long sequence is memory-bandwidth bound; this keeps the number
    of full-size passes small. Returns the scanned h; `a` is consumed.
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

    # Now a[..., c, t] is the decay from the start of chunk c to t, and h[..., c, t] is
    # the chunk's result from a zero start. Chunk end states follow the same recurrence
    # one level up: X_c = a[c, -1] * X_{c-1} + h[c, -1].
    ac = a[..., -1].clone()
    hc = h[..., -1].clone()
    _scan_(ac, hc)                          # hc[..., c] is now X_c

    carry = F.pad(hc[..., :-1], (1, 0), value=0.0)   # chunk c starts from X_{c-1}
    h.addcmul_(a, carry.unsqueeze(-1))

    h = h.reshape(*lead, -1)
    return h[..., :l] if pad else h


def selective_scan_pytorch(u, delta, A, B, C, D=None, delta_bias=None,
                           delta_softplus=False):
    """Drop-in replacement for selective_scan_cuda_core.fwd.

    u          (b, d, l)     input sequence
    delta      (b, d, l)     per-step timestep
    A          (d, n)        state matrix, strictly negative
    B, C       (b, g, n, l)  input/output projections, g groups over d channels
    D          (d,)          skip connection, optional
    delta_bias (d,)          optional
    returns    (b, d, l)

    The recurrence is x_t = a_t * x_{t-1} + b_t with a_t = exp(delta_t * A). Since
    A < 0 and delta > 0, every a_t lies in (0, 1], so products of them stay bounded.
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

    # Split channels into (group, channel) so B and C broadcast over their group
    # instead of being copied to every channel.
    u = u.view(b, g, dg, l)
    delta = delta.view(b, g, dg, l)
    A = A.view(g, dg, n)
    B = B.view(b, g, 1, n, l)
    C = C.view(b, g, 1, n, l)

    # Process channels in blocks so each block's (b, g, c, n, l) state fits _BLOCK_BYTES.
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
