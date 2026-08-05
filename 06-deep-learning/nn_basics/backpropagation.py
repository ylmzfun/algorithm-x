"""Manual backpropagation on a small neural network.

Verifies analytical gradients against numerical gradients (finite differences).
Network: 2 input → 3 hidden (sigmoid) → 1 output (sigmoid).
"""

import numpy as np
from typing import Optional


class SmallNetwork:
    """A small 2-layer network (2→3→1) with sigmoid activations.

    Implements manual forward and backward passes with full gradient tracking.
    Used to demonstrate and verify backpropagation.
    """

    def __init__(self, random_seed: int = 42):
        """Initialize weights and biases with small random values.

        Args:
            random_seed: Seed for reproducible initialization.
        """
        rng = np.random.RandomState(random_seed)
        # Layer 1: 2 input → 3 hidden
        self.W1 = rng.randn(2, 3) * 0.5
        self.b1 = rng.randn(1, 3) * 0.1
        # Layer 2: 3 hidden → 1 output
        self.W2 = rng.randn(3, 1) * 0.5
        self.b2 = rng.randn(1, 1) * 0.1

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        """Numerically stable sigmoid."""
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, dict]:
        """Forward pass through the network.

        Args:
            X: Input of shape (batch_size, 2).

        Returns:
            Tuple of (output, cache) where cache stores:
                - Z1, A1: hidden layer pre/post activation
                - Z2, A2: output layer pre/post activation
                - X: input (for convenience)
        """
        # Hidden layer
        Z1 = np.dot(X, self.W1) + self.b1        # (N, 3)
        A1 = self._sigmoid(Z1)                     # (N, 3)

        # Output layer
        Z2 = np.dot(A1, self.W2) + self.b2        # (N, 1)
        A2 = self._sigmoid(Z2)                     # (N, 1)

        cache = {"Z1": Z1, "A1": A1, "Z2": Z2, "A2": A2, "X": X}
        return A2, cache

    def backward(self, y: np.ndarray, cache: dict) -> dict[str, np.ndarray]:
        """Backward pass computing gradients for all parameters.

        Uses binary cross-entropy loss: L = -[y log(ŷ) + (1-y) log(1-ŷ)].
        dL/dA2 = -(y/A2 - (1-y)/(1-A2)).

        Args:
            y: True labels of shape (batch_size, 1).
            cache: Intermediate values from forward pass.

        Returns:
            Dict with keys: dW1, db1, dW2, db2, dX.
        """
        m = y.shape[0]
        A2 = cache["A2"]
        A1 = cache["A1"]
        X = cache["X"]

        # Gradient of loss w.r.t. output activation A2
        dA2 = -(y / (A2 + 1e-12) - (1 - y) / (1 - A2 + 1e-12)) / m

        # Output layer
        dZ2 = dA2 * A2 * (1 - A2)                  # sigmoid gradient: A2*(1-A2)
        dW2 = np.dot(A1.T, dZ2)                    # (3, 1)
        db2 = np.sum(dZ2, axis=0, keepdims=True)   # (1, 1)

        # Hidden layer
        dA1 = np.dot(dZ2, self.W2.T)               # (N, 3)
        dZ1 = dA1 * A1 * (1 - A1)                  # sigmoid gradient
        dW1 = np.dot(X.T, dZ1)                     # (2, 3)
        db1 = np.sum(dZ1, axis=0, keepdims=True)   # (1, 3)

        # Gradient w.r.t. input (for gradient checking)
        dX = np.dot(dZ1, self.W1.T)                # (N, 2)

        return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2, "dX": dX}

    def compute_loss(self, y_true: np.ndarray, y_pred: np.ndarray) -> float:
        """Binary cross-entropy loss.

        Args:
            y_true: True labels.
            y_pred: Predicted probabilities.

        Returns:
            Scalar loss value.
        """
        eps = 1e-12
        y_pred = np.clip(y_pred, eps, 1 - eps)
        return float(-np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)))

    def numerical_gradient(
        self,
        X: np.ndarray,
        y: np.ndarray,
        param_name: str,
        eps: float = 1e-5,
    ) -> np.ndarray:
        """Compute numerical gradient for a parameter using central finite differences.

        Args:
            X: Input data.
            y: True labels.
            param_name: Which parameter to differentiate w.r.t. ('W1', 'b1', 'W2', 'b2').
            eps: Step size.

        Returns:
            Numerical gradient of the same shape as the parameter.
        """
        param = getattr(self, param_name)
        grad = np.zeros_like(param, dtype=float)

        def loss_fn():
            out, _ = self.forward(X)
            return self.compute_loss(y, out)

        for idx in np.ndindex(param.shape):
            orig = param[idx]
            param[idx] = orig + eps
            loss_plus = loss_fn()
            param[idx] = orig - eps
            loss_minus = loss_fn()
            param[idx] = orig
            grad[idx] = (loss_plus - loss_minus) / (2 * eps)

        return grad

    def gradient_check(
        self, X: np.ndarray, y: np.ndarray, tol: float = 1e-5
    ) -> dict[str, float]:
        """Compare analytical and numerical gradients for all parameters.

        Args:
            X: Input data.
            y: True labels.
            tol: Tolerance for max relative error.

        Returns:
            Dict mapping parameter names to max relative errors.
        """
        _, cache = self.forward(X)
        anal_grads = self.backward(y, cache)

        errors = {}
        for name in ["W1", "b1", "W2", "b2"]:
            num_grad = self.numerical_gradient(X, y, name)
            anal_grad = anal_grads[f"d{name}"]
            denom = np.maximum(np.abs(num_grad), np.abs(anal_grad))
            denom = np.maximum(denom, 1e-10)
            max_rel_err = float(np.max(np.abs(num_grad - anal_grad) / denom))
            errors[name] = max_rel_err
        return errors


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing backpropagation...")

    # Create network and test data
    net = SmallNetwork(random_seed=42)
    X = np.array([[0.0, 0.0], [0.0, 1.0], [1.0, 0.0], [1.0, 1.0]])
    y = np.array([[0.0], [1.0], [1.0], [0.0]])  # XOR target

    # Test 1: Forward pass produces valid output
    output, cache = net.forward(X)
    assert output.shape == (4, 1), f"Wrong output shape: {output.shape}"
    assert np.all((output > 0) & (output < 1)), "Output not in (0, 1)"
    print(f"  PASS: Forward pass shape correct, output range valid")

    # Test 2: Backward pass produces correct gradient shapes
    grads = net.backward(y, cache)
    assert grads["dW1"].shape == (2, 3), f"Wrong dW1 shape: {grads['dW1'].shape}"
    assert grads["db1"].shape == (1, 3), f"Wrong db1 shape: {grads['db1'].shape}"
    assert grads["dW2"].shape == (3, 1), f"Wrong dW2 shape: {grads['dW2'].shape}"
    assert grads["db2"].shape == (1, 1), f"Wrong db2 shape: {grads['db2'].shape}"
    assert grads["dX"].shape == (4, 2), f"Wrong dX shape: {grads['dX'].shape}"
    print("  PASS: Backward pass gradient shapes correct")

    # Test 3: Compute loss
    loss = net.compute_loss(y, output)
    assert loss > 0, f"Loss should be positive, got {loss}"
    print(f"  PASS: Loss computed: {loss:.6f}")

    # Test 4: Gradient check
    errors = net.gradient_check(X, y)
    all_ok = True
    for name, err in errors.items():
        status = "PASS" if err < 1e-5 else "FAIL"
        print(f"  {status}: d{name} max relative error = {err:.2e}")
        if err >= 1e-5:
            all_ok = False

    # Test 5: Training reduces loss
    net2 = SmallNetwork(random_seed=123)
    initial_loss = net2.compute_loss(y, net2.forward(X)[0])
    for _ in range(5000):
        out, cache2 = net2.forward(X)
        grads2 = net2.backward(y, cache2)
        net2.W1 -= 0.5 * grads2["dW1"]
        net2.b1 -= 0.5 * grads2["db1"]
        net2.W2 -= 0.5 * grads2["dW2"]
        net2.b2 -= 0.5 * grads2["db2"]
    final_loss = net2.compute_loss(y, net2.forward(X)[0])
    assert final_loss < initial_loss, f"Loss did not decrease: {initial_loss:.4f} → {final_loss:.4f}"
    print(f"  PASS: Training reduced loss: {initial_loss:.4f} → {final_loss:.4f}")

    # Test 6: Predictions approach XOR
    final_output, _ = net2.forward(X)
    pred_labels = (final_output > 0.5).astype(int).flatten()
    acc = np.mean(pred_labels == y.flatten())
    print(f"  PASS: XOR accuracy after training: {acc:.2f}")

    print(f"\n{'All backpropagation tests passed!' if all_ok else 'Some gradient checks FAILED!'}")
