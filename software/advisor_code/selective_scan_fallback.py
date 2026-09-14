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

import torch
import torch.nn.functional as F


def selective_scan_pytorch(u, delta, A, B, C, D=None, delta_bias=None,
                           delta_softplus=False, chunk=8):
    """Same maths as selective_scan_cuda_core.fwd, ~200x slower, runs anywhere.

    u          (b, d, l)     input sequence
    delta      (b, d, l)     per-step timestep
    A          (d, n)        state matrix, strictly negative
    B, C       (b, g, n, l)  input/output projections, g groups over d channels
    D          (d,)          skip connection, optional
    delta_bias (d,)          optional
    returns    (b, d, l)

    The recurrence is x_t = a_t * x_{t-1} + b_t with a_t = exp(delta_t * A).
    Solving it per chunk gives x_t = exp(s_t)*x_prev + sum_{j<=t} exp(s_t - s_j)*b_j
    where s = cumsum(delta*A). Because A < 0 and delta > 0, every exp(s_t - s_j)
    with j <= t lies in (0, 1] — so the decay matrix can never overflow. That is
    why this is chunked rather than a single cumsum: the naive form needs
    exp(-s_j), which does overflow on long sequences.
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

    # one group serves d//g consecutive channels
    B = B.repeat_interleave(d // g, dim=1)          # (b, d, n, l)
    C = C.repeat_interleave(d // g, dim=1)          # (b, d, n, l)

    A = A.view(1, d, 1, n)
    x = u.new_zeros(b, d, n)                        # carried state
    outs = []

    for start in range(0, l, chunk):
        end = min(start + chunk, l)
        T = end - start

        dt = delta[:, :, start:end]                                  # (b,d,T)
        da = dt.unsqueeze(-1) * A                                    # (b,d,T,n), <= 0
        s = da.cumsum(dim=2).permute(0, 1, 3, 2)                     # (b,d,n,T)

        bu = (dt.unsqueeze(-1)
              * B[:, :, :, start:end].permute(0, 1, 3, 2)
              * u[:, :, start:end].unsqueeze(-1))                    # (b,d,T,n)
        bu = bu.permute(0, 1, 3, 2)                                  # (b,d,n,T)

        # decay[..., t, j] = exp(s_t - s_j), kept only for j <= t
        decay = torch.exp(s.unsqueeze(-1) - s.unsqueeze(-2))         # (b,d,n,T,T)
        decay = torch.tril(decay)

        xs = torch.matmul(decay, bu.unsqueeze(-1)).squeeze(-1)       # (b,d,n,T)
        xs = xs + torch.exp(s) * x.unsqueeze(-1)                     # carry in

        outs.append((xs * C[:, :, :, start:end]).sum(dim=2))         # (b,d,T)
        x = xs[..., -1]

    out = torch.cat(outs, dim=2)                                     # (b,d,l)
    if D is not None:
        out = out + u * D.float().view(1, -1, 1)
    return out.to(dtype_in)


def _self_check():
    """Compare the chunked solver against a plain step-by-step loop."""
    torch.manual_seed(0)
    b, d, l, n, g = 2, 8, 37, 4, 2          # l deliberately not a multiple of chunk
    u = torch.randn(b, d, l)
    delta = torch.rand(b, d, l) + 0.1
    A = -torch.rand(d, n) - 0.1             # must be negative
    B = torch.randn(b, g, n, l)
    C = torch.randn(b, g, n, l)
    D = torch.randn(d)
    delta_bias = torch.randn(d) * 0.1

    got = selective_scan_pytorch(u, delta, A, B, C, D, delta_bias,
                                 delta_softplus=True, chunk=8)

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
    assert err < 1e-4, f"chunked scan disagrees with the naive loop: {err}"
    print(f"self-check OK (max abs error {err:.2e})")


if __name__ == "__main__":
    _self_check()
