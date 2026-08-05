"""Preprocessing utilities: scalers, encoders, train/test split, k-fold CV.

All implementations are from scratch using numpy, with sklearn-compatible APIs
for easy comparison during testing.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Tuple

# ======================================================================
# StandardScaler
# ======================================================================


class StandardScaler:
    """Standardize features by removing the mean and scaling to unit variance.

    Computes z = (x - mean) / std for each feature.

    Parameters
    ----------
    with_mean : bool, default=True
        If True, center the data before scaling.
    with_std : bool, default=True
        If True, scale the data to unit variance.

    Attributes
    ----------
    mean_ : np.ndarray of shape (n_features,)
        Per-feature mean of the training data.
    std_ : np.ndarray of shape (n_features,)
        Per-feature standard deviation of the training data.
    """

    def __init__(self, with_mean: bool = True, with_std: bool = True) -> None:
        self.with_mean = with_mean
        self.with_std = with_std
        self.mean_: np.ndarray | None = None
        self.std_: np.ndarray | None = None

    def fit(self, X: np.ndarray) -> StandardScaler:
        """Compute mean and std for later scaling.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        if self.with_mean:
            self.mean_ = np.mean(X, axis=0)
        if self.with_std:
            self.std_ = np.std(X, axis=0, ddof=0)
            # Avoid division by zero
            self.std_[self.std_ == 0] = 1.0
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Scale X according to fitted parameters.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_scaled : np.ndarray
        """
        X = X.astype(np.float64, copy=False)
        if self.with_mean:
            X = X - self.mean_
        if self.with_std:
            X = X / self.std_
        return X

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit to data, then transform it.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_scaled : np.ndarray
        """
        return self.fit(X).transform(X)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """Undo the scaling.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_original : np.ndarray
        """
        X = X.astype(np.float64, copy=False)
        if self.with_std:
            X = X * self.std_
        if self.with_mean:
            X = X + self.mean_
        return X


# ======================================================================
# MinMaxScaler
# ======================================================================


class MinMaxScaler:
    """Transform features by scaling each feature to a given range.

    The default range is [0, 1].

    Parameters
    ----------
    feature_range : tuple (min, max), default=(0, 1)

    Attributes
    ----------
    min_ : np.ndarray of shape (n_features,)
        Per-feature minimum seen in the data.
    scale_ : np.ndarray of shape (n_features,)
        Per-feature relative scaling.
    """

    def __init__(self, feature_range: Tuple[float, float] = (0, 1)) -> None:
        self.feature_range = feature_range
        self.min_: np.ndarray | None = None
        self.scale_: np.ndarray | None = None
        self.data_min_: np.ndarray | None = None
        self.data_max_: np.ndarray | None = None

    def fit(self, X: np.ndarray) -> MinMaxScaler:
        """Compute min and range for scaling.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        self
        """
        self.data_min_ = np.min(X, axis=0)
        self.data_max_ = np.max(X, axis=0)
        data_range = self.data_max_ - self.data_min_
        data_range[data_range == 0] = 1.0
        self.scale_ = (self.feature_range[1] - self.feature_range[0]) / data_range
        self.min_ = self.feature_range[0] - self.data_min_ * self.scale_
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Scale X according to fitted parameters.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_scaled : np.ndarray
        """
        return X * self.scale_ + self.min_

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit to data, then transform it."""
        return self.fit(X).transform(X)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """Undo the scaling.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_original : np.ndarray
        """
        return (X - self.min_) / self.scale_


# ======================================================================
# LabelEncoder
# ======================================================================


class LabelEncoder:
    """Encode target labels with integer values between 0 and n_classes-1.

    Attributes
    ----------
    classes_ : np.ndarray of shape (n_classes,)
        Unique class labels.
    """

    def __init__(self) -> None:
        self.classes_: np.ndarray | None = None
        self._class_to_idx: dict = {}

    def fit(self, y: np.ndarray) -> LabelEncoder:
        """Fit label encoder.

        Parameters
        ----------
        y : np.ndarray of shape (n_samples,)
            Target values.

        Returns
        -------
        self
        """
        self.classes_ = np.unique(y)
        self._class_to_idx = {c: i for i, c in enumerate(self.classes_)}
        return self

    def transform(self, y: np.ndarray) -> np.ndarray:
        """Transform labels to normalized encoding.

        Parameters
        ----------
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        y_encoded : np.ndarray of shape (n_samples,)
        """
        return np.array([self._class_to_idx[v] for v in y])

    def fit_transform(self, y: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(y).transform(y)

    def inverse_transform(self, y: np.ndarray) -> np.ndarray:
        """Transform integer labels back to original encoding.

        Parameters
        ----------
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        y_original : np.ndarray
        """
        return self.classes_[y.astype(int)]


# ======================================================================
# OneHotEncoder
# ======================================================================


class OneHotEncoder:
    """Encode categorical features as a one-hot numeric array.

    Attributes
    ----------
    categories_ : list of np.ndarray
        Unique categories per feature.
    """

    def __init__(self, sparse: bool = False) -> None:
        self.sparse = sparse
        self.categories_: list[np.ndarray] = []
        self._dtype = np.float64

    def fit(self, X: np.ndarray) -> OneHotEncoder:
        """Fit the encoder.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
            Categorical data.

        Returns
        -------
        self
        """
        self.categories_ = [np.unique(X[:, i]) for i in range(X.shape[1])]
        return self

    def transform(self, X: np.ndarray) -> np.ndarray:
        """Transform X using one-hot encoding.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)

        Returns
        -------
        X_out : np.ndarray of shape (n_samples, total_categories)
        """
        n_samples = X.shape[0]
        col_indices = []
        for i, cats in enumerate(self.categories_):
            mapping = {c: j for j, c in enumerate(cats)}
            col_indices.append(np.array([mapping[v] for v in X[:, i]]))

        offsets = np.cumsum([0] + [len(c) for c in self.categories_[:-1]])
        row_idx = np.arange(n_samples)
        n_total = sum(len(c) for c in self.categories_)
        result = np.zeros((n_samples, n_total), dtype=self._dtype)
        for feat_idx, col_idx in enumerate(col_indices):
            result[row_idx, offsets[feat_idx] + col_idx] = 1.0
        return result

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit and transform."""
        return self.fit(X).transform(X)

    def inverse_transform(self, X: np.ndarray) -> np.ndarray:
        """Convert one-hot encoded data back to categorical.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, total_categories)

        Returns
        -------
        X_orig : np.ndarray of shape (n_samples, n_features)
        """
        n_samples = X.shape[0]
        offsets = np.cumsum([0] + [len(c) for c in self.categories_[:-1]])
        result = np.empty((n_samples, len(self.categories_)), dtype=object)

        for feat_idx, cats in enumerate(self.categories_):
            start = offsets[feat_idx]
            end = start + len(cats)
            sub = X[:, start:end]
            indices = np.argmax(sub, axis=1)
            result[:, feat_idx] = cats[indices]
        return result


# ======================================================================
# train_test_split
# ======================================================================


def train_test_split(
    *arrays: np.ndarray,
    test_size: float = 0.25,
    shuffle: bool = True,
    random_state: Optional[int] = None,
) -> list[np.ndarray]:
    """Split arrays into random train and test subsets.

    Parameters
    ----------
    *arrays : np.ndarray
        Arrays to split (e.g., X, y).
    test_size : float
        Proportion of the dataset to include in the test split.
    shuffle : bool
        Whether to shuffle the data before splitting.
    random_state : int or None
        Seed for reproducibility.

    Returns
    -------
    splits : list[np.ndarray]
        Train-test split for each input array, in the same order.
    """
    if not arrays:
        raise ValueError("At least one array is required.")

    n_samples = arrays[0].shape[0]
    for arr in arrays:
        if arr.shape[0] != n_samples:
            raise ValueError(
                f"Found array with {arr.shape[0]} samples while the "
                f"first has {n_samples}."
            )

    n_test = max(1, int(n_samples * test_size))
    indices = np.arange(n_samples)

    if shuffle:
        rng = np.random.RandomState(random_state)
        rng.shuffle(indices)

    train_idx = indices[:-n_test] if n_test < n_samples else indices[:0]
    test_idx = indices[-n_test:]

    result = []
    for arr in arrays:
        result.append(arr[train_idx])
        result.append(arr[test_idx])
    return result


# ======================================================================
# KFold
# ======================================================================


class KFold:
    """K-Fold cross-validator.

    Provides train/test indices to split data into k consecutive folds.

    Parameters
    ----------
    n_splits : int, default=5
        Number of folds.
    shuffle : bool, default=False
        Whether to shuffle the data before splitting.
    random_state : int or None, default=None
        Seed for reproducibility when shuffle=True.
    """

    def __init__(
        self,
        n_splits: int = 5,
        shuffle: bool = False,
        random_state: Optional[int] = None,
    ) -> None:
        if n_splits < 2:
            raise ValueError("n_splits must be at least 2.")
        self.n_splits = n_splits
        self.shuffle = shuffle
        self.random_state = random_state

    def split(self, X: np.ndarray, y: np.ndarray | None = None):
        """Generate indices to split data into training and test sets.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray or None (ignored)

        Yields
        ------
        train_idx : np.ndarray
        test_idx : np.ndarray
        """
        n_samples = X.shape[0]
        indices = np.arange(n_samples)
        if self.shuffle:
            rng = np.random.RandomState(self.random_state)
            rng.shuffle(indices)

        fold_sizes = np.full(self.n_splits, n_samples // self.n_splits, dtype=int)
        fold_sizes[: n_samples % self.n_splits] += 1

        current = 0
        for fold_size in fold_sizes:
            start, stop = current, current + fold_size
            test_idx = indices[start:stop]
            train_idx = np.concatenate([indices[:start], indices[stop:]])
            yield train_idx, test_idx
            current = stop

    def get_n_splits(self) -> int:
        """Return the number of splitting iterations."""
        return self.n_splits


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Preprocessing ===")

    # Test data
    np.random.seed(42)
    X = np.random.randn(100, 3)
    X[0, 0] = 100  # outlier
    y = np.array(["a", "b", "c"] * 33 + ["a"])
    cat_X = np.array([["red", "small"], ["blue", "large"], ["green", "medium"]])

    # --- StandardScaler ---
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    assert np.allclose(np.mean(X_scaled, axis=0), 0, atol=1e-10), "StandardScaler mean failed"
    assert np.allclose(np.std(X_scaled, axis=0, ddof=0), 1, atol=1e-10), "StandardScaler std failed"
    X_inv = scaler.inverse_transform(X_scaled)
    assert np.allclose(X, X_inv), "StandardScaler inverse failed"
    print("  StandardScaler: PASS")

    # --- MinMaxScaler ---
    mm_scaler = MinMaxScaler()
    X_mm = mm_scaler.fit_transform(X)
    assert np.allclose(np.min(X_mm, axis=0), 0, atol=1e-10), "MinMaxScaler min failed"
    assert np.allclose(np.max(X_mm, axis=0), 1, atol=1e-10), "MinMaxScaler max failed"
    print("  MinMaxScaler: PASS")

    # --- LabelEncoder ---
    le = LabelEncoder()
    y_enc = le.fit_transform(y)
    assert np.array_equal(np.unique(y_enc), [0, 1, 2]), "LabelEncoder encoding failed"
    y_orig = le.inverse_transform(y_enc)
    assert np.array_equal(y_orig, y), "LabelEncoder inverse failed"
    print("  LabelEncoder: PASS")

    # --- OneHotEncoder ---
    ohe = OneHotEncoder()
    ohe.fit(cat_X)
    X_ohe = ohe.transform(cat_X)
    # 3 categories for color, 3 for size = 6 total
    assert X_ohe.shape == (3, 6), f"OneHotEncoder shape failed: {X_ohe.shape}"
    assert np.all(np.sum(X_ohe, axis=1) == 2), "OneHotEncoder row sum failed"
    print("  OneHotEncoder: PASS")

    # --- train_test_split ---
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_enc, test_size=0.3, random_state=42
    )
    assert len(X_train) == 70, f"train size: {len(X_train)}"
    assert len(X_test) == 30, f"test size: {len(X_test)}"
    print("  train_test_split: PASS")

    # --- KFold ---
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    folds = list(kf.split(X, y_enc))
    assert len(folds) == 5, f"KFold n_splits: {len(folds)}"
    for train_idx, test_idx in folds:
        assert len(np.intersect1d(train_idx, test_idx)) == 0, "KFold overlap"
    print("  KFold: PASS")

    print("All preprocessing tests PASSED!\n")
