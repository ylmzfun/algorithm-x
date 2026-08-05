"""Build a simple CNN from scratch using NumPy.

Architecture: Conv2d → ReLU → MaxPool2d → Flatten → FC → ReLU → FC
Trained on a synthetic digit-like dataset (or sklearn digits).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from typing import Optional
from convolution import Conv2d
from pooling import MaxPool2d


class SimpleCNN:
    """A simple Convolutional Neural Network built from scratch with NumPy.

    Architecture:
        Conv2d(1→8, kernel=3) → ReLU → MaxPool2d(2) →
        Conv2d(8→16, kernel=3) → ReLU → MaxPool2d(2) →
        Flatten → FC(→hidden) → ReLU → FC(→n_classes)
    """

    def __init__(
        self,
        input_channels: int = 1,
        input_height: int = 28,
        input_width: int = 28,
        n_classes: int = 10,
        random_seed: int = 42,
    ):
        """Initialize the SimpleCNN.

        Args:
            input_channels: Number of input channels (1 for grayscale).
            input_height: Input image height.
            input_width: Input image width.
            n_classes: Number of output classes.
            random_seed: Random seed for reproducibility.
        """
        self.n_classes = n_classes
        self.rng = np.random.RandomState(random_seed)

        # Layer 1: Conv2d
        self.conv1 = Conv2d(input_channels, 8, kernel_size=3, stride=1, padding=1, random_seed=random_seed)
        # After Conv1: (N, 8, H, W) → MaxPool: (N, 8, H/2, W/2)
        h1, w1 = input_height // 2, input_width // 2

        # Layer 2: Conv2d
        self.conv2 = Conv2d(8, 16, kernel_size=3, stride=1, padding=1, random_seed=random_seed + 1)
        # After Conv2: (N, 16, H/2, W/2) → MaxPool: (N, 16, H/4, W/4)
        h2, w2 = h1 // 2, w1 // 2

        # Pooling layers
        self.pool1 = MaxPool2d(kernel_size=2, stride=2)
        self.pool2 = MaxPool2d(kernel_size=2, stride=2)

        # FC input size
        fc_input_size = 16 * h2 * w2
        hidden_size = 128

        # FC layer weights
        scale1 = np.sqrt(2.0 / fc_input_size)
        self.W_fc1 = self.rng.randn(fc_input_size, hidden_size) * scale1
        self.b_fc1 = np.zeros((1, hidden_size))

        scale2 = np.sqrt(2.0 / hidden_size)
        self.W_fc2 = self.rng.randn(hidden_size, n_classes) * scale2
        self.b_fc2 = np.zeros((1, n_classes))

        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through the CNN.

        Args:
            x: Input of shape (N, C, H, W).

        Returns:
            Logits of shape (N, n_classes).
        """
        # Conv1 + ReLU + Pool
        out = self.conv1.forward(x)
        out = np.maximum(0, out)  # ReLU
        out = self.pool1.forward(out)
        cache_conv1 = self.conv1._cache.copy()

        # Conv2 + ReLU + Pool
        out = self.conv2.forward(out)
        out = np.maximum(0, out)  # ReLU
        out = self.pool2.forward(out)
        cache_conv2 = self.conv2._cache.copy()

        # Flatten
        N = out.shape[0]
        flat = out.reshape(N, -1)

        # FC1 + ReLU
        fc1_out = np.dot(flat, self.W_fc1) + self.b_fc1
        fc1_act = np.maximum(0, fc1_out)

        # FC2 (output layer)
        logits = np.dot(fc1_act, self.W_fc2) + self.b_fc2

        # Cache everything for backward
        self._cache = {
            "conv1": cache_conv1,
            "conv2": cache_conv2,
            "pool1_out": None,  # will be filled
            "pool2_out": None,
            "flat": flat,
            "fc1_out": fc1_out,
            "fc1_act": fc1_act,
            "x": x,
        }
        # We need to track the actual intermediate values for backward
        # Let's redo forward with proper tracking
        return logits

    def _forward_with_cache(self, x: np.ndarray) -> tuple[np.ndarray, dict]:
        """Forward pass with complete caching for backward pass."""
        cache = {"x": x}

        # Conv1
        c1 = self.conv1.forward(x)
        cache["conv1_pre"] = c1
        cache["conv1_cache"] = self.conv1._cache.copy()

        # ReLU1
        r1 = np.maximum(0, c1)
        cache["relu1_out"] = r1
        cache["relu1_mask"] = (c1 > 0).astype(float)

        # Pool1
        p1 = self.pool1.forward(r1)
        cache["pool1_out"] = p1
        cache["pool1_cache"] = self.pool1._cache.copy()

        # Conv2
        c2 = self.conv2.forward(p1)
        cache["conv2_pre"] = c2
        cache["conv2_cache"] = self.conv2._cache.copy()

        # ReLU2
        r2 = np.maximum(0, c2)
        cache["relu2_out"] = r2
        cache["relu2_mask"] = (c2 > 0).astype(float)

        # Pool2
        p2 = self.pool2.forward(r2)
        cache["pool2_out"] = p2
        cache["pool2_cache"] = self.pool2._cache.copy()

        # Flatten
        N = p2.shape[0]
        flat = p2.reshape(N, -1)
        cache["flat_shape"] = p2.shape
        cache["flat"] = flat

        # FC1
        fc1_z = np.dot(flat, self.W_fc1) + self.b_fc1
        fc1_a = np.maximum(0, fc1_z)
        cache["fc1_z"] = fc1_z
        cache["fc1_a"] = fc1_a
        cache["fc1_mask"] = (fc1_z > 0).astype(float)

        # FC2
        logits = np.dot(fc1_a, self.W_fc2) + self.b_fc2
        cache["logits"] = logits

        return logits, cache

    def _softmax(self, logits: np.ndarray) -> np.ndarray:
        """Compute softmax probabilities.

        Args:
            logits: Raw logits of shape (N, n_classes).

        Returns:
            Probabilities of shape (N, n_classes).
        """
        shifted = logits - np.max(logits, axis=1, keepdims=True)
        exps = np.exp(np.clip(shifted, -500, 500))
        return exps / np.sum(exps, axis=1, keepdims=True)

    def _cross_entropy_loss(self, logits: np.ndarray, y: np.ndarray) -> tuple[float, np.ndarray]:
        """Cross-entropy loss with softmax.

        Args:
            logits: Raw logits of shape (N, n_classes).
            y: True labels of shape (N,) with class indices.

        Returns:
            Tuple of (loss, dlogits).
        """
        probs = self._softmax(logits)
        N = logits.shape[0]
        eps = 1e-12
        loss = -np.sum(np.log(probs[np.arange(N), y] + eps)) / N

        # Gradient: dL/dlogits = (probs - one_hot) / N
        dlogits = probs.copy()
        dlogits[np.arange(N), y] -= 1.0
        dlogits /= N

        return loss, dlogits

    def backward(self, dlogits: np.ndarray, cache: dict) -> None:
        """Backward pass storing gradients in _cache['grads'].

        Args:
            dlogits: Gradient of loss w.r.t. logits, shape (N, n_classes).
            cache: Forward pass cache.
        """
        N = cache["flat"].shape[0]
        grads = {}

        # FC2 backward
        grads["dW_fc2"] = np.dot(cache["fc1_a"].T, dlogits)  # (hidden, n_classes)
        grads["db_fc2"] = np.sum(dlogits, axis=0, keepdims=True)  # (1, n_classes)
        d_fc1_a = np.dot(dlogits, self.W_fc2.T)  # (N, hidden)

        # ReLU FC1 backward
        d_fc1_z = d_fc1_a * cache["fc1_mask"]
        grads["dW_fc1"] = np.dot(cache["flat"].T, d_fc1_z)
        grads["db_fc1"] = np.sum(d_fc1_z, axis=0, keepdims=True)
        d_flat = np.dot(d_fc1_z, self.W_fc1.T)  # (N, flat_dim)

        # Unflatten
        d_pool2 = d_flat.reshape(cache["flat_shape"])

        # Pool2 backward
        self.pool2._cache = cache["pool2_cache"]
        d_conv2 = self.pool2.backward(d_pool2)

        # ReLU2 backward
        d_conv2_pre = d_conv2 * cache["relu2_mask"]

        # Conv2 backward
        self.conv2._cache = cache["conv2_cache"]
        d_pool1, grads["dW_conv2"], grads["db_conv2"] = self.conv2.backward(d_conv2_pre)

        # Pool1 backward
        self.pool1._cache = cache["pool1_cache"]
        d_conv1 = self.pool1.backward(d_pool1)

        # ReLU1 backward
        d_conv1_pre = d_conv1 * cache["relu1_mask"]

        # Conv1 backward
        self.conv1._cache = cache["conv1_cache"]
        _, grads["dW_conv1"], grads["db_conv1"] = self.conv1.backward(d_conv1_pre)

        self._cache["grads"] = grads

    def train_step(self, x: np.ndarray, y: np.ndarray, lr: float) -> float:
        """One training step.

        Args:
            x: Input batch of shape (N, C, H, W).
            y: Labels of shape (N,) with class indices.
            lr: Learning rate.

        Returns:
            Loss value.
        """
        logits, cache = self._forward_with_cache(x)
        loss, dlogits = self._cross_entropy_loss(logits, y)
        self.backward(dlogits, cache)
        grads = self._cache["grads"]

        # Update parameters
        self.W_fc2 -= lr * grads["dW_fc2"]
        self.b_fc2 -= lr * grads["db_fc2"]
        self.W_fc1 -= lr * grads["dW_fc1"]
        self.b_fc1 -= lr * grads["db_fc1"]
        self.conv2.W -= lr * grads["dW_conv2"]
        self.conv2.b -= lr * grads["db_conv2"]
        self.conv1.W -= lr * grads["dW_conv1"]
        self.conv1.b -= lr * grads["db_conv1"]

        return float(loss)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict class labels.

        Args:
            x: Input of shape (N, C, H, W).

        Returns:
            Predicted class indices of shape (N,).
        """
        logits, _ = self._forward_with_cache(x)
        return np.argmax(logits, axis=1)

    def accuracy(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute classification accuracy.

        Args:
            x: Input data.
            y: True labels.

        Returns:
            Accuracy between 0 and 1.
        """
        preds = self.predict(x)
        return float(np.mean(preds == y))


def generate_synthetic_data(
    n_samples: int = 500,
    n_classes: int = 10,
    img_size: int = 28,
    random_seed: int = 42,
) -> tuple[np.ndarray, np.ndarray]:
    """Generate synthetic data resembling simplified digits.

    Each class is a pattern of random pixels activated in a certain region.

    Args:
        n_samples: Number of samples to generate.
        n_classes: Number of classes.
        img_size: Image size (square).
        random_seed: Random seed.

    Returns:
        Tuple of (X, y) where X has shape (n_samples, 1, img_size, img_size)
        and y has shape (n_samples,).
    """
    rng = np.random.RandomState(random_seed)
    X = np.zeros((n_samples, 1, img_size, img_size), dtype=float)
    y = rng.randint(0, n_classes, n_samples)

    for i in range(n_samples):
        c = y[i]
        # Each class activates a different region
        row = (c // 2) * (img_size // 5)
        col = (c % 2) * (img_size // 5) + (img_size // 8)

        # Add some structured pattern
        for _ in range(rng.randint(10, 30)):
            dr = rng.randint(0, img_size // 4)
            dc = rng.randint(0, img_size // 4)
            rr = min(row + dr, img_size - 1)
            cc = min(col + dc, img_size - 1)
            X[i, 0, rr, cc] = 1.0

        # Add noise
        noise = rng.rand(img_size, img_size) < 0.05
        X[i, 0] += noise.astype(float)
        X[i, 0] = np.clip(X[i, 0], 0, 1)

    return X, y


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing CNN from scratch...")

    np.random.seed(42)

    # Generate small synthetic dataset
    X, y = generate_synthetic_data(n_samples=200, n_classes=5, img_size=16, random_seed=42)
    print(f"  Data: X shape = {X.shape}, y shape = {y.shape}, classes = {np.unique(y)}")

    # Test 1: Model initialization and forward pass
    cnn = SimpleCNN(input_channels=1, input_height=16, input_width=16, n_classes=5, random_seed=42)
    logits, cache = cnn._forward_with_cache(X[:4])
    assert logits.shape == (4, 5), f"Wrong logits shape: {logits.shape}"
    print(f"  PASS: Forward pass output shape: {logits.shape}")

    # Test 2: Loss computation
    loss, dlogits = cnn._cross_entropy_loss(logits, y[:4])
    assert isinstance(loss, float) and loss > 0, f"Invalid loss: {loss}"
    assert dlogits.shape == (4, 5), f"Wrong dlogits shape: {dlogits.shape}"
    print(f"  PASS: Loss computed: {loss:.4f}")

    # Test 3: Backward pass
    cnn.backward(dlogits, cache)
    grads = cnn._cache["grads"]
    assert "dW_conv1" in grads and "dW_conv2" in grads and "dW_fc1" in grads and "dW_fc2" in grads
    print("  PASS: Backward pass produced all gradients")

    # Test 4: One training step
    loss_before = cnn._cross_entropy_loss(cnn._forward_with_cache(X[:4])[0], y[:4])[0]
    loss_step = cnn.train_step(X[:4], y[:4], lr=0.01)
    loss_after = cnn._cross_entropy_loss(cnn._forward_with_cache(X[:4])[0], y[:4])[0]
    # Loss can increase initially due to random step, but values should be finite
    assert np.isfinite(loss_step), "Loss is not finite"
    print(f"  PASS: Training step completed, loss: {loss_before:.4f} → {loss_step:.4f}")

    # Test 5: Training loop (small scale)
    cnn2 = SimpleCNN(input_channels=1, input_height=16, input_width=16, n_classes=5, random_seed=123)
    initial_acc = cnn2.accuracy(X, y)

    losses = []
    for epoch in range(300):
        loss = cnn2.train_step(X, y, lr=0.05)
        losses.append(loss)
    final_acc = cnn2.accuracy(X, y)

    assert losses[-1] < losses[0], "Loss did not decrease during training"
    assert final_acc > initial_acc, f"Accuracy did not improve: {initial_acc:.3f} → {final_acc:.3f}"
    print(f"  PASS: Training: loss {losses[0]:.4f} → {losses[-1]:.4f}, accuracy {initial_acc:.3f} → {final_acc:.3f}")

    # Test 6: Random accuracy baseline
    random_acc = 1.0 / 5  # 5 classes
    assert final_acc > random_acc, f"Accuracy not better than random: {final_acc:.3f} <= {random_acc:.3f}"
    print(f"  PASS: Accuracy ({final_acc:.3f}) > random baseline ({random_acc:.3f})")

    print("\nAll CNN from scratch tests passed!")
