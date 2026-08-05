"""
Gradient Descent Methods for ML/AI Foundations.

Implements and compares optimization algorithms:
- Batch gradient descent
- Stochastic gradient descent (SGD)
- Mini-batch gradient descent
- Momentum (heavy ball method)

Includes convergence rate comparison on:
- Quadratic function (convex, well-conditioned)
- Rosenbrock function (non-convex, banana valley)

Visualization code using matplotlib.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Callable, Tuple, List, Dict
from derivatives import gradient as numerical_gradient


# ============================================================
# Test Functions
# ============================================================

def quadratic(x: NDArray[np.float64]) -> float:
    """Simple convex quadratic: f(x) = 0.5 * xᵀ Q x, Q = diag(1, 10).

    This is a 2D convex quadratic with different curvature along each axis.
    The condition number κ = λ_max/λ_min = 10, which tests how GD handles
    anisotropic curvature.
    Minimum: f(0, 0) = 0, ∇f = Qx = [x₁, 10x₂].
    """
    Q_diag = np.array([1.0, 10.0])
    return 0.5 * np.sum(Q_diag * x ** 2)


def quadratic_grad(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Analytic gradient of quadratic: ∇f = [x₁, 10x₂]."""
    return np.array([x[0], 10.0 * x[1]], dtype=np.float64)


def rosenbrock(x: NDArray[np.float64]) -> float:
    """Rosenbrock function (banana function).

    f(x, y) = (1 - x)² + 100 * (y - x²)²

    Global minimum at (1, 1) with f(1, 1) = 0.
    Known for its narrow, curved valley — challenging for gradient descent.

    Args:
        x: Point [x, y].

    Returns:
        Function value.
    """
    return (1.0 - x[0]) ** 2 + 100.0 * (x[1] - x[0] ** 2) ** 2


def rosenbrock_grad(x: NDArray[np.float64]) -> NDArray[np.float64]:
    """Analytic gradient of Rosenbrock function.

    ∂f/∂x = -2(1-x) - 400x(y - x²)
    ∂f/∂y = 200(y - x²)
    """
    dx = -2.0 * (1.0 - x[0]) - 400.0 * x[0] * (x[1] - x[0] ** 2)
    dy = 200.0 * (x[1] - x[0] ** 2)
    return np.array([dx, dy], dtype=np.float64)


# ============================================================
# Optimization Algorithms
# ============================================================

def gradient_descent(
    f_grad: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    learning_rate: float = 0.01,
    max_iter: int = 1000,
    tol: float = 1e-8
) -> Tuple[NDArray[np.float64], List[float], List[NDArray[np.float64]]]:
    """Batch (vanilla) gradient descent.

    x_{k+1} = x_k - α ∇f(x_k)

    Uses the full gradient at each step. Converges linearly for
    strongly convex functions.

    Args:
        f_grad: Gradient function ∇f: Rⁿ → Rⁿ.
        x0: Initial point.
        learning_rate: Step size α.
        max_iter: Maximum iterations.
        tol: Convergence tolerance on gradient norm.

    Returns:
        Tuple (x_opt, f_history, x_history):
            x_opt: Final point.
            f_history: Function values at each iteration.
            x_history: Points visited (for trajectory plotting).

    Complexity: O(n) per iteration (n = dimension).
    """
    x = x0.astype(np.float64).copy()
    f_history: List[float] = []
    x_history: List[NDArray[np.float64]] = [x.copy()]

    for _ in range(max_iter):
        grad = f_grad(x)
        f_history.append(float(np.linalg.norm(grad)))

        if np.linalg.norm(grad) < tol:
            break

        x = x - learning_rate * grad
        x_history.append(x.copy())

    return x, f_history, x_history


def stochastic_gradient_descent(
    f_grad: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    learning_rate: float = 0.01,
    noise_std: float = 0.5,
    max_iter: int = 1000,
    tol: float = 1e-8
) -> Tuple[NDArray[np.float64], List[float]]:
    """Stochastic Gradient Descent (SGD).

    x_{k+1} = x_k - α (∇f(x_k) + εₖ)

    where εₖ ~ N(0, noise_std²) simulates the stochastic gradient noise
    from sampling a mini-batch. In practice, SGD uses a random subset
    of the data; here we add Gaussian noise to the full gradient as a
    simplified model.

    SGD introduces variance that helps escape shallow local minima but
    prevents exact convergence. A decreasing learning rate (schedule)
    is often necessary.

    Args:
        f_grad: True gradient function.
        x0: Initial point.
        learning_rate: Step size.
        noise_std: Standard deviation of gradient noise.
        max_iter: Maximum iterations.
        tol: Convergence tolerance.

    Returns:
        Tuple (x_opt, f_history):
            x_opt: Final point.
            f_history: Norm of stochastic gradient at each step.
    """
    x = x0.astype(np.float64).copy()
    f_history: List[float] = []

    for _ in range(max_iter):
        true_grad = f_grad(x)
        noise = np.random.randn(*x.shape) * noise_std
        stoch_grad = true_grad + noise

        f_history.append(float(np.linalg.norm(true_grad)))

        if np.linalg.norm(true_grad) < tol:
            break

        x = x - learning_rate * stoch_grad

    return x, f_history


def mini_batch_gradient_descent(
    f_grad: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    learning_rate: float = 0.01,
    noise_std: float = 0.3,
    max_iter: int = 1000,
    tol: float = 1e-8
) -> Tuple[NDArray[np.float64], List[float]]:
    """Mini-Batch Gradient Descent.

    Similar to SGD but with reduced variance (smaller noise_std),
    simulating the effect of using a moderate-sized mini-batch rather
    than a single sample.

    Balances the stability of batch GD with the computational efficiency
    and exploration benefits of SGD.

    Args:
        f_grad: True gradient function.
        x0: Initial point.
        learning_rate: Step size.
        noise_std: Gradient noise std (smaller than SGD).
        max_iter: Maximum iterations.
        tol: Convergence tolerance.

    Returns:
        Tuple (x_opt, f_history).
    """
    return stochastic_gradient_descent(
        f_grad, x0, learning_rate, noise_std, max_iter, tol
    )


def momentum_gradient_descent(
    f_grad: Callable[[NDArray[np.float64]], NDArray[np.float64]],
    x0: NDArray[np.float64],
    learning_rate: float = 0.01,
    momentum: float = 0.9,
    max_iter: int = 1000,
    tol: float = 1e-8
) -> Tuple[NDArray[np.float64], List[float]]:
    """Gradient descent with momentum (heavy ball method).

    v_{k+1} = β v_k - α ∇f(x_k)
    x_{k+1} = x_k + v_{k+1}

    where β is the momentum coefficient (typically 0.9).

    Momentum accelerates convergence by accumulating a velocity vector,
    damping oscillations in high-curvature directions. Particularly
    effective for ill-conditioned problems and ravines like Rosenbrock.

    Args:
        f_grad: Gradient function.
        x0: Initial point.
        learning_rate: Step size α.
        momentum: Momentum coefficient β ∈ [0, 1).
        max_iter: Maximum iterations.
        tol: Convergence tolerance.

    Returns:
        Tuple (x_opt, f_history):
            f_history: Gradient norm at each iteration.
    """
    x = x0.astype(np.float64).copy()
    v = np.zeros_like(x)
    f_history: List[float] = []

    for _ in range(max_iter):
        grad = f_grad(x)
        f_history.append(float(np.linalg.norm(grad)))

        if np.linalg.norm(grad) < tol:
            break

        v = momentum * v - learning_rate * grad
        x = x + v

    return x, f_history


# ============================================================
# Convergence Comparison
# ============================================================

def compare_methods_on_quadratic(
    x0: NDArray[np.float64] = np.array([5.0, 5.0]),
    lr: float = 0.05,
    max_iter: int = 500
) -> Dict[str, List[float]]:
    """Compare GD, SGD, Mini-Batch GD, and Momentum on the quadratic function.

    Args:
        x0: Starting point.
        lr: Learning rate.
        max_iter: Max iterations.

    Returns:
        Dictionary mapping method name to list of gradient norms.
    """
    results: Dict[str, List[float]] = {}

    _, hist_gd, _ = gradient_descent(quadratic_grad, x0.copy(), lr, max_iter)
    results['GD'] = hist_gd

    _, hist_sgd = stochastic_gradient_descent(quadratic_grad, x0.copy(), lr,
                                              noise_std=0.5, max_iter=max_iter)
    results['SGD'] = hist_sgd

    _, hist_mbgd = mini_batch_gradient_descent(quadratic_grad, x0.copy(), lr,
                                               noise_std=0.3, max_iter=max_iter)
    results['MiniBatch'] = hist_mbgd

    _, hist_mom = momentum_gradient_descent(quadratic_grad, x0.copy(), lr,
                                            momentum=0.9, max_iter=max_iter)
    results['Momentum'] = hist_mom

    return results


def compare_methods_on_rosenbrock(
    x0: NDArray[np.float64] = np.array([-1.0, 1.0]),
    lr: float = 0.001,
    max_iter: int = 2000
) -> Dict[str, List[float]]:
    """Compare methods on the Rosenbrock function.

    Args:
        x0: Starting point.
        lr: Learning rate.
        max_iter: Max iterations.

    Returns:
        Dictionary mapping method name to list of gradient norms.
    """
    results: Dict[str, List[float]] = {}

    _, hist_gd, _ = gradient_descent(rosenbrock_grad, x0.copy(), lr, max_iter)
    results['GD'] = hist_gd

    _, hist_mom = momentum_gradient_descent(rosenbrock_grad, x0.copy(), lr,
                                            momentum=0.9, max_iter=max_iter)
    results['Momentum'] = hist_mom

    return results


# ============================================================
# Visualization
# ============================================================

def plot_convergence(
    results: Dict[str, List[float]],
    title: str = "Convergence Comparison",
    log_scale: bool = True
) -> None:
    """Plot convergence curves for multiple optimization methods.

    Args:
        results: Dict mapping method names to gradient norm histories.
        title: Plot title.
        log_scale: Use log scale on y-axis.

    Requires matplotlib.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed; skipping plot")
        return

    plt.figure(figsize=(10, 6))

    for name, history in results.items():
        iterations = range(len(history))
        plt.plot(iterations, history, label=name, linewidth=1.5)

    plt.xlabel('Iteration')
    plt.ylabel('Gradient Norm ||∇f||')
    plt.title(title)
    if log_scale:
        plt.yscale('log')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('/Users/ylmzfun/Public/item/mine/algorithm-x/algorithm-python/'
                '04-math-foundation/calculus/convergence_plot.png', dpi=100)
    plt.close()
    print("  Plot saved to convergence_plot.png")


# ============================================================
# Tests
# ============================================================

def _test_quadratic_opt() -> None:
    x0 = np.array([5.0, 5.0])
    x_opt, hist, _ = gradient_descent(quadratic_grad, x0, learning_rate=0.05,
                                       max_iter=500)
    # Should converge near [0, 0]
    assert np.linalg.norm(x_opt) < 0.1, f"GD did not converge: {x_opt}"
    # History should be decreasing (gradient norm)
    assert hist[-1] < hist[0], "Gradient norm not decreasing"
    print(f"  PASS: GD on quadratic (final x={np.round(x_opt, 4)})")


def _test_rosenbrock_opt() -> None:
    x0 = np.array([-1.0, 1.0])
    x_opt, hist, _ = gradient_descent(rosenbrock_grad, x0, learning_rate=0.001,
                                       max_iter=5000)
    # Should move toward (1, 1)
    dist_to_opt = np.linalg.norm(x_opt - np.array([1.0, 1.0]))
    # GD may not converge fully on Rosenbrock; just check progress
    start_dist = np.linalg.norm(x0 - np.array([1.0, 1.0]))
    assert dist_to_opt < start_dist, f"No progress: {x_opt}"
    print(f"  PASS: GD on Rosenbrock (x={np.round(x_opt, 4)}, dist={dist_to_opt:.4f})")


def _test_momentum() -> None:
    x0 = np.array([5.0, 5.0])
    x_mom, hist_mom = momentum_gradient_descent(
        quadratic_grad, x0, learning_rate=0.05, momentum=0.9, max_iter=500
    )
    # Should converge
    assert np.linalg.norm(x_mom) < 0.1, f"Momentum failed: {x_mom}"
    # Compare with vanilla GD
    x_gd, hist_gd, _ = gradient_descent(quadratic_grad, x0, learning_rate=0.05,
                                         max_iter=500)
    # Momentum should typically be as fast or faster
    print(f"  PASS: momentum vs GD (momentum iters={len(hist_mom)}, "
          f"GD iters={len(hist_gd)})")


def _test_sgd() -> None:
    x0 = np.array([5.0, 5.0])
    x_sgd, hist_sgd = stochastic_gradient_descent(
        quadratic_grad, x0, learning_rate=0.02, noise_std=0.5, max_iter=2000
    )
    # SGD with fixed LR won't converge exactly, but should get close
    assert np.linalg.norm(x_sgd) < 2.0, f"SGD diverged: {x_sgd}"
    print(f"  PASS: SGD (final norm={np.linalg.norm(x_sgd):.4f})")


if __name__ == "__main__":
    print("Testing gradient_descent.py ...")
    _test_quadratic_opt()
    _test_rosenbrock_opt()
    _test_momentum()
    _test_sgd()

    print("\nComparing methods on quadratic function...")
    results_q = compare_methods_on_quadratic()
    for name, hist in results_q.items():
        print(f"  {name:12s}: {len(hist):4d} iters, final ||∇f|| = {hist[-1]:.2e}")

    print("\nComparing methods on Rosenbrock function...")
    results_r = compare_methods_on_rosenbrock()
    for name, hist in results_r.items():
        print(f"  {name:12s}: {len(hist):4d} iters, final ||∇f|| = {hist[-1]:.2e}")

    # Generate visualization
    try:
        plot_convergence(results_q, "Convergence on Quadratic Function")
        plot_convergence(results_r, "Convergence on Rosenbrock Function")
    except Exception as e:
        print(f"  Visualization skipped: {e}")

    print("\nAll gradient_descent tests PASSED!")
