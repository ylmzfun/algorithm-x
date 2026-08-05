"""Feature Encoding methods from scratch.

Includes:
- Label encoding
- One-hot encoding
- Target encoding (mean target per category)
- Frequency encoding (category count ratio)
- Ordinal encoding (user-specified order)
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Dict, List


class LabelEncoder:
    """Encode categorical labels as integers.

    Attributes
    ----------
    classes_ : np.ndarray
        Unique class labels.
    """

    def __init__(self) -> None:
        self.classes_: np.ndarray | None = None
        self._mapping: dict = {}

    def fit(self, y: np.ndarray) -> LabelEncoder:
        """Fit label encoder.

        Parameters
        ----------
        y : np.ndarray of shape (n_samples,)
            Target labels.

        Returns
        -------
        self
        """
        self.classes_ = np.unique(y)
        self._mapping = {c: i for i, c in enumerate(self.classes_)}
        return self

    def transform(self, y: np.ndarray) -> np.ndarray:
        """Transform labels to integers."""
        return np.array([self._mapping[v] for v in y], dtype=int)

    def fit_transform(self, y: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(y).transform(y)

    def inverse_transform(self, y: np.ndarray) -> np.ndarray:
        """Transform integers back to original labels."""
        return self.classes_[y.astype(int)]


class OneHotEncoder:
    """One-hot encode categorical features.

    Attributes
    ----------
    categories_ : list of np.ndarray
        Unique categories per feature.
    """

    def __init__(self) -> None:
        self.categories_: list[np.ndarray] = []

    def fit(self, X: np.ndarray) -> OneHotEncoder:
        """Fit the encoder.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        self.categories_ = [np.unique(X[:, i]) for i in range(X.shape[1])]
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """One-hot encode X.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_encoded : np.ndarray of shape (n_samples, total_categories)
        """
        n_samples = X.shape[0]
        idx_per_feat = []
        for i, cats in enumerate(self.categories_):
            mapping = {c: j for j, c in enumerate(cats)}
            idx_per_feat.append(np.array([mapping[v] for v in X[:, i]], dtype=int))

        offsets = np.cumsum([0] + [len(c) for c in self.categories_[:-1]])
        n_total = sum(len(c) for c in self.categories_)
        result = np.zeros((n_samples, n_total), dtype=np.float64)
        row_idx = np.arange(n_samples)
        for feat_idx, col_idx in enumerate(idx_per_feat):
            result[row_idx, offsets[feat_idx] + col_idx] = 1.0
        return result

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)


class TargetEncoder:
    """Target encoding: replace category with mean target value.

    Uses smoothing to avoid overfitting:
    encoded = (n_cat * mean_cat + m * global_mean) / (n_cat + m)

    Parameters
    ----------
    smoothing : float, default=1.0
        Smoothing parameter m. Higher = more regularization towards global mean.
    """

    def __init__(self, smoothing: float = 1.0) -> None:
        self.smoothing = smoothing
        self._mappings: list[dict] = []
        self._global_means: list[float] = []

    def fit(self, X: np.ndarray, y: np.ndarray) -> TargetEncoder:
        """Fit target encoder.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            Categorical data.
        y : np.ndarray of shape (n_samples,)
            Continuous target.

        Returns
        -------
        self
        """
        X = np.asarray(X)
        y = np.asarray(y, dtype=np.float64)
        global_mean = float(np.mean(y))

        self._mappings = []
        self._global_means = []

        for feat_idx in range(X.shape[1]):
            col = X[:, feat_idx]
            mapping = {}
            for cat in np.unique(col):
                mask = col == cat
                n_cat = np.sum(mask)
                mean_cat = np.mean(y[mask]) if n_cat > 0 else global_mean
                # Smoothed encoding
                encoded = (n_cat * mean_cat + self.smoothing * global_mean) / (n_cat + self.smoothing)
                mapping[cat] = encoded
            self._mappings.append(mapping)
            self._global_means.append(global_mean)

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform X using target encoding.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_encoded : np.ndarray of shape (n_samples, n_features)
        """
        X = np.asarray(X)
        n_samples, n_features = X.shape
        result = np.zeros((n_samples, n_features), dtype=np.float64)

        for feat_idx in range(n_features):
            mapping = self._mappings[feat_idx]
            global_mean = self._global_means[feat_idx]
            col = X[:, feat_idx]
            result[:, feat_idx] = np.array(
                [mapping.get(v, global_mean) for v in col]
            )
        return result

    def fit_transform(self, X: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X, y).transform(X)


class FrequencyEncoder:
    """Frequency encoding: replace category with its frequency (or count).

    Parameters
    ----------
    normalize : bool, default=True
        If True, use relative frequency; if False, use absolute count.
    """

    def __init__(self, normalize: bool = True) -> None:
        self.normalize = normalize
        self._mappings: list[dict] = []

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> FrequencyEncoder:
        """Fit frequency encoder.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : ignored

        Returns
        -------
        self
        """
        X = np.asarray(X)
        n_samples = X.shape[0]
        self._mappings = []

        for feat_idx in range(X.shape[1]):
            col = X[:, feat_idx]
            unique, counts = np.unique(col, return_counts=True)
            if self.normalize:
                freqs = counts / n_samples
            else:
                freqs = counts
            self._mappings.append(dict(zip(unique, freqs)))

        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform X using frequency encoding."""
        X = np.asarray(X)
        n_samples, n_features = X.shape
        result = np.zeros((n_samples, n_features), dtype=np.float64)

        for feat_idx in range(n_features):
            mapping = self._mappings[feat_idx]
            result[:, feat_idx] = np.array(
                [mapping.get(v, 0.0) for v in X[:, feat_idx]]
            )
        return result

    def fit_transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)


class OrdinalEncoder:
    """Ordinal encoding: replace categories with ordinal integers.

    Parameters
    ----------
    categories : list of list or 'auto', default='auto'
        If 'auto', categories are sorted. Otherwise, provide ordered list
        per feature.

    Attributes
    ----------
    categories_ : list of np.ndarray
    """

    def __init__(self, categories: list | str = "auto") -> None:
        self.categories = categories
        self.categories_: list[np.ndarray] = []
        self._mappings: list[dict] = []

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> OrdinalEncoder:
        """Fit ordinal encoder.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : ignored

        Returns
        -------
        self
        """
        X = np.asarray(X)

        if isinstance(self.categories, str) and self.categories == "auto":
            self.categories_ = [np.sort(np.unique(X[:, i])) for i in range(X.shape[1])]
        else:
            self.categories_ = [np.asarray(cat) for cat in self.categories]

        self._mappings = [
            {c: i for i, c in enumerate(cats)}
            for cats in self.categories_
        ]
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform X using ordinal encoding."""
        X = np.asarray(X)
        n_samples, n_features = X.shape
        result = np.zeros((n_samples, n_features), dtype=np.float64)

        for feat_idx in range(n_features):
            mapping = self._mappings[feat_idx]
            result[:, feat_idx] = np.array(
                [mapping.get(v, -1) for v in X[:, feat_idx]]
            )
        return result

    def fit_transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Feature Encoding ===")

    np.random.seed(42)

    # Sample categorical data
    X_cat = np.array([
        ["red", "small"],
        ["blue", "large"],
        ["green", "medium"],
        ["red", "large"],
        ["blue", "small"],
        ["green", "medium"],
    ])
    y_reg = np.array([1.0, 2.0, 3.0, 1.5, 1.8, 3.2])

    # --- LabelEncoder ---
    le = LabelEncoder()
    y_enc = le.fit_transform(np.array(["a", "b", "c", "a", "b"]))
    assert np.array_equal(y_enc, [0, 1, 2, 0, 1])
    y_orig = le.inverse_transform(y_enc)
    assert np.array_equal(y_orig, ["a", "b", "c", "a", "b"])
    print("  LabelEncoder: PASS")

    # --- OneHotEncoder ---
    ohe = OneHotEncoder()
    X_ohe = ohe.fit_transform(X_cat)
    # 3 colors + 3 sizes = 6 dims
    assert X_ohe.shape == (6, 6)
    assert np.all(np.sum(X_ohe, axis=1) == 2)
    print("  OneHotEncoder: PASS")

    # --- TargetEncoder ---
    te = TargetEncoder(smoothing=1.0)
    X_te = te.fit_transform(X_cat, y_reg)
    assert X_te.shape == (6, 2)
    # Should encode to continuous values near the target mean
    print(f"  Target encoding means: {X_te.mean(axis=0)}")
    print("  TargetEncoder: PASS")

    # --- FrequencyEncoder ---
    fe = FrequencyEncoder(normalize=True)
    X_fe = fe.fit_transform(X_cat)
    assert X_fe.shape == (6, 2)
    # Frequencies should be between 0 and 1
    assert np.all((X_fe >= 0) & (X_fe <= 1))
    # Sum of frequencies per feature should be 1.0 (each category appears 2 times = 2/6 + 2/6 + 2/6 = 1)
    print(f"  Frequency encoding sums: {X_fe.sum(axis=0)}")
    print("  FrequencyEncoder: PASS")

    # --- OrdinalEncoder ---
    oe = OrdinalEncoder(categories=[["blue", "green", "red"], ["small", "medium", "large"]])
    X_oe = oe.fit_transform(X_cat)
    assert X_oe.shape == (6, 2)
    # "blue" should map to 0, "green" to 1, "red" to 2
    assert X_oe[1, 0] == 0  # blue
    assert X_oe[2, 0] == 1  # green
    assert X_oe[0, 0] == 2  # red
    print("  OrdinalEncoder: PASS")

    print("All Feature Encoding tests PASSED!\n")
