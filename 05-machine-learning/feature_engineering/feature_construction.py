"""Feature Construction methods from scratch.

Includes:
- Polynomial features (degree-2 interactions)
- Interaction features
- Binning / discretization
- Log transform
- Box-Cox power transform
"""

from __future__ import annotations

import numpy as np
from typing import Optional


class PolynomialFeatures:
    """Generate polynomial and interaction features.

    Generates a new feature matrix consisting of all polynomial combinations
    of the features with degree less than or equal to the specified degree.

    For degree=2: [1, x1, x2, x1², x1·x2, x2²]

    Parameters
    ----------
    degree : int, default=2
        Degree of polynomial features.
    include_bias : bool, default=True
        If True, include a bias column (all ones).
    interaction_only : bool, default=False
        If True, only interaction features (no x_i² terms).

    Attributes
    ----------
    powers_ : np.ndarray of shape (n_output_features, n_input_features)
        Powers of each input feature for each output feature.
    """

    def __init__(
        self,
        degree: int = 2,
        include_bias: bool = True,
        interaction_only: bool = False,
    ) -> None:
        self.degree = degree
        self.include_bias = include_bias
        self.interaction_only = interaction_only
        self.powers_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> PolynomialFeatures:
        """Compute output feature powers.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : ignored

        Returns
        -------
        self
        """
        n_features = X.shape[1]
        # Generate all combinations of powers summing to <= degree
        combinations = self._generate_powers(n_features, self.degree,
                                              self.interaction_only,
                                              self.include_bias)
        self.powers_ = np.array(combinations)
        return self

    def _generate_powers(self, n_features: int, degree: int,
                         interaction_only: bool,
                         include_bias: bool) -> list:
        """Generate combinations of exponents for each monomial."""
        combos = []

        # For each output feature index
        def _recurse(idx, remaining_degree, current, non_zero_count):
            if idx == n_features:
                if remaining_degree == 0:
                    if not interaction_only or non_zero_count <= 1:
                        combos.append(list(current))
                return

            max_power = min(remaining_degree, degree)
            start = 0 if remaining_degree < degree else 0
            # For degree > 0
            for p in range(max_power + 1):
                if interaction_only and non_zero_count == 1 and p > 0:
                    continue
                new_non_zero = non_zero_count + (1 if p > 0 else 0)
                if interaction_only and new_non_zero > 1:
                    continue
                _recurse(idx + 1, remaining_degree - p, current + [p], new_non_zero)

        if include_bias:
            combos.append([0] * n_features)
        for d in range(1, degree + 1):
            _recurse(0, d, [], 0)
        return combos

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform X to polynomial features.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        XP : np.ndarray of shape (n_samples, n_output_features)
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples = X.shape[0]
        n_output = self.powers_.shape[0]
        XP = np.ones((n_samples, n_output))

        for i in range(n_output):
            for j in range(X.shape[1]):
                XP[:, i] *= X[:, j] ** self.powers_[i, j]

        return XP

    def fit_transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)


class InteractionFeatures:
    """Generate pairwise interaction features.

    For n original features, adds n*(n-1)/2 interaction features
    of the form x_i * x_j for i < j.

    Parameters
    ----------
    include_bias : bool, default=False
    """

    def __init__(self, include_bias: bool = False) -> None:
        self.include_bias = include_bias
        self._pairs: list[tuple[int, int]] = []

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> InteractionFeatures:
        """Find interaction pairs.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        n_features = X.shape[1]
        self._pairs = [(i, j) for i in range(n_features) for j in range(i + 1, n_features)]
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Generate interaction features.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_int : np.ndarray of shape (n_samples, n_features + n_pairs)
        """
        X = np.asarray(X, dtype=np.float64)
        interactions = np.column_stack([X[:, i] * X[:, j] for i, j in self._pairs])
        return np.column_stack([X, interactions])

    def fit_transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)


class BinningDiscretizer:
    """Bin continuous features into discrete intervals.

    Parameters
    ----------
    n_bins : int, default=5
        Number of bins.
    strategy : {'uniform', 'quantile'}, default='uniform'
        Binning strategy.
    encode : {'onehot', 'ordinal'}, default='ordinal'
        How to encode bins.

    Attributes
    ----------
    bin_edges_ : list of np.ndarray
        Edges for each feature's bins.
    """

    def __init__(
        self,
        n_bins: int = 5,
        strategy: str = "uniform",
        encode: str = "ordinal",
    ) -> None:
        self.n_bins = n_bins
        self.strategy = strategy
        self.encode = encode
        self.bin_edges_: list[np.ndarray] = []

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> BinningDiscretizer:
        """Compute bin edges.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        n_features = X.shape[1]
        self.bin_edges_ = []

        for f in range(n_features):
            col = X[:, f]
            if self.strategy == "uniform":
                edges = np.linspace(np.min(col), np.max(col), self.n_bins + 1)
            elif self.strategy == "quantile":
                edges = np.percentile(col, np.linspace(0, 100, self.n_bins + 1))
            else:
                raise ValueError(f"Unknown strategy: {self.strategy}")
            # Make edges strict to avoid duplicates
            edges = np.unique(edges)
            self.bin_edges_.append(edges)

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Bin X.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_binned : np.ndarray
        """
        X = np.asarray(X, dtype=np.float64)
        n_samples, n_features = X.shape

        if self.encode == "ordinal":
            result = np.zeros((n_samples, n_features), dtype=np.float64)
            for f in range(n_features):
                result[:, f] = np.digitize(X[:, f], self.bin_edges_[f][1:-1])
            return result
        elif self.encode == "onehot":
            parts = []
            for f in range(n_features):
                edges = self.bin_edges_[f]
                n_bins_actual = len(edges) - 1
                col_binned = np.digitize(X[:, f], edges[1:-1])
                oh = np.eye(n_bins_actual)[col_binned]
                parts.append(oh)
            return np.column_stack(parts)
        else:
            raise ValueError(f"Unknown encoding: {self.encode}")

    def fit_transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)


def log_transform(X: np.ndarray, epsilon: float = 1e-10) -> np.ndarray:
    """Apply log(1 + x) transform to make data more Gaussian-like.

    Parameters
    ----------
    X : np.ndarray
    epsilon : float
        Small constant to avoid log(0).

    Returns
    -------
    X_trans : np.ndarray
    """
    X = np.asarray(X, dtype=np.float64)
    # Shift to ensure positive
    X_min = np.min(X, axis=0)
    if np.any(X_min < 0):
        X = X - X_min + epsilon
    return np.log1p(X)


def box_cox_transform(X: np.ndarray, lam: float) -> np.ndarray:
    """Apply Box-Cox power transform.

    y = (x^λ - 1) / λ  if λ ≠ 0
    y = log(x)         if λ = 0

    Parameters
    ----------
    X : np.ndarray of shape (n_samples, n_features)
        Must be strictly positive.
    lam : float
        Lambda parameter.

    Returns
    -------
    X_trans : np.ndarray
    """
    X = np.asarray(X, dtype=np.float64)
    if np.any(X <= 0):
        raise ValueError("Box-Cox requires strictly positive data.")

    if np.abs(lam) < 1e-10:
        return np.log(X)
    else:
        return (X ** lam - 1) / lam


def estimate_box_cox_lambda(X: np.ndarray) -> float:
    """Estimate optimal lambda for Box-Cox via simple method.

    Tries a range of lambda values and picks the one that
    maximizes log-likelihood (simplified).

    Parameters
    ----------
    X : np.ndarray of shape (n_samples, n_features)

    Returns
    -------
    lam : float
    """
    X = np.asarray(X, dtype=np.float64)
    # Use single feature's lambda as proxy (average)
    lambdas = []
    for f in range(X.shape[1]):
        # Try a range
        best_lam = 0.0
        best_ll = -float("inf")
        for lam in np.linspace(-2, 2, 41):
            if lam == 0:
                X_trans = np.log(X[:, f])
            else:
                X_trans = (X[:, f] ** lam - 1) / lam
            # Log-likelihood (simplified Gaussian)
            mu = np.mean(X_trans)
            sigma2 = np.var(X_trans)
            if sigma2 == 0:
                continue
            ll = -0.5 * len(X_trans) * np.log(2 * np.pi * sigma2) \
                 - 0.5 * np.sum((X_trans - mu) ** 2) / sigma2 \
                 + (lam - 1) * np.sum(np.log(X[:, f]))
            if ll > best_ll:
                best_ll = ll
                best_lam = lam
        lambdas.append(best_lam)
    return float(np.median(lambdas))


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Feature Construction ===")

    np.random.seed(42)
    X = np.random.randn(100, 3)
    X_pos = np.abs(X) + 0.1  # strictly positive for Box-Cox

    # --- PolynomialFeatures ---
    poly = PolynomialFeatures(degree=2, include_bias=True)
    X_poly = poly.fit_transform(X)
    # For 3 features, degree=2 with bias:
    # [1, x1, x2, x3, x1², x1x2, x1x3, x2², x2x3, x3²] = 10 features
    assert X_poly.shape[1] == 10, f"Expected 10 features, got {X_poly.shape[1]}"
    # Bias column should be all ones
    assert np.allclose(X_poly[:, 0], 1.0)
    print(f"  PolynomialFeatures (degree=2): {X_poly.shape[1]} features")

    # Without bias
    poly_nb = PolynomialFeatures(degree=2, include_bias=False)
    X_poly_nb = poly_nb.fit_transform(X)
    assert X_poly_nb.shape[1] == 9
    print("  PolynomialFeatures (no bias): PASS")

    # --- InteractionFeatures ---
    inter = InteractionFeatures()
    X_inter = inter.fit_transform(X)
    # 3 original + 3 interactions (3*2/2)
    assert X_inter.shape[1] == 6, f"Expected 6, got {X_inter.shape[1]}"
    # Check interaction: x1 * x2
    assert np.allclose(X_inter[:, 3], X[:, 0] * X[:, 1])
    print("  InteractionFeatures: PASS")

    # --- Binning ---
    bd = BinningDiscretizer(n_bins=5, strategy="uniform", encode="ordinal")
    X_binned = bd.fit_transform(X)
    assert X_binned.shape == X.shape
    # Binned values should be in range [0, n_bins-1]
    assert np.all((X_binned >= 0) & (X_binned < 5))
    print("  Binning (ordinal): PASS")

    # One-hot encoding
    bd_oh = BinningDiscretizer(n_bins=3, strategy="quantile", encode="onehot")
    X_binned_oh = bd_oh.fit_transform(X)
    assert X_binned_oh.shape[1] == 3 * 3  # 3 features × 3 bins
    assert np.allclose(np.sum(X_binned_oh, axis=1), 3)
    print("  Binning (onehot): PASS")

    # --- Log transform ---
    X_log = log_transform(X_pos)
    assert X_log.shape == X_pos.shape
    assert np.all(np.isfinite(X_log))
    print("  Log transform: PASS")

    # --- Box-Cox ---
    X_bc = box_cox_transform(X_pos, lam=0.0)  # equivalent to log
    assert X_bc.shape == X_pos.shape
    assert np.all(np.isfinite(X_bc))
    print("  Box-Cox (lam=0): PASS")

    X_bc2 = box_cox_transform(X_pos, lam=0.5)
    assert np.all(np.isfinite(X_bc2))
    print("  Box-Cox (lam=0.5): PASS")

    # --- Estimate lambda ---
    lam_est = estimate_box_cox_lambda(X_pos)
    print(f"  Estimated Box-Cox lambda: {lam_est:.4f}")
    assert -3 < lam_est < 3
    print("  Lambda estimation: PASS")

    print("All Feature Construction tests PASSED!\n")
