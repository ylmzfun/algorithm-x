"""Activation functions: forward and backward (gradient) implementations.

Each function pair:
- forward:  computes activation given input x
- backward: computes gradient given the _output_ of the forward pass (for efficiency)
"""

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Sigmoid
# ---------------------------------------------------------------------------
def sigmoid(x: np.ndarray) -> np.ndarray:
    """Sigmoid activation: σ(x) = 1 / (1 + exp(-x)).

    Args:
        x: Input array of any shape.

    Returns:
        Output with values in (0, 1), same shape as x.
    """
    return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))


def sigmoid_grad(y: np.ndarray) -> np.ndarray:
    """Gradient of sigmoid given its output y: σ'(x) = y * (1 - y).

    Args:
        y: Sigmoid output (result of sigmoid(x)).

    Returns:
        Gradient array, same shape as y.
    """
    return y * (1.0 - y)


# ---------------------------------------------------------------------------
# Tanh
# ---------------------------------------------------------------------------
def tanh(x: np.ndarray) -> np.ndarray:
    """Hyperbolic tangent activation: tanh(x) = (exp(x)-exp(-x)) / (exp(x)+exp(-x)).

    Args:
        x: Input array of any shape.

    Returns:
        Output with values in (-1, 1), same shape as x.
    """
    return np.tanh(x)


def tanh_grad(y: np.ndarray) -> np.ndarray:
    """Gradient of tanh given its output y: tanh'(x) = 1 - y^2.

    Args:
        y: Tanh output (result of tanh(x)).

    Returns:
        Gradient array, same shape as y.
    """
    return 1.0 - y * y


# ---------------------------------------------------------------------------
# ReLU
# ---------------------------------------------------------------------------
def relu(x: np.ndarray) -> np.ndarray:
    """Rectified Linear Unit: ReLU(x) = max(0, x).

    Args:
        x: Input array of any shape.

    Returns:
        Output, same shape as x.
    """
    return np.maximum(0.0, x)


def relu_grad(y: np.ndarray) -> np.ndarray:
    """Gradient of ReLU given its output y: 1 if y > 0, else 0.

    Args:
        y: ReLU output (result of relu(x)).

    Returns:
        Gradient array, same shape as y.
    """
    return (y > 0).astype(float)


# ---------------------------------------------------------------------------
# Leaky ReLU
# ---------------------------------------------------------------------------
def leaky_relu(x: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    """Leaky ReLU: f(x) = x if x > 0, else alpha * x.

    Args:
        x: Input array of any shape.
        alpha: Negative slope coefficient (default 0.01).

    Returns:
        Output, same shape as x.
    """
    return np.where(x > 0, x, alpha * x)


def leaky_relu_grad(y: np.ndarray, x_cache: np.ndarray, alpha: float = 0.01) -> np.ndarray:
    """Gradient of Leaky ReLU: 1 if x > 0, else alpha.

    Note: unlike other grad functions, this requires the original input x_cache
    since the output y alone is insufficient to determine the gradient.

    Args:
        y: Leaky ReLU output (unused; kept for API consistency).
        x_cache: Original input x to leaky_relu.
        alpha: Negative slope coefficient.

    Returns:
        Gradient array, same shape as x_cache.
    """
    return np.where(x_cache > 0, 1.0, alpha)


# ---------------------------------------------------------------------------
# ELU
# ---------------------------------------------------------------------------
def elu(x: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    """Exponential Linear Unit: f(x) = x if x > 0, else alpha*(exp(x) - 1).

    Args:
        x: Input array of any shape.
        alpha: Scale for negative region (default 1.0).

    Returns:
        Output, same shape as x.
    """
    return np.where(x > 0, x, alpha * (np.exp(np.clip(x, -500, 500)) - 1.0))


def elu_grad(y: np.ndarray, x_cache: np.ndarray, alpha: float = 1.0) -> np.ndarray:
    """Gradient of ELU: 1 if x > 0, else y + alpha.

    Note: requires original input x_cache because output alone is insufficient.

    Args:
        y: ELU output.
        x_cache: Original input x to elu.
        alpha: Scale for negative region.

    Returns:
        Gradient array, same shape as x_cache.
    """
    return np.where(x_cache > 0, 1.0, y + alpha)


# ---------------------------------------------------------------------------
# Swish (SiLU)
# ---------------------------------------------------------------------------
def swish(x: np.ndarray, beta: float = 1.0) -> np.ndarray:
    """Swish activation: f(x) = x * sigmoid(beta * x).

    Args:
        x: Input array of any shape.
        beta: Scaling parameter (default 1.0, making it SiLU).

    Returns:
        Output, same shape as x.
    """
    sx = sigmoid(beta * x)
    return x * sx


def swish_grad(y: np.ndarray, x_cache: np.ndarray, beta: float = 1.0) -> np.ndarray:
    """Gradient of Swish: f'(x) = f(x) + sigmoid(beta*x) * (1 - f(x)).

    Args:
        y: Swish output (unused; kept for API consistency).
        x_cache: Original input x to swish.
        beta: Scaling parameter.

    Returns:
        Gradient array, same shape as x_cache.
    """
    sx = sigmoid(beta * x_cache)
    sw = x_cache * sx
    # f'(x) = sw + sigmoid(beta*x) * beta * x_cache * (1 - sigmoid(beta*x)) via chain rule
    # Simplified: f'(x) = sw / x_cache * (1 + beta * x_cache * (1 - sw / x_cache))
    # Better: f'(x) = sigmoid(beta*x) + beta * x_cache * sigmoid(beta*x) * (1 - sigmoid(beta*x))
    # = sx * (1 + beta * x_cache * (1 - sx))
    return sx * (1.0 + beta * x_cache * (1.0 - sx))


# ---------------------------------------------------------------------------
# Softmax
# ---------------------------------------------------------------------------
def softmax(x: np.ndarray, axis: int = -1) -> np.ndarray:
    """Softmax activation: softmax(x)_i = exp(x_i) / sum_j(exp(x_j)).

    Numerically stable via subtracting max.

    Args:
        x: Input array.
        axis: Axis along which to compute softmax.

    Returns:
        Softmax probabilities, same shape as x.
    """
    x_stable = x - np.max(x, axis=axis, keepdims=True)
    exps = np.exp(np.clip(x_stable, -500, 500))
    return exps / np.sum(exps, axis=axis, keepdims=True)


def softmax_grad(y: np.ndarray) -> np.ndarray:
    """Jacobian of softmax: for softmax output y, d(y_i)/d(x_j) = y_i*(delta_ij - y_j).

    This returns the full Jacobian for a single vector. For batched input,
    computes Jacobians per row.

    Args:
        y: Softmax output of shape (..., d).

    Returns:
        Jacobian of shape (..., d, d).
    """
    # For a vector y of shape (d,):
    # J[i,j] = y_i * (delta_ij - y_j)
    # = diag(y) - y y^T
    shape = y.shape
    d = shape[-1]
    y_flat = y.reshape(-1, d)
    n = y_flat.shape[0]

    # Jacobian per sample: (n, d, d)
    J = np.zeros((n, d, d))
    for i in range(n):
        yi = y_flat[i]
        J[i] = np.diag(yi) - np.outer(yi, yi)
    return J.reshape(shape + (d,))


# ---------------------------------------------------------------------------
# GELU
# ---------------------------------------------------------------------------
def gelu(x: np.ndarray) -> np.ndarray:
    """Gaussian Error Linear Unit: GELU(x) = x * Φ(x)
    where Φ is the standard normal CDF.

    Approximation: 0.5 * x * (1 + tanh(sqrt(2/pi) * (x + 0.044715 * x^3)))

    Args:
        x: Input array of any shape.

    Returns:
        Output, same shape as x.
    """
    # Use the tanh approximation (accurate and fast)
    sqrt_2_over_pi = np.sqrt(2.0 / np.pi)
    inner = sqrt_2_over_pi * (x + 0.044715 * x ** 3)
    return 0.5 * x * (1.0 + np.tanh(inner))


def gelu_grad(y: np.ndarray, x_cache: np.ndarray) -> np.ndarray:
    """Gradient of GELU (tanh approximation).

    Args:
        y: GELU output (unused).
        x_cache: Original input x to gelu.

    Returns:
        Gradient array, same shape as x_cache.
    """
    sqrt_2_over_pi = np.sqrt(2.0 / np.pi)
    c = 0.044715
    x3 = x_cache ** 3
    inner = sqrt_2_over_pi * (x_cache + c * x3)
    tanh_inner = np.tanh(inner)
    sech2 = 1.0 - tanh_inner ** 2
    # d/dx of inner: sqrt(2/pi) * (1 + 3*c*x^2)
    dinner_dx = sqrt_2_over_pi * (1.0 + 3.0 * c * x_cache ** 2)
    # d/dx of 0.5*x*(1+tanh): 0.5*(1+tanh) + 0.5*x*sech2*dinner_dx
    return 0.5 * (1.0 + tanh_inner) + 0.5 * x_cache * sech2 * dinner_dx


# ---------------------------------------------------------------------------
# Numerical gradient checking utility
# ---------------------------------------------------------------------------
def numerical_gradient(
    fn: callable,
    x: np.ndarray,
    eps: float = 1e-5,
) -> np.ndarray:
    """Compute numerical gradient of fn at x using central finite differences.

    Args:
        fn: Function to differentiate, maps (d,) -> scalar or array.
        x: Point at which to evaluate gradient, shape (d,).
        eps: Step size for finite differences.

    Returns:
        Numerical gradient, same shape as x.
    """
    grad = np.zeros_like(x, dtype=float)
    for idx in np.ndindex(x.shape):
        orig = x[idx]
        x[idx] = orig + eps
        fp = fn(x)
        x[idx] = orig - eps
        fm = fn(x)
        x[idx] = orig
        grad[idx] = (fp - fm) / (2 * eps)
    return grad


def check_gradient(
    fn_forward: callable,
    fn_backward: callable,
    x: np.ndarray,
    eps: float = 1e-5,
    tol: float = 1e-4,
    name: str = "activation",
) -> bool:
    """Check analytical gradient against numerical gradient.

    Args:
        fn_forward: Forward function.
        fn_backward: Backward (gradient) function. Takes forward output as argument.
        x: Test input.
        eps: Finite difference step.
        tol: Relative error tolerance.
        name: Function name for reporting.

    Returns:
        True if gradient check passes.
    """
    x_test = x.copy().astype(float)
    y = fn_forward(x_test)

    # Wrap forward for numerical gradient (sum to get scalar)
    def fn_scalar(x_arr: np.ndarray) -> float:
        return float(np.sum(fn_forward(x_arr.reshape(x.shape))))

    num_grad = numerical_gradient(fn_scalar, x_test.flatten(), eps).reshape(x.shape)

    # Analytical gradient: for softmax, grad is Jacobian
    if fn_backward == softmax_grad:
        # softmax_grad returns Jacobian; d(sum(y))/dx_j = sum_i J[i,j]
        J = fn_backward(y)
        if J.ndim == 3:
            ana_grad = J.sum(axis=1)  # sum over output dim
        else:
            ana_grad = J.sum(axis=0)
    elif fn_backward in (leaky_relu_grad, elu_grad, swish_grad, gelu_grad):
        ana_grad = fn_backward(y, x_test)
    else:
        ana_grad = fn_backward(y)

    max_err = np.max(np.abs(num_grad - ana_grad)) / (np.max(np.abs(num_grad)) + 1e-10)
    if max_err < tol:
        print(f"  PASS: {name} gradient check, max rel error = {max_err:.2e}")
        return True
    else:
        print(f"  FAIL: {name} gradient check, max rel error = {max_err:.2e}")
        return False


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    np.random.seed(42)
    x_test = np.random.randn(5) * 2.0  # 5 random values for scalar tests
    x_2d = np.random.randn(3, 4) * 2.0  # 2D for batched tests

    print("Testing activation functions...")

    # --- Forward value tests ---
    # Sigmoid
    y_sig = sigmoid(x_test)
    assert np.all((y_sig > 0) & (y_sig < 1)), "Sigmoid range violated"
    assert np.isclose(sigmoid(np.array([0.0])), 0.5), "Sigmoid(0) != 0.5"
    print("  PASS: sigmoid forward")

    # Tanh
    y_tanh = tanh(x_test)
    assert np.all((y_tanh > -1) & (y_tanh < 1)), "Tanh range violated"
    assert np.isclose(tanh(np.array([0.0])), 0.0), "Tanh(0) != 0"
    print("  PASS: tanh forward")

    # ReLU
    y_relu = relu(x_test)
    assert np.all(y_relu >= 0), "ReLU has negative values"
    print("  PASS: relu forward")

    # LeakyReLU
    y_lrelu = leaky_relu(x_test, alpha=0.01)
    neg_vals = x_test < 0
    assert np.allclose(y_lrelu[neg_vals], 0.01 * x_test[neg_vals]), "LeakyReLU negative slope wrong"
    print("  PASS: leaky_relu forward")

    # ELU
    y_elu = elu(x_test, alpha=1.0)
    assert np.all(y_elu > -1.0), "ELU range violated"
    print("  PASS: elu forward")

    # Swish
    y_swish = swish(x_test)
    assert y_swish.shape == x_test.shape
    print("  PASS: swish forward")

    # Softmax
    y_sm = softmax(x_2d, axis=-1)
    assert np.allclose(y_sm.sum(axis=-1), 1.0), "Softmax rows don't sum to 1"
    assert np.all((y_sm >= 0) & (y_sm <= 1)), "Softmax values out of range"
    print("  PASS: softmax forward")

    # GELU
    y_gelu = gelu(x_test)
    assert y_gelu.shape == x_test.shape
    print("  PASS: gelu forward")

    # --- Gradient tests (on a single scalar for simplicity) ---
    x_grad = np.array([0.5, -0.3, 1.2, -0.8, 0.1])  # Avoid x=0 where ReLU subgradient is ambiguous

    print("\nGradient checks:")
    all_pass = True

    # Sigmoid grad
    y_s = sigmoid(x_grad)
    a_s = sigmoid_grad(y_s)
    def f_s(x): return np.sum(sigmoid(x))
    ng_s = numerical_gradient(f_s, x_grad.copy())
    all_pass &= np.max(np.abs(a_s - ng_s)) < 1e-4
    print(f"  {'PASS' if all_pass else 'FAIL'}: sigmoid gradient")

    # Tanh grad
    y_t = tanh(x_grad)
    a_t = tanh_grad(y_t)
    def f_t(x): return np.sum(tanh(x))
    ng_t = numerical_gradient(f_t, x_grad.copy())
    ok = np.max(np.abs(a_t - ng_t)) < 1e-4
    print(f"  {'PASS' if ok else 'FAIL'}: tanh gradient")
    all_pass &= ok

    # ReLU grad
    y_r = relu(x_grad)
    a_r = relu_grad(y_r)
    def f_r(x): return np.sum(relu(x))
    ng_r = numerical_gradient(f_r, x_grad.copy())
    ok = np.max(np.abs(a_r - ng_r)) < 1e-4
    print(f"  {'PASS' if ok else 'FAIL'}: relu gradient")
    all_pass &= ok

    # LeakyReLU grad
    a_lr = leaky_relu_grad(y_lrelu, x_grad)
    def f_lr(x): return np.sum(leaky_relu(x))
    ng_lr = numerical_gradient(f_lr, x_grad.copy())
    ok = np.max(np.abs(a_lr - ng_lr)) < 1e-4
    print(f"  {'PASS' if ok else 'FAIL'}: leaky_relu gradient")
    all_pass &= ok

    # ELU grad
    y_e = elu(x_grad)
    a_e = elu_grad(y_e, x_grad)
    def f_e(x): return np.sum(elu(x))
    ng_e = numerical_gradient(f_e, x_grad.copy())
    ok = np.max(np.abs(a_e - ng_e)) < 1e-4
    print(f"  {'PASS' if ok else 'FAIL'}: elu gradient")
    all_pass &= ok

    # Softmax gradient (check d(sum(y))/dx_j = 0 for each j)
    y_sm2 = softmax(x_grad, axis=-1)
    J_sm = softmax_grad(y_sm2)
    # For softmax, sum over output gives zero gradient for each input
    grad_sum = J_sm.sum(axis=1)  # should be near 0
    ok = np.all(np.abs(grad_sum) < 1e-10)
    print(f"  {'PASS' if ok else 'FAIL'}: softmax gradient (d(sum)/dx = 0)")
    all_pass &= ok

    # GELU grad
    a_g = gelu_grad(y_gelu, x_grad)
    def f_g(x): return np.sum(gelu(x))
    ng_g = numerical_gradient(f_g, x_grad.copy())
    ok = np.max(np.abs(a_g - ng_g)) < 1e-4
    print(f"  {'PASS' if ok else 'FAIL'}: gelu gradient")
    all_pass &= ok

    # --- 2D Softmax ---
    y_sm3 = softmax(x_2d, axis=-1)
    assert y_sm3.shape == (3, 4)
    assert np.allclose(y_sm3.sum(axis=-1), 1.0)
    print("  PASS: softmax 2D")

    # --- Visualization (optional) ---
    try:
        import matplotlib.pyplot as plt

        x_vis = np.linspace(-3, 3, 200)
        acts = {
            "Sigmoid": (sigmoid(x_vis), sigmoid_grad(sigmoid(x_vis))),
            "Tanh": (tanh(x_vis), tanh_grad(tanh(x_vis))),
            "ReLU": (relu(x_vis), relu_grad(relu(x_vis))),
            "LeakyReLU": (leaky_relu(x_vis), leaky_relu_grad(leaky_relu(x_vis), x_vis)),
            "ELU": (elu(x_vis), elu_grad(elu(x_vis), x_vis)),
            "Swish": (swish(x_vis), swish_grad(swish(x_vis), x_vis)),
            "GELU": (gelu(x_vis), gelu_grad(gelu(x_vis), x_vis)),
        }

        fig, axes = plt.subplots(2, 4, figsize=(16, 8))
        axes = axes.flatten()
        for ax, (name, (y_act, y_grad)) in zip(axes, acts.items()):
            ax.plot(x_vis, y_act, label="f(x)", linewidth=2)
            ax.plot(x_vis, y_grad, label="f'(x)", linewidth=2, linestyle="--")
            ax.set_title(name)
            ax.legend()
            ax.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("/tmp/activation_functions.png", dpi=100)
        print("  PASS: visualization saved to /tmp/activation_functions.png")
        plt.close()
    except ImportError:
        print("  SKIP: matplotlib not available for visualization")

    print(f"\n{'All tests passed!' if all_pass else 'Some tests FAILED!'}")
