"""
Gradient-Based Optimization Methods for ML/AI Foundations.

Implements classic and modern gradient methods from scratch:
- Vanilla Gradient Descent
- Momentum (heavy ball)
- Nesterov Accelerated Gradient (NAG)
- AdaGrad
- RMSProp
- Adam (Adaptive Moment Estimation)

All tested on simple convex functions with convergence plots.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Callable, Tuple, List, Dict, Optional


# ============================================================
# Test Functions (Convex)
# ============================================================

def convex_quadratic(x: NDArray[np.float64]) -> float:
    """Strongly convex quadratic: f(x, y) = x² + 10y².

    Condition number κ = 10.
    Minimum: f(0, 0) = 0.
    """
    return x[0]**2 + 10.0 * x[1]**2


def convex_quadratic_grad(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Gradient of convex quadratic."""
    return np.array([2.0 * x[0], 20.0 * x[1]], dtype=np.float64)


def convex_bowl(x: NDArray[np.float64]) -> float:
    """Shifted convex quadratic: f(x) = (x₁-3)² + (x₂+2)².

    Minimum at (3, -2), f = 0.
    """
    return (x[0] - 3.0)**2 + (x[1] + 2.0)**2


def convex_bowl_grad(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Gradient of convex bowl."""
    return np.array([2.0 * (x[0] - 3.0), 2.0 * (x[1] + 2.0)], dtype=np.float64)


# ============================================================
# Optimizers
# ============================================================

class SGD:
    """Vanilla Stochastic / Batch Gradient Descent.

    Update: x_{t+1} = x_t - η * g_t
    where g_t is the gradient at x_t.
    """

    def __init__(self, learning_rate: float = 0.01):
        self.lr = learning_rate

    def update(
        self,
        x: NDArray[np.float64],
        grad: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        """Single SGD update step.

        Args:
            x: Current parameter vector.
            grad: Gradient at x.

        Returns:
            Updated parameter vector.
        """
        return x - self.lr * grad

    def reset(self) -> None:
        pass

    def name(self) -> str:
        return "SGD"


class Momentum:
    """Gradient Descent with Momentum (heavy ball method).

    v_t = β * v_{t-1} - η * g_t
    x_t = x_{t-1} + v_t

    where β is the momentum coefficient (typically 0.9).

    Momentum smooths the update direction by accumulating past gradients,
    damping oscillations and accelerating in consistent directions.
    """

    def __init__(self, learning_rate: float = 0.01, beta: float = 0.9):
        self.lr = learning_rate
        self.beta = beta
        self.v: Optional[NDArray[np.float64]] = None

    def update(
        self,
        x: NDArray[np.float64],
        grad: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        if self.v is None:
            self.v = np.zeros_like(x)
        self.v = self.beta * self.v - self.lr * grad
        return x + self.v

    def reset(self) -> None:
        self.v = None

    def name(self) -> str:
        return "Momentum"


class Nesterov:
    """Nesterov Accelerated Gradient (NAG).

    "Look ahead" before computing gradient:

    v_t = β * v_{t-1} - η * ∇f(x_{t-1} + β * v_{t-1})
    x_t = x_{t-1} + v_t

    NAG provides better theoretical convergence rates (O(1/t²) for
    convex smooth functions vs O(1/t) for standard momentum) and
    often converges faster in practice.
    """

    def __init__(self, learning_rate: float = 0.01, beta: float = 0.9):
        self.lr = learning_rate
        self.beta = beta
        self.v: Optional[NDArray[np.float64]] = None

    def update(
        self,
        x: NDArray[np.float64],
        grad: NDArray[np.float64],
        grad_fn: Callable[[NDArray[np.float64]], NDArray[np.float64]]
    ) -> NDArray[np.float64]:
        if self.v is None:
            self.v = np.zeros_like(x)
        # Look-ahead point
        x_lookahead = x + self.beta * self.v
        # Gradient at look-ahead
        grad_lookahead = grad_fn(x_lookahead)
        self.v = self.beta * self.v - self.lr * grad_lookahead
        return x + self.v

    def reset(self) -> None:
        self.v = None

    def name(self) -> str:
        return "Nesterov"


class AdaGrad:
    """AdaGrad: Adaptive Gradient Algorithm.

    Accumulates squared gradients and uses per-parameter learning rates:

    G_t = G_{t-1} + g_t²          (sum of squared gradients)
    x_{t+1} = x_t - η * g_t / (√G_t + ε)

    Pros: Adapts learning rate per parameter, good for sparse features.
    Cons: Learning rate monotonically decreases, can stop too early
          (accumulator grows without bound).
    """

    def __init__(self, learning_rate: float = 0.1, eps: float = 1e-8):
        self.lr = learning_rate
        self.eps = eps
        self.G: Optional[NDArray[np.float64]] = None

    def update(
        self,
        x: NDArray[np.float64],
        grad: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        if self.G is None:
            self.G = np.zeros_like(x)
        self.G += grad ** 2
        adjusted_lr = self.lr / (np.sqrt(self.G) + self.eps)
        return x - adjusted_lr * grad

    def reset(self) -> None:
        self.G = None

    def name(self) -> str:
        return "AdaGrad"


class RMSProp:
    """RMSProp: Root Mean Square Propagation.

    Uses exponentially decaying average of squared gradients instead of
    accumulating all past gradients (fixes AdaGrad's diminishing LR issue):

    E[g²]_t = ρ * E[g²]_{t-1} + (1-ρ) * g_t²
    x_{t+1} = x_t - η * g_t / (√E[g²]_t + ε)

    where ρ is the decay rate (typically 0.9).
    """

    def __init__(self, learning_rate: float = 0.01, rho: float = 0.9,
                 eps: float = 1e-8):
        self.lr = learning_rate
        self.rho = rho
        self.eps = eps
        self.Eg2: Optional[NDArray[np.float64]] = None

    def update(
        self,
        x: NDArray[np.float64],
        grad: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        if self.Eg2 is None:
            self.Eg2 = np.zeros_like(x)
        self.Eg2 = self.rho * self.Eg2 + (1.0 - self.rho) * grad ** 2
        adjusted_lr = self.lr / (np.sqrt(self.Eg2) + self.eps)
        return x - adjusted_lr * grad

    def reset(self) -> None:
        self.Eg2 = None

    def name(self) -> str:
        return "RMSProp"


class Adam:
    """Adam: Adaptive Moment Estimation.

    Combines momentum (first moment) and RMSProp (second moment) with
    bias correction:

    m_t = β₁ * m_{t-1} + (1-β₁) * g_t          (momentum)
    v_t = β₂ * v_{t-1} + (1-β₂) * g_t²         (RMSProp)
    m̂_t = m_t / (1 - β₁^t)                      (bias correction)
    v̂_t = v_t / (1 - β₂^t)
    x_{t+1} = x_t - η * m̂_t / (√v̂_t + ε)

    Default hyperparameters (from the paper): β₁=0.9, β₂=0.999, ε=1e-8.

    Adam is the most widely used optimizer in deep learning due to its
    robustness, fast convergence, and minimal tuning requirements.
    """

    def __init__(
        self,
        learning_rate: float = 0.001,
        beta1: float = 0.9,
        beta2: float = 0.999,
        eps: float = 1e-8
    ):
        self.lr = learning_rate
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m: Optional[NDArray[np.float64]] = None
        self.v: Optional[NDArray[np.float64]] = None
        self.t: int = 0

    def update(
        self,
        x: NDArray[np.float64],
        grad: NDArray[np.float64]
    ) -> NDArray[np.float64]:
        if self.m is None:
            self.m = np.zeros_like(x)
            self.v = np.zeros_like(x)
        self.t += 1

        self.m = self.beta1 * self.m + (1.0 - self.beta1) * grad
        self.v = self.beta2 * self.v + (1.0 - self.beta2) * grad ** 2

        # Bias correction
        m_hat = self.m / (1.0 - self.beta1 ** self.t)
        v_hat = self.v / (1.0 - self.beta2 ** self.t)

        return x - self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

    def reset(self) -> None:
        self.m = None
        self.v = None
        self.t = 0

    def name(self) -> str:
        return "Adam"


# ============================================================
# Training Loop
# ============================================================

def optimize(
    optimizer,
    grad_fn: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    max_iter: int = 1000,
    tol: float = 1e-8
) -> Tuple[NDArray[np.float64], List[float]]:
    """Run optimization for a given optimizer and gradient function.

    Args:
        optimizer: One of SGD, Momentum, Nesterov, AdaGrad, RMSProp, Adam.
        grad_fn: Function computing gradient at a point.
        x0: Starting point.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on gradient norm.

    Returns:
        Tuple (x_opt, grad_norm_history):
            x_opt: Final point.
            grad_norm_history: List of gradient norms at each iteration.

    Complexity: O(max_iter) gradient evaluations.
    """
    x = x0.astype(np.float64).copy()
    grad_norms: List[float] = []

    for _ in range(max_iter):
        grad = grad_fn(x)
        gnorm = float(np.linalg.norm(grad))
        grad_norms.append(gnorm)

        if gnorm < tol:
            break

        # Nesterov needs the gradient function for look-ahead
        if isinstance(optimizer, Nesterov):
            x = optimizer.update(x, grad, grad_fn)
        else:
            x = optimizer.update(x, grad)

    return x, grad_norms


# ============================================================
# Comparison & Visualization
# ============================================================

def compare_optimizers(
    grad_fn: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    max_iter: int = 500
) -> Dict[str, List[float]]:
    """Compare all optimizers on a given problem.

    Args:
        grad_fn: Gradient function.
        x0: Starting point.
        max_iter: Max iterations per optimizer.

    Returns:
        Dictionary mapping optimizer name to gradient norm history.
    """
    optimizers2 = [
        SGD(learning_rate=0.09),
        Momentum(learning_rate=0.1, beta=0.9),
        Nesterov(learning_rate=0.02, beta=0.9),
        AdaGrad(learning_rate=0.5),
        RMSProp(learning_rate=0.1, rho=0.9),
        Adam(learning_rate=0.1),
    ]

    results: Dict[str, List[float]] = {}

    for opt in optimizers2:
        opt.reset()
        _, history = optimize(opt, grad_fn, x0.copy(), max_iter)
        results[opt.name()] = history

    return results


def plot_optimizer_comparison(
    results: Dict[str, List[float]],
    title: str = "Optimizer Comparison"
) -> None:
    """Plot convergence curves for multiple optimizers.

    Args:
        results: Dict mapping optimizer name to gradient norm histories.
        title: Plot title.

    Requires matplotlib.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping plot")
        return

    plt.figure(figsize=(12, 7))

    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    for (name, history), color in zip(results.items(), colors):
        iterations = range(len(history))
        plt.plot(iterations, history, label=name, color=color, linewidth=1.5)

    plt.xlabel('Iteration')
    plt.ylabel('Gradient Norm ||∇f||')
    plt.title(title)
    plt.yscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('/Users/ylmzfun/Public/item/mine/algorithm-x/algorithm-python/'
                '04-math-foundation/optimization/optimizer_comparison.png', dpi=100)
    plt.close()
    print("  Plot saved to optimizer_comparison.png")


# ============================================================
# Tests
# ============================================================

def _test_all_optimizers() -> None:
    x0 = np.array([5.0, 5.0])

    optimizers = [
        SGD(learning_rate=0.09),
        Momentum(learning_rate=0.1, beta=0.9),
        Nesterov(learning_rate=0.02, beta=0.9),
        AdaGrad(learning_rate=0.5),
        RMSProp(learning_rate=0.1, rho=0.9),
        Adam(learning_rate=0.1),
    ]

    for opt in optimizers:
        opt.reset()
        x_opt, history = optimize(opt, convex_quadratic_grad, x0.copy(),
                                  max_iter=500)
        final_dist = np.linalg.norm(x_opt)
        assert final_dist < 1.0, \
            f"{opt.name()} did not converge: dist={final_dist:.4f}"
        # Check monotonic progress (gradient norm decreasing)
        assert history[-1] < history[0], \
            f"{opt.name()} gradient norm not decreasing"
        print(f"  PASS: {opt.name():10s} ({len(history):4d} iters, "
              f"final dist={final_dist:.4f})")


def _test_convex_bowl() -> None:
    """Test that optimizers converge to (3, -2) on convex bowl."""
    x0 = np.array([0.0, 0.0])
    opt = Adam(learning_rate=0.1)
    x_opt, _ = optimize(opt, convex_bowl_grad, x0.copy(), max_iter=500)
    # Should converge near (3, -2)
    assert abs(x_opt[0] - 3.0) < 0.01, f"x0 off: {x_opt[0]}"
    assert abs(x_opt[1] + 2.0) < 0.01, f"x1 off: {x_opt[1]}"
    print(f"  PASS: convex_bowl (Adam) → x={np.round(x_opt, 3)}")


if __name__ == "__main__":
    print("Testing gradient_methods.py ...")
    _test_all_optimizers()
    _test_convex_bowl()

    print("\nComparing optimizers on convex quadratic...")
    results = compare_optimizers(convex_quadratic_grad, np.array([5.0, 5.0]))
    for name, hist in results.items():
        print(f"  {name:10s}: {len(hist):4d} iters, final ||∇f|| = {hist[-1]:.2e}")

    # Generate visualization
    try:
        plot_optimizer_comparison(results, "Optimizer Convergence on Convex Quadratic")
    except Exception as e:
        print(f"  Visualization skipped: {e}")

    print("\nAll gradient_methods tests PASSED!")
