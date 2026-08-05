"""Hyperparameter Tuning: Grid Search, Random Search, and Bayesian Optimization.

All implemented from scratch.
"""

from __future__ import annotations

import numpy as np
from itertools import product
from typing import Optional, Dict, Any, List, Tuple, Callable

# Handle imports for both package and direct execution
try:
    from .cross_validation import KFold, StratifiedKFold
except ImportError:
    import sys as _sys, os as _os
    _dir = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
    if _dir not in _sys.path:
        _sys.path.insert(0, _dir)
    from evaluation.cross_validation import KFold, StratifiedKFold


class GridSearchCV:
    """Exhaustive search over specified parameter values.

    Parameters
    ----------
    estimator : object
        Estimator with fit and predict/score methods.
    param_grid : dict
        Dictionary with parameter names as keys and lists of values.
    cv : cross-validator (or int for KFold), default=5
        Cross-validation strategy.
    scoring : str, default='accuracy'
        Scoring metric: 'accuracy' or 'r2'.
    refit : bool, default=True
        Refit on full dataset with best params.

    Attributes
    ----------
    best_params_ : dict
        Best parameter combination.
    best_score_ : float
        Mean CV score for best params.
    cv_results_ : dict
        All results.
    best_estimator_ : object
        Estimator refit on full data.
    """

    def __init__(
        self,
        estimator,
        param_grid: Dict[str, list],
        cv: int = 5,
        scoring: str = "accuracy",
        refit: bool = True,
    ) -> None:
        self.estimator = estimator
        self.param_grid = param_grid
        self.cv = cv
        self.scoring = scoring
        self.refit = refit
        self.best_params_: dict | None = None
        self.best_score_: float = float("-inf")
        self.cv_results_: dict = {}
        self.best_estimator_ = None

    def fit(self, X: np.ndarray, y: np.ndarray) -> GridSearchCV:
        """Run grid search.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y)

        # Build CV
        if self.scoring == "accuracy":
            cv = StratifiedKFold(n_splits=self.cv, shuffle=True)
        else:
            cv = KFold(n_splits=self.cv, shuffle=True)

        # Generate all parameter combinations
        keys = list(self.param_grid.keys())
        values = list(self.param_grid.values())
        param_combinations = list(product(*values))

        all_scores = []
        all_params = []

        for combo in param_combinations:
            params = dict(zip(keys, combo))
            fold_scores = []

            for train_idx, test_idx in cv.split(X, y):
                est = type(self.estimator)(**params)
                try:
                    est.fit(X[train_idx], y[train_idx])
                    if hasattr(est, "score") and self.scoring in ("accuracy", "r2"):
                        score = est.score(X[test_idx], y[test_idx])
                    else:
                        y_pred = est.predict(X[test_idx])
                        if self.scoring == "accuracy":
                            score = np.mean(y_pred == y[test_idx])
                        else:
                            ss_res = np.sum((y[test_idx] - y_pred) ** 2)
                            ss_tot = np.sum((y[test_idx] - np.mean(y[test_idx])) ** 2)
                            score = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
                    fold_scores.append(score)
                except Exception:
                    fold_scores.append(np.nan)

            mean_score = np.nanmean(fold_scores)
            all_scores.append((mean_score, np.nanstd(fold_scores)))
            all_params.append(params)

            if mean_score > self.best_score_:
                self.best_score_ = mean_score
                self.best_params_ = params

        self.cv_results_ = {
            "params": all_params,
            "mean_test_score": np.array([s[0] for s in all_scores]),
            "std_test_score": np.array([s[1] for s in all_scores]),
        }

        if self.refit and self.best_params_:
            self.best_estimator_ = type(self.estimator)(**self.best_params_)
            self.best_estimator_.fit(X, y)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using best estimator."""
        if self.best_estimator_ is None:
            raise ValueError("Model not fitted or refit=False.")
        return self.best_estimator_.predict(X)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Score using best estimator."""
        if self.best_estimator_ is None:
            raise ValueError("Model not fitted or refit=False.")
        return self.best_estimator_.score(X, y)


class RandomizedSearchCV:
    """Random search over hyperparameters.

    Parameters
    ----------
    estimator : object
    param_distributions : dict
        Dictionary with parameter names as keys and distributions as values.
        If value is list, sample uniformly. If tuple (low, high), sample
        uniformly from the range (for float/int params).
    n_iter : int, default=10
        Number of parameter settings sampled.
    cv : int, default=5
    scoring : str, default='accuracy'
    refit : bool, default=True
    random_state : int or None

    Attributes
    ----------
    best_params_ : dict
    best_score_ : float
    cv_results_ : dict
    best_estimator_ : object
    """

    def __init__(
        self,
        estimator,
        param_distributions: Dict[str, Any],
        n_iter: int = 10,
        cv: int = 5,
        scoring: str = "accuracy",
        refit: bool = True,
        random_state: int | None = None,
    ) -> None:
        self.estimator = estimator
        self.param_distributions = param_distributions
        self.n_iter = n_iter
        self.cv = cv
        self.scoring = scoring
        self.refit = refit
        self.random_state = random_state
        self.best_params_: dict | None = None
        self.best_score_: float = float("-inf")
        self.cv_results_: dict = {}
        self.best_estimator_ = None

    def _sample_params(self, rng: np.random.RandomState) -> dict:
        """Sample one parameter combination."""
        params = {}
        for key, dist in self.param_distributions.items():
            if isinstance(dist, list):
                params[key] = dist[rng.randint(len(dist))]
            elif isinstance(dist, tuple) and len(dist) == 2:
                low, high = dist
                if isinstance(low, int) and isinstance(high, int):
                    params[key] = rng.randint(low, high + 1)
                else:
                    params[key] = rng.uniform(low, high)
            elif callable(dist):
                params[key] = dist(rng)
            else:
                params[key] = dist
        return params

    def fit(self, X: np.ndarray, y: np.ndarray) -> RandomizedSearchCV:
        """Run random search.

        Parameters
        ----------
        X : np.ndarray of shape (n_samples, n_features)
        y : np.ndarray of shape (n_samples,)

        Returns
        -------
        self
        """
        X = np.asarray(X, dtype=np.float64)
        y = np.asarray(y)
        rng = np.random.RandomState(self.random_state)

        if self.scoring == "accuracy":
            cv = StratifiedKFold(n_splits=self.cv, shuffle=True,
                                 random_state=self.random_state)
        else:
            cv = KFold(n_splits=self.cv, shuffle=True,
                       random_state=self.random_state)

        all_scores = []
        all_params = []

        for _ in range(self.n_iter):
            params = self._sample_params(rng)
            # Merge with default estimator params
            base_params = {}
            for k, v in self.estimator.__dict__.items():
                if not k.endswith("_") and k not in params:
                    base_params[k] = v
            base_params.update(params)
            # Clean reserved/internal attrs
            final_params = {k: v for k, v in base_params.items()
                           if not k.startswith("_") and not k.endswith("_")}

            fold_scores = []
            for train_idx, test_idx in cv.split(X, y):
                try:
                    est = type(self.estimator)(**final_params)
                    est.fit(X[train_idx], y[train_idx])
                    if hasattr(est, "score"):
                        score = est.score(X[test_idx], y[test_idx])
                    else:
                        y_pred = est.predict(X[test_idx])
                        if self.scoring == "accuracy":
                            score = np.mean(y_pred == y[test_idx])
                        else:
                            ss_res = np.sum((y[test_idx] - y_pred) ** 2)
                            ss_tot = np.sum((y[test_idx] - np.mean(y[test_idx])) ** 2)
                            score = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
                    fold_scores.append(score)
                except Exception:
                    fold_scores.append(np.nan)

            mean_score = np.nanmean(fold_scores)
            all_scores.append((mean_score, np.nanstd(fold_scores)))
            all_params.append(params)

            if mean_score > self.best_score_:
                self.best_score_ = mean_score
                self.best_params_ = params

        self.cv_results_ = {
            "params": all_params,
            "mean_test_score": np.array([s[0] for s in all_scores]),
            "std_test_score": np.array([s[1] for s in all_scores]),
        }

        if self.refit and self.best_params_:
            self.best_estimator_ = type(self.estimator)(**self.best_params_)
            self.best_estimator_.fit(X, y)

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Predict using best estimator."""
        if self.best_estimator_ is None:
            raise ValueError("Model not fitted or refit=False.")
        return self.best_estimator_.predict(X)

    def score(self, X: np.ndarray, y: np.ndarray) -> float:
        """Score using best estimator."""
        if self.best_estimator_ is None:
            raise ValueError("Model not fitted or refit=False.")
        return self.best_estimator_.score(X, y)


class BayesianOptimSearch:
    """Simple Bayesian Optimization for hyperparameter tuning.

    Uses Gaussian Process regression as surrogate, Expected Improvement
    as acquisition function.

    Parameters
    ----------
    param_bounds : dict
        Parameter names -> (low, high) tuples for continuous params,
        or list of discrete values.
    n_iter : int, default=20
        Number of iterations.
    n_initial_points : int, default=5
        Number of random initial evaluations.
    cv : int, default=3
        Cross-validation folds.
    scoring : str, default='accuracy'
    random_state : int or None
    """

    def __init__(
        self,
        estimator,
        param_bounds: Dict[str, Any],
        n_iter: int = 20,
        n_initial_points: int = 5,
        cv: int = 3,
        scoring: str = "accuracy",
        random_state: int | None = None,
    ) -> None:
        self.estimator = estimator
        self.param_bounds = param_bounds
        self.n_iter = n_iter
        self.n_initial_points = n_initial_points
        self.cv = cv
        self.scoring = scoring
        self.random_state = random_state
        self.best_params_: dict | None = None
        self.best_score_: float = float("-inf")

    def _params_to_vector(self, params: dict) -> np.ndarray:
        """Convert params dict to normalized vector [0, 1]^d."""
        vec = []
        for key in sorted(self.param_bounds.keys()):
            bound = self.param_bounds[key]
            if isinstance(bound, tuple):
                low, high = bound
                vec.append((params[key] - low) / (high - low + 1e-10))
            else:
                idx = bound.index(params[key])
                vec.append(idx / max(len(bound) - 1, 1))
        return np.array(vec)

    def _vector_to_params(self, vec: np.ndarray) -> dict:
        """Convert normalized vector back to params."""
        params = {}
        for i, key in enumerate(sorted(self.param_bounds.keys())):
            bound = self.param_bounds[key]
            if isinstance(bound, tuple):
                low, high = bound
                params[key] = low + vec[i] * (high - low)
                if isinstance(low, int) and isinstance(high, int):
                    params[key] = int(round(params[key]))
            else:
                idx = int(round(vec[i] * (len(bound) - 1)))
                idx = max(0, min(idx, len(bound) - 1))
                params[key] = bound[idx]
        return params

    def _gp_predict(self, X_train: np.ndarray, y_train: np.ndarray,
                    X_test: np.ndarray, noise: float = 1e-6) -> Tuple[np.ndarray, np.ndarray]:
        """Gaussian Process prediction (RBF kernel). Returns mean and std."""
        def kernel(X1, X2, length_scale=1.0):
            sq_dists = np.sum(X1**2, axis=1).reshape(-1, 1) + \
                       np.sum(X2**2, axis=1).reshape(1, -1) - \
                       2 * X1 @ X2.T
            return np.exp(-0.5 * sq_dists / length_scale**2)

        K = kernel(X_train, X_train) + noise * np.eye(len(X_train))
        K_s = kernel(X_train, X_test)
        K_ss = kernel(X_test, X_test)

        try:
            K_inv = np.linalg.inv(K)
            mu = K_s.T @ K_inv @ y_train
            cov = K_ss - K_s.T @ K_inv @ K_s
            std = np.sqrt(np.maximum(np.diag(cov), 1e-10))
            return mu, std
        except np.linalg.LinAlgError:
            return np.zeros(len(X_test)), np.ones(len(X_test))

    def _expected_improvement(self, mu: np.ndarray, std: np.ndarray,
                              y_best: float, xi: float = 0.01) -> np.ndarray:
        """Expected Improvement acquisition function."""
        imp = mu - y_best - xi
        Z = imp / (std + 1e-10)
        pdf = np.exp(-0.5 * Z**2) / np.sqrt(2 * np.pi)
        cdf = 0.5 * (1 + np.array([self._erf_approx(z / np.sqrt(2)) for z in Z]))
        return imp * cdf + std * pdf

    @staticmethod
    def _erf_approx(x: float) -> float:
        """Approximate error function."""
        a1, a2, a3, a4, a5 = 0.254829592, -0.284496736, 1.421413741, -1.453152027, 1.061405429
        p = 0.3275911
        sign = 1 if x >= 0 else -1
        x = abs(x)
        t = 1.0 / (1.0 + p * x)
        y = 1.0 - (((((a5 * t + a4) * t) + a3) * t + a2) * t + a1) * t * np.exp(-x * x)
        return sign * y

    def fit(self, X: np.ndarray, y: np.ndarray) -> BayesianOptimSearch:
        """Run Bayesian optimization."""
        X_data = np.asarray(X, dtype=np.float64)
        y_data = np.asarray(y)
        rng = np.random.RandomState(self.random_state)
        n_dims = len(self.param_bounds)

        if self.scoring == "accuracy":
            cv = StratifiedKFold(n_splits=self.cv, shuffle=True,
                                 random_state=self.random_state)
        else:
            cv = KFold(n_splits=self.cv, shuffle=True,
                       random_state=self.random_state)

        def evaluate(params: dict) -> float:
            fold_scores = []
            for train_idx, test_idx in cv.split(X_data, y_data):
                try:
                    est = type(self.estimator)(**params)
                    est.fit(X_data[train_idx], y_data[train_idx])
                    if hasattr(est, "score"):
                        score = est.score(X_data[test_idx], y_data[test_idx])
                    else:
                        y_pred = est.predict(X_data[test_idx])
                        score = np.mean(y_pred == y_data[test_idx])
                    fold_scores.append(score)
                except Exception:
                    fold_scores.append(np.nan)
            return np.nanmean(fold_scores)

        X_obs = []
        y_obs = []

        for _ in range(self.n_initial_points):
            vec = rng.uniform(0, 1, n_dims)
            params = self._vector_to_params(vec)
            score = evaluate(params)
            X_obs.append(vec)
            y_obs.append(score)
            if score > self.best_score_:
                self.best_score_ = score
                self.best_params_ = params

        X_obs = np.array(X_obs)
        y_obs = np.array(y_obs)

        for _ in range(self.n_iter - self.n_initial_points):
            mu, std = self._gp_predict(X_obs, y_obs, X_obs)
            n_candidates = 100
            candidates = rng.uniform(0, 1, (n_candidates, n_dims))
            mu_cand, std_cand = self._gp_predict(X_obs, y_obs, candidates)
            ei = self._expected_improvement(mu_cand, std_cand, np.max(y_obs))

            next_vec = candidates[np.argmax(ei)]
            next_params = self._vector_to_params(next_vec)
            next_score = evaluate(next_params)

            X_obs = np.vstack([X_obs, next_vec])
            y_obs = np.append(y_obs, next_score)

            if next_score > self.best_score_:
                self.best_score_ = next_score
                self.best_params_ = next_params

        return self


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Hyperparameter Tuning ===")

    np.random.seed(42)
    n_samples = 150

    X = np.random.randn(n_samples, 4)
    y = ((X[:, 0] + X[:, 1] - X[:, 2]) > 0).astype(int)

    # Import logistic regression
    try:
        from ..linear_model.logistic_regression import LogisticRegression
    except ImportError:
        import sys, os
        _dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if _dir not in sys.path:
            sys.path.insert(0, _dir)
        from linear_model.logistic_regression import LogisticRegression

    # --- GridSearchCV ---
    lr = LogisticRegression(fit_intercept=True, max_iter=5000)
    param_grid = {
        "fit_intercept": [True, False],
        "alpha": [0.0, 0.1, 1.0],
        "learning_rate": [0.01, 0.1],
    }

    gs = GridSearchCV(lr, param_grid, cv=3, scoring="accuracy")
    gs.fit(X, y)
    print(f"  GridSearch best params: {gs.best_params_}")
    print(f"  GridSearch best score: {gs.best_score_:.4f}")
    assert gs.best_params_ is not None
    assert gs.best_score_ > 0.5
    y_pred = gs.predict(X)
    assert len(y_pred) == n_samples
    print("  GridSearchCV: PASS")

    # --- RandomizedSearchCV ---
    lr2 = LogisticRegression(fit_intercept=True, max_iter=5000)
    param_dist = {
        "alpha": (0.0, 5.0),
        "learning_rate": [0.001, 0.01, 0.1, 0.5],
    }

    rs = RandomizedSearchCV(lr2, param_dist, n_iter=8, cv=3,
                            scoring="accuracy", random_state=42)
    rs.fit(X, y)
    print(f"  RandomSearch best params: {rs.best_params_}")
    print(f"  RandomSearch best score: {rs.best_score_:.4f}")
    assert rs.best_params_ is not None
    assert rs.best_score_ > 0.5
    print("  RandomizedSearchCV: PASS")

    # --- BayesianOptimSearch ---
    lr3 = LogisticRegression(fit_intercept=True, max_iter=5000)
    param_bounds = {
        "alpha": (0.0, 5.0),
        "learning_rate": [0.01, 0.05, 0.1, 0.5],
    }

    bo = BayesianOptimSearch(lr3, param_bounds, n_iter=10,
                             n_initial_points=3, cv=3,
                             scoring="accuracy", random_state=42)
    bo.fit(X, y)
    print(f"  Bayesian opt best params: {bo.best_params_}")
    print(f"  Bayesian opt best score: {bo.best_score_:.4f}")
    assert bo.best_params_ is not None
    assert bo.best_score_ > 0.5
    print("  BayesianOptimSearch: PASS")

    print("All Hyperparameter Tuning tests PASSED!\n")
