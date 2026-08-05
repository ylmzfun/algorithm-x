"""Collaborative Filtering from scratch using NumPy.

Implements:
- User-based collaborative filtering
- Item-based collaborative filtering
- Matrix Factorization (SVD for CF) with SGD
- RMSE evaluation metric

Reference: Koren et al., "Matrix Factorization Techniques for
Recommender Systems" (2009).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# RMSE
# ---------------------------------------------------------------------------

def rmse(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute Root Mean Squared Error.

    Args:
        y_true: Ground truth values.
        y_pred: Predicted values.

    Returns:
        RMSE value.
    """
    return float(np.sqrt(np.mean((y_true - y_pred) ** 2)))


def _cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two vectors."""
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    return float(np.dot(a, b) / denom) if denom > 0 else 0.0


def _pearson_sim(a: np.ndarray, b: np.ndarray) -> float:
    """Pearson correlation between two vectors (considering only overlapping non-zero entries)."""
    mask = (a != 0) & (b != 0)
    if np.sum(mask) < 2:
        return 0.0
    a_m = a[mask] - np.mean(a[mask])
    b_m = b[mask] - np.mean(b[mask])
    denom = np.linalg.norm(a_m) * np.linalg.norm(b_m)
    return float(np.dot(a_m, b_m) / denom) if denom > 0 else 0.0


# ---------------------------------------------------------------------------
# User-Based CF
# ---------------------------------------------------------------------------

class UserBasedCF:
    """User-based collaborative filtering.

    Predicts a user's rating for an item as the weighted average of
    similar users' ratings for that item.

    Attributes:
        user_sim: User-user similarity matrix [n_users, n_users].
        ratings: Original (or mean-centered) rating matrix.
        user_means: Mean rating per user.
    """

    def __init__(self, k: int = 5) -> None:
        """Initialize user-based CF.

        Args:
            k: Number of similar users to consider.
        """
        self.k = k
        self.user_sim: np.ndarray = np.array([])
        self.ratings: np.ndarray = np.array([])
        self.user_means: np.ndarray = np.array([])

    def fit(self, ratings: np.ndarray) -> None:
        """Compute user-user similarity matrix.

        Args:
            ratings: Rating matrix [n_users, n_items]. 0 = unrated.
        """
        self.ratings = ratings.astype(np.float64)
        n_users = ratings.shape[0]
        self.user_sim = np.zeros((n_users, n_users))
        self.user_means = np.zeros(n_users)

        for u in range(n_users):
            rated = ratings[u] > 0
            if np.any(rated):
                self.user_means[u] = np.mean(ratings[u, rated])
            else:
                self.user_means[u] = 0.0

            for v in range(n_users):
                if u != v:
                    self.user_sim[u, v] = _pearson_sim(ratings[u], ratings[v])

    def predict(self, user: int, item: int) -> float:
        """Predict rating for a given user-item pair.

        Args:
            user: User index.
            item: Item index.

        Returns:
            Predicted rating.
        """
        sims = self.user_sim[user].copy()
        # Only consider users who rated this item
        rated_mask = (self.ratings[:, item] > 0)
        sims[~rated_mask] = -1  # Exclude

        # Top-k similar users
        top_users = np.argsort(sims)[::-1][:self.k]
        top_users = [u for u in top_users if sims[u] > 0]

        if not top_users:
            return self.user_means[user]

        # Weighted average of (mean-centered) ratings
        numer = 0.0
        denom = 0.0
        for v in top_users:
            w = self.user_sim[user, v]
            numer += w * (self.ratings[v, item] - self.user_means[v])
            denom += abs(w)

        pred = self.user_means[user]
        if denom > 0:
            pred += numer / denom
        return pred


# ---------------------------------------------------------------------------
# Item-Based CF
# ---------------------------------------------------------------------------

class ItemBasedCF:
    """Item-based collaborative filtering.

    Predicts a user's rating for an item as the weighted average of
    the user's ratings for similar items.

    Attributes:
        item_sim: Item-item similarity matrix [n_items, n_items].
        ratings: Rating matrix.
    """

    def __init__(self, k: int = 5) -> None:
        """Initialize item-based CF.

        Args:
            k: Number of similar items to consider.
        """
        self.k = k
        self.item_sim: np.ndarray = np.array([])
        self.ratings: np.ndarray = np.array([])

    def fit(self, ratings: np.ndarray) -> None:
        """Compute item-item similarity matrix.

        Args:
            ratings: Rating matrix [n_users, n_items].
        """
        self.ratings = ratings.astype(np.float64)
        n_items = ratings.shape[1]
        self.item_sim = np.zeros((n_items, n_items))

        for i in range(n_items):
            for j in range(n_items):
                if i != j:
                    self.item_sim[i, j] = _cosine_sim(
                        ratings[:, i], ratings[:, j]
                    )

    def predict(self, user: int, item: int) -> float:
        """Predict rating for a given user-item pair.

        Args:
            user: User index.
            item: Item index.

        Returns:
            Predicted rating.
        """
        # Items the user has rated
        user_rated = self.ratings[user] > 0
        sims = self.item_sim[item].copy()
        sims[~user_rated] = -1

        top_items = np.argsort(sims)[::-1][:self.k]
        top_items = [j for j in top_items if sims[j] > 0]

        if not top_items:
            return np.mean(self.ratings[user, user_rated]) if np.any(user_rated) else 3.0

        numer = 0.0
        denom = 0.0
        for j in top_items:
            w = self.item_sim[item, j]
            numer += w * self.ratings[user, j]
            denom += abs(w)

        return float(numer / denom) if denom > 0 else 3.0


# ---------------------------------------------------------------------------
# Matrix Factorization (SVD for CF)
# ---------------------------------------------------------------------------

class MatrixFactorization:
    """Matrix Factorization for collaborative filtering via SGD.

    Learns user factors P [n_users, k] and item factors Q [n_items, k]
    such that R ≈ P @ Q^T, plus bias terms.

    r_hat(u,i) = mu + b_u + b_i + p_u · q_i

    Attributes:
        n_users, n_items: Rating matrix dimensions.
        n_factors: Latent factor dimension.
        mu: Global mean rating.
        P: User factor matrix.
        Q: Item factor matrix.
        b_u: User biases.
        b_i: Item biases.
    """

    def __init__(self, n_factors: int = 10, lr: float = 0.01,
                 reg: float = 0.02, seed: int = 42) -> None:
        """Initialize matrix factorization.

        Args:
            n_factors: Number of latent factors.
            lr: Learning rate for SGD.
            reg: L2 regularization strength.
            seed: Random seed.
        """
        self.n_factors = n_factors
        self.lr = lr
        self.reg = reg
        self.rng = np.random.default_rng(seed)

        self.mu: float = 0.0
        self.P: np.ndarray = np.array([])
        self.Q: np.ndarray = np.array([])
        self.b_u: np.ndarray = np.array([])
        self.b_i: np.ndarray = np.array([])

    def fit(self, ratings: np.ndarray, epochs: int = 50) -> list[float]:
        """Train the matrix factorization model.

        Args:
            ratings: Rating matrix [n_users, n_items]. 0 = unrated.
            epochs: Number of training epochs.

        Returns:
            List of RMSE values per epoch (on training data).
        """
        ratings = ratings.astype(np.float64)
        self.n_users, self.n_items = ratings.shape

        # Find rated entries
        rows, cols = np.where(ratings > 0)
        train_indices = list(zip(rows, cols))
        train_values = ratings[rows, cols]

        # Global mean
        self.mu = np.mean(train_values)

        # Initialize parameters
        self.P = self.rng.normal(0, 0.1, (self.n_users, self.n_factors))
        self.Q = self.rng.normal(0, 0.1, (self.n_items, self.n_factors))
        self.b_u = np.zeros(self.n_users)
        self.b_i = np.zeros(self.n_items)

        epoch_losses: list[float] = []

        for epoch in range(epochs):
            # Shuffle training data
            perm = self.rng.permutation(len(train_indices))
            for idx in perm:
                u, i = train_indices[idx]
                r = train_values[idx]

                # Prediction
                pred = self.mu + self.b_u[u] + self.b_i[i] \
                    + np.dot(self.P[u], self.Q[i])
                err = r - pred

                # SGD update
                self.b_u[u] += self.lr * (err - self.reg * self.b_u[u])
                self.b_i[i] += self.lr * (err - self.reg * self.b_i[i])

                p_u = self.P[u].copy()
                self.P[u] += self.lr * (err * self.Q[i] - self.reg * self.P[u])
                self.Q[i] += self.lr * (err * p_u - self.reg * self.Q[i])

            # Compute training RMSE
            train_preds = self.predict_batch(
                np.array([u for u, _ in train_indices]),
                np.array([i for _, i in train_indices]),
            )
            epoch_rmse = rmse(train_values, train_preds)
            epoch_losses.append(epoch_rmse)

        return epoch_losses

    def predict(self, user: int, item: int) -> float:
        """Predict rating for a single user-item pair.

        Args:
            user: User index.
            item: Item index.

        Returns:
            Predicted rating.
        """
        return float(
            self.mu + self.b_u[user] + self.b_i[item]
            + np.dot(self.P[user], self.Q[item])
        )

    def predict_batch(
        self, users: np.ndarray, items: np.ndarray
    ) -> np.ndarray:
        """Predict ratings for multiple user-item pairs.

        Args:
            users: User indices [N].
            items: Item indices [N].

        Returns:
            Predicted ratings [N].
        """
        return (
            self.mu
            + self.b_u[users]
            + self.b_i[items]
            + np.sum(self.P[users] * self.Q[items], axis=1)
        )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing collaborative_filtering.py — Collaborative Filtering")
    print("=" * 60)

    # Create a small user-item rating matrix (10 users, 8 items)
    np.random.seed(42)
    n_users, n_items = 10, 8
    # True latent factors
    true_P = np.random.randn(n_users, 3)
    true_Q = np.random.randn(n_items, 3)
    true_ratings = 3.0 + true_P @ true_Q.T  # mean ~3

    # Create sparse ratings (hide 30% for testing)
    ratings = true_ratings.copy()
    mask = np.random.random((n_users, n_items)) < 0.3
    ratings[mask] = 0  # 0 = unrated

    print(f"\nRating matrix: {n_users} users x {n_items} items")
    print(f"  Sparsity: {np.mean(ratings == 0):.1%}")

    all_pass = True

    # Test 1: Matrix Factorization
    print("\n--- Matrix Factorization ---")
    mf = MatrixFactorization(n_factors=3, lr=0.01, reg=0.02, seed=42)
    mf_losses = mf.fit(ratings, epochs=100)

    print(f"  Initial RMSE: {mf_losses[0]:.4f}")
    print(f"  Final RMSE:   {mf_losses[-1]:.4f}")
    mf_improved = mf_losses[-1] < mf_losses[0]
    print(f"  RMSE decreased: {mf_improved}")
    all_pass = all_pass and mf_improved

    # Predict held-out ratings
    rows, cols = np.where(mask)
    if len(rows) > 0:
        true_vals = true_ratings[rows, cols]
        pred_vals = mf.predict_batch(rows, cols)
        test_rmse = rmse(true_vals, pred_vals)
        print(f"  Held-out RMSE: {test_rmse:.4f}")
        all_pass = all_pass and test_rmse < 5.0

    # Test 2: User-Based CF
    print("\n--- User-Based CF ---")
    ucf = UserBasedCF(k=3)
    ucf.fit(ratings)
    ucf_pred = ucf.predict(0, 0)
    print(f"  User 0, Item 0 prediction: {ucf_pred:.2f}")

    # Test 3: Item-Based CF
    print("\n--- Item-Based CF ---")
    icf = ItemBasedCF(k=3)
    icf.fit(ratings)
    icf_pred = icf.predict(0, 0)
    print(f"  User 0, Item 0 prediction: {icf_pred:.2f}")

    # Compare predictions (they should be in a reasonable range)
    for pred_name, pred_val in [("MF", mf.predict(0, 0)),
                                 ("UCF", ucf_pred),
                                 ("ICF", icf_pred)]:
        reasonable = 0.0 < pred_val < 10.0
        print(f"  {pred_name} prediction reasonable (0-10): {reasonable}")
        all_pass = all_pass and reasonable

    # Test 4: RMSE metric
    print("\n--- RMSE ---")
    a = np.array([1.0, 2.0, 3.0])
    b = np.array([1.0, 2.0, 3.0])
    c = np.array([2.0, 3.0, 4.0])
    print(f"  RMSE(a, a) = {rmse(a, b):.4f} (expected 0.0)")
    print(f"  RMSE(a, c) = {rmse(a, c):.4f} (expected ~1.0)")
    all_pass = all_pass and abs(rmse(a, b)) < 0.001
    all_pass = all_pass and abs(rmse(a, c) - 1.0) < 0.01

    print(f"\n{'PASS' if all_pass else 'FAIL'}: collaborative_filtering.py")
