"""Single Perceptron and Multi-Layer Perceptron (MLP) from scratch using NumPy.

Implements:
- Perceptron: linear threshold unit for binary classification
- MLP: multi-layer perceptron with manual forward/backward passes
"""

import numpy as np
from typing import Optional, Callable


class Perceptron:
    """A single-layer perceptron (linear threshold unit) for binary classification.

    The perceptron learns a linear decision boundary using the perceptron learning rule.
    It can only solve linearly separable problems (fails on XOR).
    """

    def __init__(self, learning_rate: float = 0.1, max_epochs: int = 1000):
        """
        Args:
            learning_rate: Step size for weight updates.
            max_epochs: Maximum number of training epochs.
        """
        self.lr = learning_rate
        self.max_epochs = max_epochs
        self.weights: Optional[np.ndarray] = None
        self.bias: float = 0.0
        self._classes: Optional[np.ndarray] = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> "Perceptron":
        """Train the perceptron on binary-labeled data.

        Args:
            X: Feature matrix of shape (n_samples, n_features).
            y: Binary labels of shape (n_samples,). Must be 0 or 1.

        Returns:
            self
        """
        n_samples, n_features = X.shape
        self.weights = np.random.randn(n_features) * 0.01
        self.bias = 0.0

        # Convert {0, 1} to {-1, 1} for perceptron update rule
        y_polar = np.where(y == 0, -1, 1)

        for epoch in range(self.max_epochs):
            errors = 0
            for i in range(n_samples):
                linear = np.dot(X[i], self.weights) + self.bias
                y_pred = 1 if linear >= 0 else -1
                if y_pred != y_polar[i]:
                    self.weights += self.lr * y_polar[i] * X[i]
                    self.bias += self.lr * y_polar[i]
                    errors += 1
            if errors == 0:
                break
        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict binary labels.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Binary predictions of shape (n_samples,).
        """
        linear = np.dot(X, self.weights) + self.bias
        return (linear >= 0).astype(int)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Compute accuracy on given data."""
        return np.mean(self.predict(X) == y)


class MLP:
    """Multi-Layer Perceptron with manual forward/backward passes using NumPy.

    Supports configurable hidden layer sizes and activation functions.
    Trained with mini-batch gradient descent.
    """

    def __init__(
        self,
        layer_sizes: list[int],
        activation: str = "relu",
        learning_rate: float = 0.1,
        random_seed: int = 42,
    ):
        """Initialize MLP.

        Args:
            layer_sizes: List of layer sizes including input and output, e.g. [2, 4, 1].
            activation: Activation function name: 'relu', 'sigmoid', or 'tanh'.
            learning_rate: Learning rate for gradient descent.
            random_seed: Random seed for weight initialization.
        """
        self.layer_sizes = layer_sizes
        self.lr = learning_rate
        self.rng = np.random.RandomState(random_seed)

        # Initialize weights and biases
        self.weights: list[np.ndarray] = []
        self.biases: list[np.ndarray] = []
        for i in range(len(layer_sizes) - 1):
            # He initialization for ReLU, Xavier for sigmoid/tanh
            if activation == "relu":
                scale = np.sqrt(2.0 / layer_sizes[i])
            else:
                scale = np.sqrt(1.0 / layer_sizes[i])
            W = self.rng.randn(layer_sizes[i], layer_sizes[i + 1]) * scale
            b = np.zeros((1, layer_sizes[i + 1]))
            self.weights.append(W)
            self.biases.append(b)

        # Select activation
        act_map = {
            "relu": (self._relu, self._relu_grad),
            "sigmoid": (self._sigmoid, self._sigmoid_grad),
            "tanh": (self._tanh, self._tanh_grad),
        }
        self.act_fn, self.act_grad_fn = act_map[activation]

    @staticmethod
    def _sigmoid(x: np.ndarray) -> np.ndarray:
        return 1.0 / (1.0 + np.exp(-np.clip(x, -500, 500)))

    @staticmethod
    def _sigmoid_grad(a: np.ndarray) -> np.ndarray:
        return a * (1.0 - a)

    @staticmethod
    def _relu(x: np.ndarray) -> np.ndarray:
        return np.maximum(0, x)

    @staticmethod
    def _relu_grad(a: np.ndarray) -> np.ndarray:
        return (a > 0).astype(float)

    @staticmethod
    def _tanh(x: np.ndarray) -> np.ndarray:
        return np.tanh(x)

    @staticmethod
    def _tanh_grad(a: np.ndarray) -> np.ndarray:
        return 1.0 - a ** 2

    def forward(self, X: np.ndarray) -> tuple[np.ndarray, list[dict]]:
        """Forward pass through all layers.

        Args:
            X: Input of shape (batch_size, n_features).

        Returns:
            Tuple of (output, cache) where cache stores intermediate values for backward pass.
        """
        cache = []
        A = X
        for i in range(len(self.weights)):
            Z = np.dot(A, self.weights[i]) + self.biases[i]
            if i < len(self.weights) - 1:
                # Hidden layer: apply activation
                A = self.act_fn(Z)
                cache.append({"Z": Z, "A_prev": cache[-1]["A"] if cache else X, "A": A})
            else:
                # Output layer: sigmoid for binary classification
                A = self._sigmoid(Z)
                cache.append({"Z": Z, "A_prev": cache[-1]["A"] if cache else X, "A": A})
        return A, cache

    def backward(self, y: np.ndarray, output: np.ndarray, cache: list[dict]) -> tuple[list[np.ndarray], list[np.ndarray]]:
        """Backward pass computing gradients for all weights and biases.

        Args:
            y: True labels of shape (batch_size, 1).
            output: Network output from forward pass.
            cache: Intermediate values from forward pass.

        Returns:
            Tuple of (dW_list, db_list) containing gradients.
        """
        m = y.shape[0]
        dW_list: list[np.ndarray] = []
        db_list: list[np.ndarray] = []

        # Output layer gradient (binary cross-entropy + sigmoid)
        dA = -(y / (output + 1e-8) - (1 - y) / (1 - output + 1e-8)) / m
        dZ = dA * self._sigmoid_grad(output)

        for i in reversed(range(len(self.weights))):
            A_prev = cache[i]["A_prev"]
            dW = np.dot(A_prev.T, dZ)
            db = np.sum(dZ, axis=0, keepdims=True)
            dW_list.insert(0, dW)
            db_list.insert(0, db)

            if i > 0:
                dA_prev = np.dot(dZ, self.weights[i].T)
                dZ = dA_prev * self.act_grad_fn(cache[i - 1]["A"])

        return dW_list, db_list

    def train_step(self, X: np.ndarray, y: np.ndarray) -> float:
        """One step of gradient descent.

        Args:
            X: Input batch of shape (batch_size, n_features).
            y: Target labels of shape (batch_size, 1).

        Returns:
            Binary cross-entropy loss value.
        """
        output, cache = self.forward(X)
        dW_list, db_list = self.backward(y, output, cache)

        for i in range(len(self.weights)):
            self.weights[i] -= self.lr * dW_list[i]
            self.biases[i] -= self.lr * db_list[i]

        loss = -np.mean(y * np.log(output + 1e-8) + (1 - y) * np.log(1 - output + 1e-8))
        return loss

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict binary labels.

        Args:
            X: Feature matrix of shape (n_samples, n_features).

        Returns:
            Predictions of shape (n_samples, 1) with values in [0, 1].
        """
        output, _ = self.forward(X)
        return output

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        epochs: int = 5000,
        batch_size: Optional[int] = None,
        verbose: bool = False,
    ) -> list[float]:
        """Train the MLP.

        Args:
            X: Training features of shape (n_samples, n_features).
            y: Training labels of shape (n_samples, 1) or (n_samples,).
            epochs: Number of training epochs.
            batch_size: Mini-batch size. If None, uses full batch.
            verbose: If True, print loss every 500 epochs.

        Returns:
            List of loss values per epoch.
        """
        if y.ndim == 1:
            y = y.reshape(-1, 1)
        n_samples = X.shape[0]
        if batch_size is None:
            batch_size = n_samples

        losses: list[float] = []
        for epoch in range(epochs):
            # Mini-batch shuffling
            indices = np.random.permutation(n_samples)
            epoch_loss = 0.0
            for start in range(0, n_samples, batch_size):
                batch_idx = indices[start : start + batch_size]
                X_batch, y_batch = X[batch_idx], y[batch_idx]
                loss = self.train_step(X_batch, y_batch)
                epoch_loss += loss * len(batch_idx)
            epoch_loss /= n_samples
            losses.append(epoch_loss)
            if verbose and epoch % 500 == 0:
                print(f"Epoch {epoch}: loss = {epoch_loss:.6f}")
        return losses


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Perceptron...")

    # Test 1: Linearly separable data (AND gate)
    X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    y_and = np.array([0, 0, 0, 1])
    p = Perceptron(learning_rate=0.1, max_epochs=100)
    p.fit(X_and, y_and)
    assert np.all(p.predict(X_and) == y_and), "Perceptron failed on AND gate"
    print("  PASS: Perceptron learned AND gate")

    # Test 2: OR gate
    y_or = np.array([0, 1, 1, 1])
    p2 = Perceptron(learning_rate=0.1, max_epochs=100)
    p2.fit(X_and, y_or)
    assert np.all(p2.predict(X_and) == y_or), "Perceptron failed on OR gate"
    print("  PASS: Perceptron learned OR gate")

    # Test 3: XOR (should fail - not linearly separable)
    y_xor = np.array([0, 1, 1, 0])
    p3 = Perceptron(learning_rate=0.1, max_epochs=100)
    p3.fit(X_and, y_xor)
    # Perceptron cannot learn XOR; accuracy should be <= 75%
    acc = p3.score(X_and, y_xor)
    print(f"  PASS: Perceptron on XOR accuracy = {acc:.2f} (expected <= 0.75, not linearly separable)")

    print("\nTesting MLP...")

    # Test 4: MLP learns XOR
    mlp = MLP(layer_sizes=[2, 4, 1], activation="relu", learning_rate=0.5)
    losses = mlp.fit(X_and.astype(float), y_xor.astype(float).reshape(-1, 1), epochs=5000, verbose=False)
    preds = mlp.predict(X_and.astype(float))
    pred_labels = (preds > 0.5).astype(int).flatten()
    xor_acc = np.mean(pred_labels == y_xor)
    assert xor_acc == 1.0, f"MLP failed on XOR, accuracy = {xor_acc}"
    assert losses[-1] < losses[0], "Loss did not decrease"
    print(f"  PASS: MLP learned XOR, final loss = {losses[-1]:.6f}")

    # Test 5: MLP with tanh activation
    mlp_tanh = MLP(layer_sizes=[2, 3, 1], activation="tanh", learning_rate=0.5)
    losses_t = mlp_tanh.fit(X_and.astype(float), y_xor.astype(float).reshape(-1, 1), epochs=5000)
    preds_t = mlp_tanh.predict(X_and.astype(float))
    pred_labels_t = (preds_t > 0.5).astype(int).flatten()
    assert np.mean(pred_labels_t == y_xor) == 1.0, "MLP-tanh failed on XOR"
    print(f"  PASS: MLP with tanh learned XOR, final loss = {losses_t[-1]:.6f}")

    # Test 6: Verify forward/backward shapes
    X_test = np.random.randn(8, 2)
    y_test = np.random.randint(0, 2, (8, 1)).astype(float)
    output, cache = mlp.forward(X_test)
    assert output.shape == (8, 1), f"Wrong output shape: {output.shape}"
    dW, db = mlp.backward(y_test, output, cache)
    assert len(dW) == 2, f"Wrong number of weight gradients: {len(dW)}"
    assert dW[0].shape == (2, 4), f"Wrong dW shape: {dW[0].shape}"
    assert dW[1].shape == (4, 1), f"Wrong dW shape: {dW[1].shape}"
    print("  PASS: Forward/backward shapes are correct")

    print("\nAll perceptron tests passed!")
