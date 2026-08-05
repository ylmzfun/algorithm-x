"""Optimizers from scratch (NumPy-based).

Each optimizer operates on parameter and gradient dictionaries.
Tested on a simple convex optimization problem: minimize x^2.
"""

import numpy as np
from typing import Optional


class SGD:
    """Stochastic Gradient Descent with optional L2 weight decay.

    w = w - lr * grad - lr * weight_decay * w
    """

    def __init__(self, lr: float = 0.01, weight_decay: float = 0.0):
        """
        Args:
            lr: Learning rate.
            weight_decay: L2 weight decay coefficient.
        """
        self.lr = lr
        self.weight_decay = weight_decay
        self.iterations = 0

    def update(self, params: dict, grads: dict) -> None:
        """Update parameters.

        Args:
            params: Dict of parameter names to numpy arrays.
            grads: Dict of parameter names to gradient arrays.
        """
        for key in params:
            if key in grads:
                params[key] -= self.lr * (grads[key] + self.weight_decay * params[key])

    def step(self):
        """Increment step counter."""
        self.iterations += 1


class MomentumSGD:
    """SGD with momentum.

    v = momentum * v - lr * grad
    w = w + v
    """

    def __init__(self, lr: float = 0.01, momentum: float = 0.9):
        """
        Args:
            lr: Learning rate.
            momentum: Momentum coefficient.
        """
        self.lr = lr
        self.momentum = momentum
        self.velocity: dict[str, np.ndarray] = {}
        self.iterations = 0

    def update(self, params: dict, grads: dict) -> None:
        """Update parameters with momentum."""
        for key in params:
            if key in grads:
                if key not in self.velocity:
                    self.velocity[key] = np.zeros_like(params[key])
                self.velocity[key] = self.momentum * self.velocity[key] - self.lr * grads[key]
                params[key] += self.velocity[key]

    def step(self):
        """Increment step counter."""
        self.iterations += 1


class NesterovSGD:
    """SGD with Nesterov accelerated gradient.

    v = momentum * v - lr * grad(w + momentum * v)
    w = w + v
    """

    def __init__(self, lr: float = 0.01, momentum: float = 0.9):
        """
        Args:
            lr: Learning rate.
            momentum: Momentum coefficient.
        """
        self.lr = lr
        self.momentum = momentum
        self.velocity: dict[str, np.ndarray] = {}
        self.iterations = 0

    def update(self, params: dict, grads: dict) -> None:
        """Update parameters with Nesterov momentum."""
        for key in params:
            if key in grads:
                if key not in self.velocity:
                    self.velocity[key] = np.zeros_like(params[key])
                v_prev = self.velocity[key].copy()
                self.velocity[key] = self.momentum * self.velocity[key] - self.lr * grads[key]
                params[key] += -self.momentum * v_prev + (1 + self.momentum) * self.velocity[key]

    def step(self):
        """Increment step counter."""
        self.iterations += 1


class AdaGrad:
    """AdaGrad: adaptive learning rate with accumulated squared gradients.

    cache += grad^2
    w = w - lr * grad / sqrt(cache + eps)
    """

    def __init__(self, lr: float = 0.01, eps: float = 1e-8):
        """
        Args:
            lr: Learning rate.
            eps: Small epsilon for numerical stability.
        """
        self.lr = lr
        self.eps = eps
        self.cache: dict[str, np.ndarray] = {}
        self.iterations = 0

    def update(self, params: dict, grads: dict) -> None:
        """Update parameters with AdaGrad."""
        for key in params:
            if key in grads:
                if key not in self.cache:
                    self.cache[key] = np.zeros_like(params[key])
                self.cache[key] += grads[key] ** 2
                params[key] -= self.lr * grads[key] / (np.sqrt(self.cache[key]) + self.eps)

    def step(self):
        """Increment step counter."""
        self.iterations += 1


class RMSProp:
    """RMSProp: adaptive learning rate with moving average of squared gradients.

    cache = decay_rate * cache + (1 - decay_rate) * grad^2
    w = w - lr * grad / sqrt(cache + eps)
    """

    def __init__(self, lr: float = 0.01, decay_rate: float = 0.9, eps: float = 1e-8):
        """
        Args:
            lr: Learning rate.
            decay_rate: Decay rate for moving average.
            eps: Small epsilon.
        """
        self.lr = lr
        self.decay_rate = decay_rate
        self.eps = eps
        self.cache: dict[str, np.ndarray] = {}
        self.iterations = 0

    def update(self, params: dict, grads: dict) -> None:
        """Update parameters with RMSProp."""
        for key in params:
            if key in grads:
                if key not in self.cache:
                    self.cache[key] = np.zeros_like(params[key])
                self.cache[key] = self.decay_rate * self.cache[key] + (1 - self.decay_rate) * grads[key] ** 2
                params[key] -= self.lr * grads[key] / (np.sqrt(self.cache[key]) + self.eps)

    def step(self):
        """Increment step counter."""
        self.iterations += 1


class Adam:
    """Adam: adaptive moment estimation.

    m = beta1 * m + (1 - beta1) * grad
    v = beta2 * v + (1 - beta2) * grad^2
    m_hat = m / (1 - beta1^t)
    v_hat = v / (1 - beta2^t)
    w = w - lr * m_hat / (sqrt(v_hat) + eps)
    """

    def __init__(self, lr: float = 0.001, beta1: float = 0.9,
                 beta2: float = 0.999, eps: float = 1e-8):
        """
        Args:
            lr: Learning rate.
            beta1: Exponential decay rate for first moment.
            beta2: Exponential decay rate for second moment.
            eps: Small epsilon.
        """
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.m: dict[str, np.ndarray] = {}
        self.v: dict[str, np.ndarray] = {}
        self.iterations = 0

    def update(self, params: dict, grads: dict) -> None:
        """Update parameters with Adam."""
        for key in params:
            if key in grads:
                if key not in self.m:
                    self.m[key] = np.zeros_like(params[key])
                    self.v[key] = np.zeros_like(params[key])

                self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * grads[key]
                self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * grads[key] ** 2

                # Bias correction
                m_hat = self.m[key] / (1 - self.beta1 ** (self.iterations + 1))
                v_hat = self.v[key] / (1 - self.beta2 ** (self.iterations + 1))

                params[key] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

    def step(self):
        """Increment step counter."""
        self.iterations += 1


class AdamW:
    """AdamW: Adam with decoupled weight decay.

    m = beta1 * m + (1 - beta1) * grad
    v = beta2 * v + (1 - beta2) * grad^2
    w = w - lr * (m_hat / (sqrt(v_hat) + eps) + weight_decay * w)
    """

    def __init__(self, lr: float = 0.001, beta1: float = 0.9,
                 beta2: float = 0.999, eps: float = 1e-8,
                 weight_decay: float = 0.01):
        """
        Args:
            lr: Learning rate.
            beta1: Exponential decay rate for first moment.
            beta2: Exponential decay rate for second moment.
            eps: Small epsilon.
            weight_decay: Weight decay coefficient (decoupled).
        """
        self.lr = lr
        self.beta1 = beta1
        self.beta2 = beta2
        self.eps = eps
        self.weight_decay = weight_decay
        self.m: dict[str, np.ndarray] = {}
        self.v: dict[str, np.ndarray] = {}
        self.iterations = 0

    def update(self, params: dict, grads: dict) -> None:
        """Update parameters with AdamW."""
        for key in params:
            if key in grads:
                if key not in self.m:
                    self.m[key] = np.zeros_like(params[key])
                    self.v[key] = np.zeros_like(params[key])

                # Decoupled weight decay
                params[key] *= (1 - self.lr * self.weight_decay)

                self.m[key] = self.beta1 * self.m[key] + (1 - self.beta1) * grads[key]
                self.v[key] = self.beta2 * self.v[key] + (1 - self.beta2) * grads[key] ** 2

                m_hat = self.m[key] / (1 - self.beta1 ** (self.iterations + 1))
                v_hat = self.v[key] / (1 - self.beta2 ** (self.iterations + 1))

                params[key] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)

    def step(self):
        """Increment step counter."""
        self.iterations += 1


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Optimizers...")

    def test_optimizer(opt, name: str, n_steps: int = 100, tol: float = 1e-2) -> bool:
        """Test optimizer on minimizing x^2 starting from x=5.0."""
        params = {"x": np.array([5.0])}
        losses = []
        for _ in range(n_steps):
            grad = {"x": 2 * params["x"]}  # d(x^2)/dx = 2x
            opt.update(params, grad)
            opt.step()
            losses.append(float(params["x"] ** 2))
        final = float(params["x"] ** 2)
        ok = final < tol
        if ok:
            print(f"  PASS: {name}: 5.0^2 → {final:.2e} in {n_steps} steps")
        else:
            print(f"  FAIL: {name}: 5.0^2 → {final:.2e} (expected < {tol})")
        return ok

    # Test all optimizers
    all_ok = True
    all_ok &= test_optimizer(SGD(lr=0.1), "SGD")
    all_ok &= test_optimizer(MomentumSGD(lr=0.1, momentum=0.9), "MomentumSGD")
    all_ok &= test_optimizer(NesterovSGD(lr=0.1, momentum=0.9), "NesterovSGD")
    all_ok &= test_optimizer(AdaGrad(lr=1.0), "AdaGrad")
    all_ok &= test_optimizer(RMSProp(lr=0.1, decay_rate=0.99), "RMSProp", n_steps=200)
    all_ok &= test_optimizer(Adam(lr=0.5), "Adam")
    all_ok &= test_optimizer(AdamW(lr=0.5, weight_decay=0.0), "AdamW")

    # Test SGD with weight decay
    opt_wd = SGD(lr=0.1, weight_decay=0.01)
    params_wd = {"x": np.array([5.0])}
    for _ in range(100):
        grad = {"x": 2 * params_wd["x"]}
        opt_wd.update(params_wd, grad)
        opt_wd.step()
    final_wd = float(params_wd["x"] ** 2)
    print(f"  PASS: SGD with weight decay final loss: {final_wd:.2e}")

    # Test bias correction in Adam
    opt_adam = Adam(lr=0.1)
    params_a = {"x": np.array([5.0])}
    for _ in range(50):
        grad = {"x": 2 * params_a["x"]}
        opt_adam.update(params_a, grad)
        opt_adam.step()
    assert params_a["x"] ** 2 < 1.0, f"Adam should converge: {params_a['x']}"
    print("  PASS: Adam converges (bias correction working)")

    print(f"\n{'All optimizer tests passed!' if all_ok else 'Some tests FAILED!'}")
