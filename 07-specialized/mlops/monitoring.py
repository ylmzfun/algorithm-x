"""Simulated model monitoring from scratch.

Implements:
- Data drift detection (two-sample KS test)
- Prediction drift monitoring
- Performance degradation alerts

Reference: The Kolmogorov-Smirnov test is a non-parametric test
for comparing two probability distributions.
"""

from __future__ import annotations

import numpy as np
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# KS Test
# ---------------------------------------------------------------------------

def ks_test(
    reference: np.ndarray, current: np.ndarray
) -> tuple[float, float]:
    """Two-sample Kolmogorov-Smirnov test.

    Computes the KS statistic = sup_x |F_ref(x) - F_cur(x)|.
    In practice, KS stat > 0.05 is often considered indicative of drift.

    Args:
        reference: Reference data samples [N].
        current: Current data samples [M].

    Returns:
        Tuple of (ks_statistic, p_value_approximation).
    """
    ref_sorted = np.sort(reference)
    cur_sorted = np.sort(current)

    n1, n2 = len(ref_sorted), len(cur_sorted)
    all_values = np.sort(np.concatenate([ref_sorted, cur_sorted]))

    # Compute empirical CDFs
    cdf1 = np.searchsorted(ref_sorted, all_values, side="right") / n1
    cdf2 = np.searchsorted(cur_sorted, all_values, side="right") / n2

    ks_stat = float(np.max(np.abs(cdf1 - cdf2)))

    # If no difference, p-value is 1.0
    if ks_stat == 0.0:
        return ks_stat, 1.0

    # Approximate p-value (simplified)
    # Using the asymptotic formula: p ≈ 2 * Σ_{k=1}^{∞} (-1)^{k-1} exp(-2 k^2 λ^2)
    # where λ = (sqrt(n) + 0.12 + 0.11/sqrt(n)) * D
    n_eff = n1 * n2 / (n1 + n2)
    lam = (np.sqrt(n_eff) + 0.12 + 0.11 / np.sqrt(n_eff)) * ks_stat

    # Approximate p-value with first few terms
    p_value = 0.0
    for k in range(1, 101):
        term = (-1) ** (k - 1) * np.exp(-2 * (k * lam) ** 2)
        p_value += term
        if abs(term) < 1e-15:
            break
    p_value = min(1.0, max(0.0, 2.0 * p_value))

    return ks_stat, p_value


# ---------------------------------------------------------------------------
# Data Drift Detector
# ---------------------------------------------------------------------------

@dataclass
class DriftReport:
    """Report for a single drift check.

    Attributes:
        feature_name: Name of the feature checked.
        ks_statistic: KS test statistic.
        p_value: Approximate p-value.
        is_drifted: Whether drift is detected (p < threshold).
        threshold: P-value threshold used.
        timestamp: Time of the check.
    """
    feature_name: str
    ks_statistic: float
    p_value: float
    is_drifted: bool
    threshold: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class DataDriftDetector:
    """Detects data drift between reference and current data distributions.

    Uses the two-sample KS test for each feature independently.

    Attributes:
        reference_data: Reference dataset [N, D].
        feature_names: Names of the features.
        p_threshold: Significance threshold for drift detection.
        history: List of past DriftReports.
    """

    def __init__(
        self,
        reference_data: np.ndarray,
        feature_names: Optional[list[str]] = None,
        p_threshold: float = 0.05,
    ) -> None:
        """Initialize the drift detector with reference data.

        Args:
            reference_data: Reference feature matrix [N, D].
            feature_names: Feature names (auto-generated if None).
            p_threshold: P-value threshold for flagging drift.
        """
        self.reference_data = reference_data
        n_features = reference_data.shape[1]
        self.feature_names = feature_names or [
            f"feature_{i}" for i in range(n_features)
        ]
        self.p_threshold = p_threshold
        self.history: list[DriftReport] = []

    def check_drift(self, current_data: np.ndarray) -> list[DriftReport]:
        """Check for drift between reference and current data.

        Args:
            current_data: Current feature matrix [M, D].

        Returns:
            List of DriftReport, one per feature.
        """
        reports: list[DriftReport] = []
        n_features = self.reference_data.shape[1]

        for i in range(n_features):
            ref_col = self.reference_data[:, i]
            cur_col = current_data[:, i]
            ks_stat, p_val = ks_test(ref_col, cur_col)
            is_drifted = p_val < self.p_threshold

            report = DriftReport(
                feature_name=self.feature_names[i],
                ks_statistic=ks_stat,
                p_value=p_val,
                is_drifted=is_drifted,
                threshold=self.p_threshold,
            )
            reports.append(report)

        self.history.extend(reports)
        return reports

    def get_drifted_features(self) -> list[str]:
        """Get names of features flagged for drift in the most recent check.

        Returns:
            List of drifted feature names.
        """
        if not self.history:
            return []
        # Get reports from the most recent check
        n_features = len(self.feature_names)
        recent = self.history[-n_features:]
        return [r.feature_name for r in recent if r.is_drifted]

    def get_summary(self) -> dict:
        """Get a summary of recent drift status.

        Returns:
            Summary dictionary.
        """
        if not self.history:
            return {"status": "no_data", "drifted_features": []}

        n_features = len(self.feature_names)
        recent = self.history[-n_features:]
        drifted = [r for r in recent if r.is_drifted]
        return {
            "status": "drift_detected" if drifted else "stable",
            "drifted_features": [r.feature_name for r in drifted],
            "total_features": n_features,
            "drifted_count": len(drifted),
            "avg_ks_statistic": float(np.mean([r.ks_statistic for r in recent])),
        }


# ---------------------------------------------------------------------------
# Prediction Drift Monitor
# ---------------------------------------------------------------------------

class PredictionDriftMonitor:
    """Monitors prediction distribution shifts over time.

    Tracks the distribution of model predictions and flags significant
    changes compared to a reference period.

    Attributes:
        reference_predictions: Reference prediction distribution.
        bins: Histogram bins for discretization.
        threshold: JS divergence threshold for drift.
    """

    def __init__(
        self,
        reference_predictions: np.ndarray,
        n_bins: int = 20,
        threshold: float = 0.1,
    ) -> None:
        """Initialize prediction drift monitor.

        Args:
            reference_predictions: Predictions from the reference period [N].
            n_bins: Number of bins for histogram.
            threshold: JS divergence threshold for flagging drift.
        """
        self.reference_predictions = reference_predictions
        self.n_bins = n_bins
        self.threshold = threshold

        # Compute reference histogram
        self.ref_hist, self.bin_edges = np.histogram(
            reference_predictions, bins=n_bins, density=True
        )
        self.history: list[dict] = []

    def check_drift(self, current_predictions: np.ndarray) -> dict:
        """Check for prediction distribution drift.

        Uses Jensen-Shannon divergence between reference and current
        prediction histograms.

        Args:
            current_predictions: Current period predictions [M].

        Returns:
            Dictionary with drift metrics.
        """
        cur_hist, _ = np.histogram(
            current_predictions, bins=self.bin_edges, density=True
        )

        # Jensen-Shannon divergence
        m = 0.5 * (self.ref_hist + cur_hist)
        kl_ref = np.sum(self.ref_hist * np.log(
            (self.ref_hist + 1e-12) / (m + 1e-12)
        ))
        kl_cur = np.sum(cur_hist * np.log(
            (cur_hist + 1e-12) / (m + 1e-12)
        ))
        js_div = float(0.5 * kl_ref + 0.5 * kl_cur)

        result = {
            "js_divergence": js_div,
            "is_drifted": js_div > self.threshold,
            "ref_mean": float(np.mean(self.reference_predictions)),
            "cur_mean": float(np.mean(current_predictions)),
            "mean_shift": float(
                abs(np.mean(current_predictions) - np.mean(self.reference_predictions))
            ),
            "timestamp": datetime.now().isoformat(),
        }
        self.history.append(result)
        return result


# ---------------------------------------------------------------------------
# Performance Monitor
# ---------------------------------------------------------------------------

class PerformanceMonitor:
    """Monitors model performance metrics for degradation.

    Compares recent performance against historical baseline and
    triggers alerts when performance drops significantly.

    Attributes:
        baseline_metrics: Historical performance metrics dict.
        metric_thresholds: Alert thresholds per metric.
        degradation_history: List of past alerts.
    """

    def __init__(
        self,
        baseline_metrics: dict[str, float],
        metric_thresholds: Optional[dict[str, float]] = None,
    ) -> None:
        """Initialize performance monitor.

        Args:
            baseline_metrics: Dict of metric_name → baseline_value.
            metric_thresholds: Dict of metric_name → relative degradation
                              threshold. Default: 5% drop per metric.
        """
        self.baseline_metrics = baseline_metrics
        self.metric_thresholds = metric_thresholds or {
            k: 0.05 for k in baseline_metrics
        }
        self.degradation_history: list[dict] = []

    def check_performance(
        self, current_metrics: dict[str, float]
    ) -> dict:
        """Check for performance degradation.

        Compares each current metric against the baseline and flags
        metrics that have degraded beyond the threshold.

        Args:
            current_metrics: Current evaluation metrics.

        Returns:
            Dictionary with degradation status per metric.
        """
        degradations: dict[str, dict] = {}
        has_degradation = False

        for metric_name, baseline_val in self.baseline_metrics.items():
            if metric_name not in current_metrics:
                continue

            current_val = current_metrics[metric_name]
            rel_change = (current_val - baseline_val) / (abs(baseline_val) + 1e-12)

            # For most metrics, decrease = degradation
            # For error metrics (loss, rmse), increase = degradation
            is_error_metric = any(
                err in metric_name.lower()
                for err in ["loss", "error", "rmse", "mse", "mae"]
            )
            threshold = self.metric_thresholds.get(metric_name, 0.05)

            if is_error_metric:
                degraded = current_val > baseline_val * (1 + threshold)
            else:
                degraded = current_val < baseline_val * (1 - threshold)

            degradations[metric_name] = {
                "baseline": baseline_val,
                "current": current_val,
                "relative_change": rel_change,
                "degraded": degraded,
            }

            if degraded:
                has_degradation = True

        alert = {
            "timestamp": datetime.now().isoformat(),
            "has_degradation": has_degradation,
            "metrics": degradations,
        }
        self.degradation_history.append(alert)
        return alert

    def get_latest_alert(self) -> Optional[dict]:
        """Get the most recent performance check result.

        Returns:
            Latest alert dict, or None.
        """
        return self.degradation_history[-1] if self.degradation_history else None


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing monitoring.py — Model Monitoring")
    print("=" * 60)

    np.random.seed(42)
    all_pass = True

    # Test 1: KS test
    print("\n--- KS Test ---")
    # Same distribution
    a = np.random.randn(1000)
    b = np.random.randn(1000)
    ks_same, p_same = ks_test(a, b)
    print(f"  Same distribution: KS={ks_same:.4f}, p={p_same:.4f}")
    same_ok = p_same > 0.05  # Should NOT be significant
    all_pass = all_pass and same_ok

    # Different distributions
    c = np.random.randn(1000) + 1.0  # Shifted mean
    ks_diff, p_diff = ks_test(a, c)
    print(f"  Different distribution: KS={ks_diff:.4f}, p={p_diff:.4f}")
    diff_ok = p_diff < 0.05  # Should be significant
    print(f"  Same not significant: {same_ok}, Different significant: {diff_ok}")
    all_pass = all_pass and diff_ok

    # Test 2: Data Drift Detection
    print("\n--- Data Drift Detection ---")
    # Reference data
    ref_data = np.random.randn(500, 5)
    feature_names = ["age", "income", "score", "clicks", "time"]

    detector = DataDriftDetector(
        reference_data=ref_data,
        feature_names=feature_names,
        p_threshold=0.05,
    )

    # Current data with drift in feature 2 and 3
    cur_data = ref_data.copy()
    cur_data[:, 2] += 0.8  # Shift feature 2
    cur_data[:, 3] *= 2.0  # Scale feature 3

    reports = detector.check_drift(cur_data)
    print(f"  Drift reports: {len(reports)} features")
    for r in reports:
        flag = "⚠️ DRIFT" if r.is_drifted else "✓ stable"
        print(f"    {r.feature_name}: KS={r.ks_statistic:.4f}, "
              f"p={r.p_value:.4f} — {flag}")

    drifted = detector.get_drifted_features()
    print(f"  Drifted features: {drifted}")
    drift_detected = len(drifted) > 0
    print(f"  Drift detected: {drift_detected}")
    all_pass = all_pass and drift_detected

    # Test 3: Prediction Drift
    print("\n--- Prediction Drift ---")
    ref_preds = np.random.beta(2, 5, size=1000)  # Skewed distribution

    monitor = PredictionDriftMonitor(
        reference_predictions=ref_preds,
        n_bins=20,
        threshold=0.1,
    )

    # Similar predictions
    cur_similar = np.random.beta(2, 5, size=500)
    result_similar = monitor.check_drift(cur_similar)
    print(f"  Similar predictions: JS={result_similar['js_divergence']:.4f}, "
          f"drifted={result_similar['is_drifted']}")

    # Shifted predictions
    cur_shifted = np.random.beta(5, 2, size=500)  # Different distribution
    result_shifted = monitor.check_drift(cur_shifted)
    print(f"  Shifted predictions: JS={result_shifted['js_divergence']:.4f}, "
          f"drifted={result_shifted['is_drifted']}")

    # Shifted should have higher JS divergence
    js_ok = result_shifted["js_divergence"] > result_similar["js_divergence"]
    print(f"  Shifted > Similar JS: {js_ok}")
    all_pass = all_pass and js_ok

    # Test 4: Performance Monitoring
    print("\n--- Performance Monitoring ---")
    baseline = {
        "accuracy": 0.85,
        "rmse": 0.42,
        "f1_score": 0.78,
        "auc": 0.91,
    }
    perf_monitor = PerformanceMonitor(
        baseline_metrics=baseline,
        metric_thresholds={"accuracy": 0.05, "rmse": 0.10,
                           "f1_score": 0.05, "auc": 0.03},
    )

    # Good performance
    good_metrics = {"accuracy": 0.84, "rmse": 0.43, "f1_score": 0.77, "auc": 0.90}
    good_alert = perf_monitor.check_performance(good_metrics)
    print(f"  Good performance: degradation={good_alert['has_degradation']}")
    all_pass = all_pass and not good_alert["has_degradation"]

    # Degraded performance
    bad_metrics = {"accuracy": 0.78, "rmse": 0.55, "f1_score": 0.70, "auc": 0.87}
    bad_alert = perf_monitor.check_performance(bad_metrics)
    print(f"  Bad performance: degradation={bad_alert['has_degradation']}")
    for m, info in bad_alert["metrics"].items():
        flag = "⚠️" if info["degraded"] else "✓"
        print(f"    {m}: {info['baseline']:.3f} → {info['current']:.3f} {flag}")

    degraded_detected = bad_alert["has_degradation"]
    print(f"  Degradation detected: {degraded_detected}")
    all_pass = all_pass and degraded_detected

    # Test 5: Summary
    print("\n--- Drift Summary ---")
    summary = detector.get_summary()
    print(f"  Status: {summary['status']}")
    print(f"  Drifted: {summary['drifted_count']}/{summary['total_features']}")
    summary_ok = summary["status"] == "drift_detected"
    all_pass = all_pass and summary_ok

    print(f"\n{'PASS' if all_pass else 'FAIL'}: monitoring.py")
