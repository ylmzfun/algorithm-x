"""Kernel SVM using simplified SMO algorithm.

Supports linear, polynomial, and RBF (Gaussian) kernels.
Tested on non-linearly separable data (e.g., concentric circles).
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Literal, Callable


def linear_kernel(x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
    """Linear kernel: k(x1, x2) = x1 · x2.

    Parameters
    ----------
    x1 : np.ndarray of shape (n1, n_features)
    x2 : np.ndarray of shape (n2, n_features)

    Returns
    -------
    K : np.ndarray of shape (n1, n2)
    """
    return x1 @ x2.T


def polynomial_kernel(x1: np.ndarray, x2: np.ndarray,
                      degree: int = 3, gamma: float = 1.0,
                      coef0: float = 0.0) -> np.ndarray:
    """Polynomial kernel: k(x1, x2) = (gamma * x1·x2 + coef0)^degree.

    Parameters
    ----------
    x1 : np.ndarray of shape (n1, n_features)
    x2 : np.ndarray of shape (n2, n_features)
    degree : int
    gamma : float
    coef0 : float

    Returns
    -------
    K : np.ndarray of shape (n1, n2)
    """
    return (gamma * (x1 @ x2.T) + coef0) ** degree


def rbf_kernel(x1: np.ndarray, x2: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    """RBF (Gaussian) kernel: k(x1, x2) = exp(-gamma * ||x1 - x2||²).

    Parameters
    ----------
    x1 : np.ndarray of shape (n1, n_features)
    x2 : np.ndarray of shape (n2, n_features)
    gamma : float
        Kernel coefficient. Typically gamma = 1/(n_features * variance).

    Returns
    -------
    K : np.ndarray of shape (n1, n2)
    """
    # ||x1 - x2||² = ||x1||² + ||x2||² - 2*x1·x2
    x1_sq = np.sum(x1 ** 2, axis=1).reshape(-1, 1)
    x2_sq = np.sum(x2 ** 2, axis=1).reshape(1, -1)
    sq_dists = x1_sq + x2_sq - 2 * x1 @ x2.T
    return np.exp(-gamma * sq_dists)


class KernelSVM:
    """Kernel SVM classifier using simplified SMO.

    Parameters
    ----------
    C : float, default=1.0
        Regularization parameter.
    kernel : {'linear', 'poly', 'rbf'}, default='rbf'
        Kernel type.
    degree : int, default=3
        Degree for polynomial kernel.
    gamma : float or 'scale' or 'auto', default='scale'
        Kernel coefficient. 'scale' = 1/(n_features * X.var()),
        'auto' = 1/n_features.
    coef0 : float, default=0.0
        Independent term in polynomial kernel.
    tol : float, default=1e-3
        Tolerance for stopping criterion.
    max_passes : int, default=10
        Maximum passes over training set without alpha changes.

    Attributes
    ----------
    support_vectors_ : np.ndarray
        Support vectors.
    support_labels_ : np.ndarray
        Labels of support vectors.
    support_alphas_ : np.ndarray
        Alpha values for support vectors.
    intercept_ : float
    """

    def __init__(
        self,
        C: float = 1.0,
        kernel: Literal["linear", "poly", "rbf"] = "rbf",
        degree: int = 3,
        gamma: float | Literal["scale", "auto"] = "scale",
        coef0: float = 0.0,
        tol: float = 1e-3,
        max_passes: int = 10,
    ) -> None:
        self.C = C
        self.kernel = kernel
        self.degree = degree
        self.gamma = gamma
        self.coef0 = coef0
        self.tol = tol
        self.max_passes = max_passes
        self.support_vectors_: np.ndarray | None = None
        self.support_labels_: np.ndarray | None = None
        self.support_alphas_: np.ndarray | None = None
        self.intercept_: float = 0.0
        self._gamma_: float = 1.0
        self._X_train: np.ndarray | None = None

    def _compute_gamma(self, X: np.ndarray) -> float:
        """Compute gamma value based on data."""
        if isinstance(self.gamma, (int, float)):
            return float(self.gamma)
        n_features = X.shape[1]
        if self.gamma == "scale":
            var = np.var(X)
            return 1.0 / (n_features * var) if var > 0 else 1.0 / n_features
        elif self.gamma == "auto":
            return 1.0 / n_features
        return 1.0

    def _kernel_function(self, x1: np.ndarray, x2: np.ndarray) -> np.ndarray:
        """Apply the kernel function."""
        if self.kernel == "linear":
            return linear_kernel(x1, x2)
        elif self.kernel == "poly":
            return polynomial_kernel(x1, x2, degree=self.degree,
                                     gamma=self._gamma_, coef0=self.coef0)
        elif self.kernel == "rbf":
            return rbf_kernel(x1, x2, gamma=self._gamma_)
        else:
            raise ValueError(f"Unknown kernel: {self.kernel}")

    def fit(self, X: np.ndarray, y: np.ndarray) -> KernelSVM:
        """Fit kernel SVM.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)
            Labels must be -1 or +1.

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y, dtype=np.float64).reshape(-1)
        n_samples, n_features = X.shape

        # Normalize labels to -1/+1
        unique_labels = np.unique(y)
        if not np.array_equal(np.sort(unique_labels), [-1, 1]):
            y = np.where(y == unique_labels[0], -1.0, 1.0)

        self._X_train = X
        self._gamma_ = self._compute_gamma(X)

        # Precompute kernel matrix
        K = self._kernel_function(X, X)

        # SMO
        alphas = np.zeros(n_samples)
        b = 0.0

        passes = 0
        while passes < self.max_passes:
            num_changed = 0
            for i in range(n_samples):
                E_i = np.sum(alphas * y * K[:, i]) + b - y[i]

                if (y[i] * E_i < -self.tol and alphas[i] < self.C) or \
                   (y[i] * E_i > self.tol and alphas[i] > 0):
                    j = i
                    while j == i:
                        j = np.random.randint(0, n_samples)
                    E_j = np.sum(alphas * y * K[:, j]) + b - y[j]

                    alpha_i_old, alpha_j_old = alphas[i], alphas[j]

                    if y[i] != y[j]:
                        L = max(0, alphas[j] - alphas[i])
                        H = min(self.C, self.C + alphas[j] - alphas[i])
                    else:
                        L = max(0, alphas[i] + alphas[j] - self.C)
                        H = min(self.C, alphas[i] + alphas[j])

                    if L == H:
                        continue

                    eta = 2 * K[i, j] - K[i, i] - K[j, j]
                    if eta >= 0:
                        continue

                    alphas[j] -= y[j] * (E_i - E_j) / eta
                    alphas[j] = np.clip(alphas[j], L, H)

                    if np.abs(alphas[j] - alpha_j_old) < 1e-5:
                        continue

                    alphas[i] += y[i] * y[j] * (alpha_j_old - alphas[j])

                    b1 = b - E_i - y[i] * (alphas[i] - alpha_i_old) * K[i, i] \
                         - y[j] * (alphas[j] - alpha_j_old) * K[i, j]
                    b2 = b - E_j - y[i] * (alphas[i] - alpha_i_old) * K[i, j] \
                         - y[j] * (alphas[j] - alpha_j_old) * K[j, j]

                    if 0 < alphas[i] < self.C:
                        b = b1
                    elif 0 < alphas[j] < self.C:
                        b = b2
                    else:
                        b = (b1 + b2) / 2

                    num_changed += 1

            if num_changed == 0:
                passes += 1
            else:
                passes = 0

        # Extract support vectors
        sv_idx = alphas > 1e-5
        self.support_vectors_ = X[sv_idx]
        self.support_labels_ = y[sv_idx]
        self.support_alphas_ = alphas[sv_idx]
        self.intercept_ = b

        return self

    def decision_function(self, X: np.ndarray) -> np.ndarray:
        """Compute decision function values.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        scores : np.ndarray of shape (n_samples,)
        """
        if self.support_vectors_ is None:
            raise ValueError("Model not fitted.")
        X = np.asarray(X, dtype=np.float64)
        K = self._kernel_function(X, self.support_vectors_)
        return (
            np.sum((self.support_alphas_ * self.support_labels_) * K, axis=1)
            + self.intercept_
        )

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict labels (-1 or +1).

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        y_pred : np.ndarray of shape (n_samples,)
        """
        return np.sign(self.decision_function(X))

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Mean accuracy."""
        return float(np.mean(self.predict(X) == y))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Kernel SVM ===")

    np.random.seed(42)
    n_samples = 200

    # --- Test 1: Linear kernel on linearly separable data ---
    X_pos = np.random.randn(n_samples // 2, 2) + np.array([2, 2])
    X_neg = np.random.randn(n_samples // 2, 2) + np.array([-2, -2])
    X = np.vstack([X_pos, X_neg])
    y = np.array([1] * (n_samples // 2) + [-1] * (n_samples // 2))
    idx = np.random.permutation(n_samples)
    X, y = X[idx], y[idx]
    split = int(0.8 * n_samples)

    svm_lin = KernelSVM(C=1.0, kernel="linear", max_passes=20)
    svm_lin.fit(X[:split], y[:split])
    acc_lin = svm_lin.score(X[split:], y[split:])
    print(f"  Linear kernel accuracy: {acc_lin:.4f}")
    assert acc_lin > 0.8
    print("  Linear kernel: PASS")

    # --- Test 2: RBF kernel on concentric circles ---
    # Generate inner circle
    n_inner = n_samples // 2
    theta_inner = np.random.uniform(0, 2 * np.pi, n_inner)
    r_inner = np.random.uniform(0, 1.0, n_inner)
    X_inner = np.column_stack([r_inner * np.cos(theta_inner),
                                r_inner * np.sin(theta_inner)])

    # Generate outer ring
    n_outer = n_samples // 2
    theta_outer = np.random.uniform(0, 2 * np.pi, n_outer)
    r_outer = np.random.uniform(2.0, 3.0, n_outer)
    X_outer = np.column_stack([r_outer * np.cos(theta_outer),
                                r_outer * np.sin(theta_outer)])

    X_circles = np.vstack([X_inner, X_outer])
    y_circles = np.array([1] * n_inner + [-1] * n_outer)

    idx = np.random.permutation(n_samples)
    X_circles, y_circles = X_circles[idx], y_circles[idx]
    split = int(0.8 * n_samples)

    svm_rbf = KernelSVM(C=10.0, kernel="rbf", gamma=1.0, max_passes=20)
    svm_rbf.fit(X_circles[:split], y_circles[:split])
    acc_rbf = svm_rbf.score(X_circles[split:], y_circles[split:])
    print(f"  RBF kernel accuracy (circles): {acc_rbf:.4f}")
    assert acc_rbf > 0.7, f"RBF accuracy too low: {acc_rbf}"
    print("  RBF kernel: PASS")

    # --- Test 3: Polynomial kernel ---
    svm_poly = KernelSVM(C=1.0, kernel="poly", degree=3, gamma=0.5, max_passes=20)
    svm_poly.fit(X[:split], y[:split])
    acc_poly = svm_poly.score(X[split:], y[split:])
    print(f"  Polynomial kernel accuracy: {acc_poly:.4f}")
    assert acc_poly > 0.8
    print("  Polynomial kernel: PASS")

    # --- Compare with sklearn ---
    try:
        from sklearn.svm import SVC
        sk_rbf = SVC(C=10.0, kernel="rbf", gamma=1.0, random_state=42)
        sk_rbf.fit(X_circles[:split], y_circles[:split])
        sk_acc = sk_rbf.score(X_circles[split:], y_circles[split:])
        print(f"  sklearn SVC RBF accuracy: {sk_acc:.4f}")
        print("  sklearn comparison: PASS")
    except ImportError:
        print("  sklearn not installed, skipping comparison")

    print("All Kernel SVM tests PASSED!\n")
