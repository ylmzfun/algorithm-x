"""Regularization techniques: L1/L2, early stopping, label smoothing, data augmentation.

All implemented with NumPy.
"""

import numpy as np
from typing import Optional
import copy


def l1_regularization(weights: np.ndarray, lambda_l1: float) -> float:
    """Compute L1 regularization penalty: λ * sum(|w|).

    Args:
        weights: Weight array.
        lambda_l1: L1 regularization strength.

    Returns:
        L1 penalty (scalar).
    """
    return lambda_l1 * np.sum(np.abs(weights))


def l1_gradient(weights: np.ndarray, lambda_l1: float) -> np.ndarray:
    """Gradient of L1 regularization w.r.t. weights: λ * sign(w).

    Args:
        weights: Weight array.
        lambda_l1: L1 regularization strength.

    Returns:
        Gradient array of same shape as weights.
    """
    return lambda_l1 * np.sign(weights)


def l2_regularization(weights: np.ndarray, lambda_l2: float) -> float:
    """Compute L2 regularization penalty: λ * sum(w^2).

    Args:
        weights: Weight array.
        lambda_l2: L2 regularization strength.

    Returns:
        L2 penalty (scalar).
    """
    return lambda_l2 * np.sum(weights ** 2)


def l2_gradient(weights: np.ndarray, lambda_l2: float) -> np.ndarray:
    """Gradient of L2 regularization w.r.t. weights: 2 * λ * w.

    Args:
        weights: Weight array.
        lambda_l2: L2 regularization strength.

    Returns:
        Gradient array of same shape as weights.
    """
    return 2 * lambda_l2 * weights


class EarlyStopping:
    """Early stopping with model checkpointing.

    Monitors validation loss and stops training when no improvement
    is observed for `patience` epochs.
    """

    def __init__(self, patience: int = 10, min_delta: float = 0.0):
        """Initialize EarlyStopping.

        Args:
            patience: Number of epochs to wait before stopping.
            min_delta: Minimum improvement to count as progress.
        """
        self.patience = patience
        self.min_delta = min_delta
        self.best_loss: float = float("inf")
        self.best_epoch: int = 0
        self.counter: int = 0
        self.should_stop: bool = False
        self.best_weights: Optional[dict] = None

    def step(self, val_loss: float, model_weights: Optional[dict] = None) -> bool:
        """Check if training should stop.

        Args:
            val_loss: Current validation loss.
            model_weights: Current model weights to checkpoint.

        Returns:
            True if training should stop.
        """
        if val_loss < self.best_loss - self.min_delta:
            self.best_loss = val_loss
            self.counter = 0
            if model_weights is not None:
                self.best_weights = copy.deepcopy(model_weights)
        else:
            self.counter += 1

        self.should_stop = self.counter >= self.patience
        return self.should_stop

    def restore_best(self, model_weights: dict) -> None:
        """Restore best weights into model_weights dict.

        Args:
            model_weights: Dict to restore weights into (modified in place).
        """
        if self.best_weights is not None:
            for key in model_weights:
                if key in self.best_weights:
                    model_weights[key] = self.best_weights[key].copy()


def label_smoothing(
    y_true: np.ndarray,
    num_classes: int,
    epsilon: float = 0.1,
) -> np.ndarray:
    """Apply label smoothing to one-hot labels.

    y_smoothed = (1 - ε) * y_one_hot + ε / num_classes

    Args:
        y_true: Class indices of shape (batch_size,) or one-hot of shape (batch_size, num_classes).
        num_classes: Number of classes.
        epsilon: Smoothing factor (0 = no smoothing, 1 = uniform).

    Returns:
        Smoothed labels of shape (batch_size, num_classes).
    """
    if y_true.ndim == 1:
        y_one_hot = np.eye(num_classes)[y_true]
    else:
        y_one_hot = y_true.astype(float)

    return (1 - epsilon) * y_one_hot + epsilon / num_classes


def data_augmentation_demo(
    X: np.ndarray,
    y: np.ndarray,
    augment_prob: float = 0.5,
    random_seed: Optional[int] = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Demonstrate simple data augmentations: flip, shift, add noise.

    Assumes X is image data of shape (N, C, H, W) or (N, H, W).

    Args:
        X: Input data.
        y: Labels.
        augment_prob: Probability of applying each augmentation.
        random_seed: Random seed.

    Returns:
        Tuple of (augmented_X, y).
    """
    rng = np.random.RandomState(random_seed)
    X_aug = X.copy()
    is_image_4d = X.ndim == 4

    for i in range(len(X)):
        if is_image_4d:
            img = X_aug[i]  # (C, H, W)
            # Horizontal flip
            if rng.rand() < augment_prob:
                img = img[:, :, ::-1]
            # Vertical shift
            if rng.rand() < augment_prob:
                shift = rng.randint(-2, 3)
                img = np.roll(img, shift, axis=1)
            # Add noise
            if rng.rand() < augment_prob:
                noise = rng.randn(*img.shape) * 0.05
                img = img + noise
            X_aug[i] = img
        else:
            row = X_aug[i]
            # Add noise
            if rng.rand() < augment_prob:
                noise = rng.randn(*row.shape) * 0.05
                row = row + noise
            X_aug[i] = row

    return X_aug, y


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Regularization Techniques...")

    np.random.seed(42)

    # Test 1: L1 regularization
    w = np.array([1.0, -2.0, 0.5, -0.3])
    l1_val = l1_regularization(w, lambda_l1=0.1)
    expected_l1 = 0.1 * (1.0 + 2.0 + 0.5 + 0.3)
    assert np.isclose(l1_val, expected_l1, atol=1e-6), f"L1: {l1_val} != {expected_l1}"
    print(f"  PASS: L1 penalty = {l1_val:.4f}")

    # Test 2: L1 gradient
    l1_grad = l1_gradient(w, lambda_l1=0.1)
    expected_grad = 0.1 * np.array([1.0, -1.0, 1.0, -1.0])
    assert np.allclose(l1_grad, expected_grad)
    print("  PASS: L1 gradient correct")

    # Test 3: L2 regularization
    l2_val = l2_regularization(w, lambda_l2=0.1)
    expected_l2 = 0.1 * (1.0 + 4.0 + 0.25 + 0.09)
    assert np.isclose(l2_val, expected_l2, atol=1e-6)
    print(f"  PASS: L2 penalty = {l2_val:.4f}")

    # Test 4: Early stopping
    es = EarlyStopping(patience=3, min_delta=0.01)
    losses = [1.0, 0.8, 0.6, 0.55, 0.56, 0.57, 0.58]
    stop_epoch = None
    for i, loss in enumerate(losses):
        weights = {"w": np.array([float(i)])}
        if es.step(loss, weights):
            stop_epoch = i
            break
    assert stop_epoch == 6, f"Should stop at epoch 6, got {stop_epoch}"
    assert np.isclose(es.best_loss, 0.55, atol=1e-6), f"Best loss should be 0.55, got {es.best_loss}"
    print(f"  PASS: Early stopping at epoch {stop_epoch}, best loss = {es.best_loss}")

    # Test 5: Early stopping weight restoration
    current_weights = {"w": np.array([99.0])}
    es_restore = EarlyStopping(patience=2)
    es_restore.step(0.5, {"w": np.array([0.5])})
    es_restore.step(0.7, {"w": np.array([0.7])})
    es_restore.step(0.8, {"w": np.array([0.8])})
    es_restore.restore_best(current_weights)
    assert np.isclose(current_weights["w"], 0.5), f"Should restore to 0.5, got {current_weights['w']}"
    print("  PASS: Early stopping restores best weights")

    # Test 6: Label smoothing
    y_true = np.array([0, 1, 2])
    y_smooth = label_smoothing(y_true, num_classes=3, epsilon=0.1)
    assert y_smooth.shape == (3, 3), f"Wrong shape: {y_smooth.shape}"
    assert np.allclose(y_smooth.sum(axis=1), 1.0), "Rows should sum to 1"
    # For class 0: (1-0.1)*1 + 0.1/3 = 0.9333..., others = 0.0333...
    assert np.isclose(y_smooth[0, 0], 0.9 + 0.1/3, atol=1e-6)
    assert np.isclose(y_smooth[0, 1], 0.1/3, atol=1e-6)
    print("  PASS: Label smoothing produces correct values")

    # Test 7: Label smoothing with one-hot input
    y_one_hot = np.eye(4)
    y_smooth_oh = label_smoothing(y_one_hot, num_classes=4, epsilon=0.0)
    assert np.allclose(y_smooth_oh, y_one_hot), "ε=0 should be identity"
    print("  PASS: Label smoothing with ε=0 is identity")

    # Test 8: Data augmentation
    X_img = np.random.rand(10, 3, 16, 16)
    y_img = np.arange(10)
    X_aug, y_aug = data_augmentation_demo(X_img, y_img, augment_prob=1.0, random_seed=42)
    assert X_aug.shape == X_img.shape, "Augmentation should preserve shape"
    assert y_aug is y_img, "Labels should be unchanged"
    # Some pixels should have changed
    assert not np.allclose(X_aug[0], X_img[0]), "Augmentation should change data"
    print(f"  PASS: Data augmentation preserves shape: {X_aug.shape}")

    # Test 9: Data augmentation with 2D input
    X_2d = np.random.randn(20, 10)
    X_2d_aug, _ = data_augmentation_demo(X_2d, np.arange(20), augment_prob=1.0, random_seed=42)
    assert X_2d_aug.shape == (20, 10)
    print(f"  PASS: Data aug works on 2D data: {X_2d_aug.shape}")

    print("\nAll Regularization tests passed!")
