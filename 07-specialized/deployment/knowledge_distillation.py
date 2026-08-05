"""Knowledge Distillation from scratch using NumPy.

Implements teacher-student distillation:
- Train a larger teacher model on a classification task
- Distill knowledge to a smaller student using soft targets
- Compare student performance with and without distillation

The key idea: use the teacher's soft predictions (with temperature)
as additional training signal for the student, transferring dark knowledge.

Reference: Hinton et al., "Distilling the Knowledge in a Neural Network" (2015).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Base network
# ---------------------------------------------------------------------------

class NeuralNetwork:
    """Simple feed-forward neural network for classification.

    Attributes:
        layers: List of (W, b) tuples.
    """

    def __init__(
        self,
        layer_dims: list[int],
        seed: int = 42,
    ) -> None:
        """Initialize the network.

        Args:
            layer_dims: List of dimensions [input, hidden..., output].
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.layer_dims = layer_dims
        self.layers: list[tuple[np.ndarray, np.ndarray]] = []

        for i in range(len(layer_dims) - 1):
            fan_in = layer_dims[i]
            fan_out = layer_dims[i + 1]
            scale = np.sqrt(2.0 / fan_in)
            W = rng.normal(0, scale, (fan_in, fan_out))
            b = np.zeros(fan_out)
            self.layers.append((W, b))

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass (logits).

        Args:
            x: Input [B, input_dim].

        Returns:
            Logits [B, output_dim].
        """
        out = x
        for i, (W, b) in enumerate(self.layers):
            out = out @ W + b
            if i < len(self.layers) - 1:
                out = np.maximum(0, out)  # ReLU
        return out

    def predict_proba(self, x: np.ndarray, temperature: float = 1.0) -> np.ndarray:
        """Softmax probabilities with optional temperature.

        Args:
            x: Input.
            temperature: Temperature for softening (T=1 = standard softmax).

        Returns:
            Class probabilities.
        """
        logits = self.forward(x) / temperature
        return _softmax(logits)

    def predict(self, x: np.ndarray) -> np.ndarray:
        """Predict class labels.

        Args:
            x: Input.

        Returns:
            Predicted class indices [B].
        """
        probs = self.predict_proba(x)
        return np.argmax(probs, axis=-1)

    def get_params(self) -> np.ndarray:
        """Get all parameters as flat array."""
        parts = [W.ravel() for W, _ in self.layers] + [b.ravel() for _, b in self.layers]
        return np.concatenate(parts)

    def set_params(self, flat: np.ndarray) -> None:
        """Set all parameters from flat array."""
        offset = 0
        for W, _ in self.layers:
            s = W.size
            W.ravel()[:] = flat[offset:offset + s]
            offset += s
        for _, b in self.layers:
            s = b.size
            b.ravel()[:] = flat[offset:offset + s]
            offset += s


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / np.sum(e, axis=-1, keepdims=True)


def _cross_entropy(logits: np.ndarray, labels: np.ndarray) -> float:
    probs = _softmax(logits)
    n = len(labels)
    return float(-np.sum(np.log(probs[np.arange(n), labels] + 1e-12)) / n)


# ---------------------------------------------------------------------------
# Teacher and Student
# ---------------------------------------------------------------------------

class TeacherModel(NeuralNetwork):
    """Larger teacher model (3-4 layers)."""

    def __init__(self, input_dim: int, num_classes: int, seed: int = 42) -> None:
        dims = [input_dim, 64, 32, num_classes]
        super().__init__(dims, seed=seed)


class StudentModel(NeuralNetwork):
    """Smaller student model (1-2 layers)."""

    def __init__(self, input_dim: int, num_classes: int, seed: int = 42) -> None:
        dims = [input_dim, 16, num_classes]
        super().__init__(dims, seed=seed)


# ---------------------------------------------------------------------------
# Softmax with temperature
# ---------------------------------------------------------------------------

def softmax_with_temperature(
    logits: np.ndarray, temperature: float = 1.0
) -> np.ndarray:
    """Softmax with temperature scaling.

    p_i = exp(z_i / T) / Σ_j exp(z_j / T)

    Higher T → softer probability distribution.

    Args:
        logits: Model logits [B, C].
        temperature: Temperature parameter (T > 0).

    Returns:
        Softmax probabilities.
    """
    return _softmax(logits / max(temperature, 1e-8))


# ---------------------------------------------------------------------------
# Distillation Loss
# ---------------------------------------------------------------------------

def distillation_loss(
    student_logits: np.ndarray,
    teacher_logits: np.ndarray,
    temperature: float = 3.0,
    alpha: float = 0.7,
    true_labels: np.ndarray = None,
) -> float:
    r"""Compute the distillation loss.

    L = α * L_hard + (1 - α) * L_soft

    L_hard = cross-entropy with true labels
    L_soft = KL(teacher_soft || student_soft) * T²

    The T² scaling is needed because gradients are scaled by 1/T²
    when using temperature.

    Args:
        student_logits: Student model logits [B, C].
        teacher_logits: Teacher model logits [B, C].
        temperature: Softmax temperature.
        alpha: Weight for hard loss (1-alpha for soft loss).
        true_labels: True class labels [B].

    Returns:
        Total distillation loss.
    """
    # Soft targets
    teacher_soft = softmax_with_temperature(teacher_logits, temperature)
    student_soft = softmax_with_temperature(student_logits, temperature)

    # KL divergence: Σ_i t_i * log(t_i / s_i)
    soft_loss = -np.sum(
        teacher_soft * np.log(student_soft + 1e-12)
    ) / student_logits.shape[0]
    # Scale by T² to keep gradient magnitude consistent
    soft_loss *= temperature ** 2

    # Hard loss
    hard_loss = 0.0
    if true_labels is not None and alpha > 0:
        hard_loss = _cross_entropy(student_logits, true_labels)

    return alpha * hard_loss + (1 - alpha) * soft_loss


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_model(
    model: NeuralNetwork,
    X: np.ndarray,
    y: np.ndarray,
    epochs: int = 100,
    lr: float = 0.01,
) -> list[float]:
    """Train a model using cross-entropy loss and finite-difference SGD.

    Args:
        model: Neural network to train.
        X: Training data [N, D].
        y: Labels [N].
        epochs: Number of epochs.
        lr: Learning rate.

    Returns:
        List of losses per epoch.
    """
    n = X.shape[0]
    losses: list[float] = []

    for epoch in range(epochs):
        logits = model.forward(X)
        loss = _cross_entropy(logits, y)
        losses.append(loss)

        # SGD via finite differences
        eps = 1e-4
        params = model.get_params()
        grad = np.zeros_like(params)
        subset = np.random.choice(len(params), min(30, len(params)), replace=False)

        for idx in subset:
            orig = params[idx]
            params[idx] = orig + eps
            model.set_params(params)
            l_plus = _cross_entropy(model.forward(X), y)
            params[idx] = orig - eps
            model.set_params(params)
            l_minus = _cross_entropy(model.forward(X), y)
            params[idx] = orig
            grad[idx] = (l_plus - l_minus) / (2 * eps)

        params -= lr * grad
        model.set_params(params)

    return losses


def train_distillation(
    teacher: TeacherModel,
    student: StudentModel,
    X: np.ndarray,
    y: np.ndarray,
    temperature: float = 3.0,
    alpha: float = 0.7,
    epochs: int = 100,
    lr: float = 0.01,
) -> list[float]:
    """Train student via knowledge distillation.

    Args:
        teacher: Pre-trained teacher model.
        student: Student model to train.
        X: Training data [N, D].
        y: Labels [N].
        temperature: Softmax temperature.
        alpha: Weight for hard loss.
        epochs: Number of epochs.
        lr: Learning rate.

    Returns:
        List of distillation losses per epoch.
    """
    teacher_logits = teacher.forward(X)

    losses: list[float] = []
    for epoch in range(epochs):
        student_logits = student.forward(X)
        loss = distillation_loss(
            student_logits, teacher_logits, temperature, alpha, y
        )
        losses.append(loss)

        # SGD
        eps = 1e-4
        params = student.get_params()
        grad = np.zeros_like(params)
        subset = np.random.choice(len(params), min(30, len(params)), replace=False)

        for idx in subset:
            orig = params[idx]
            params[idx] = orig + eps
            student.set_params(params)
            l_plus = distillation_loss(
                student.forward(X), teacher_logits, temperature, alpha, y
            )
            params[idx] = orig - eps
            student.set_params(params)
            l_minus = distillation_loss(
                student.forward(X), teacher_logits, temperature, alpha, y
            )
            params[idx] = orig
            grad[idx] = (l_plus - l_minus) / (2 * eps)

        params -= lr * grad
        student.set_params(params)

    return losses


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing knowledge_distillation.py — Knowledge Distillation")
    print("=" * 60)

    np.random.seed(42)

    # Create synthetic classification data
    n_samples = 300
    n_features = 10
    n_classes = 4

    # Generate clusters
    X = np.zeros((n_samples, n_features))
    y = np.zeros(n_samples, dtype=np.int64)
    centers = np.random.randn(n_classes, n_features) * 2
    for i in range(n_samples):
        c = i % n_classes
        X[i] = centers[c] + np.random.randn(n_features) * 0.5
        y[i] = c

    split = int(0.7 * n_samples)
    X_train, y_train = X[:split], y[:split]
    X_test, y_test = X[split:], y[split:]

    print(f"\nData: {n_samples} samples, {n_features} features, "
          f"{n_classes} classes")

    all_pass = True

    # Train teacher
    print("\n--- Teacher Training ---")
    teacher = TeacherModel(n_features, n_classes, seed=42)
    teacher_losses = train_model(teacher, X_train, y_train, epochs=80, lr=0.03)
    teacher_acc = np.mean(teacher.predict(X_test) == y_test)
    print(f"  Teacher test accuracy: {teacher_acc:.2%}")
    print(f"  Teacher final loss: {teacher_losses[-1]:.4f}")
    all_pass = all_pass and teacher_acc > 0.5

    # Train student WITHOUT distillation
    print("\n--- Student WITHOUT Distillation ---")
    student_no_distill = StudentModel(n_features, n_classes, seed=99)
    snd_losses = train_model(student_no_distill, X_train, y_train,
                              epochs=80, lr=0.03)
    snd_acc = np.mean(student_no_distill.predict(X_test) == y_test)
    print(f"  Student (no distill) test accuracy: {snd_acc:.2%}")

    # Train student WITH distillation
    print("\n--- Student WITH Distillation ---")
    student_distill = StudentModel(n_features, n_classes, seed=99)  # Same seed
    sd_losses = train_distillation(
        teacher, student_distill, X_train, y_train,
        temperature=3.0, alpha=0.5, epochs=80, lr=0.03,
    )
    sd_acc = np.mean(student_distill.predict(X_test) == y_test)
    print(f"  Student (distilled) test accuracy: {sd_acc:.2%}")

    # Compare: distillation should help (or at least not hurt much)
    distill_helps = sd_acc >= snd_acc
    print(f"\n  Distillation helps: {distill_helps}")
    all_pass = all_pass and distill_helps

    # Test temperature softmax
    print("\n--- Temperature Softmax ---")
    logits = np.array([[2.0, 1.0, 0.5, -1.0]])

    probs_t1 = softmax_with_temperature(logits, temperature=1.0)
    probs_t5 = softmax_with_temperature(logits, temperature=5.0)
    probs_t01 = softmax_with_temperature(logits, temperature=0.1)

    print(f"  T=1.0:    {probs_t1[0]}")
    print(f"  T=5.0:    {probs_t5[0]}")
    print(f"  T=0.1:    {probs_t01[0]}")

    # Higher temp should be more uniform (lower max, higher min)
    t5_softer = np.max(probs_t5) < np.max(probs_t1)
    t01_sharper = np.max(probs_t01) > np.max(probs_t1)
    print(f"  T=5 softer than T=1: {t5_softer}")
    print(f"  T=0.1 sharper than T=1: {t01_sharper}")
    all_pass = all_pass and t5_softer and t01_sharper

    print(f"\n{'PASS' if all_pass else 'FAIL'}: knowledge_distillation.py")
