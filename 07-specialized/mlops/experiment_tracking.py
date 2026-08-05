"""Simple experiment tracker from scratch.

Implements:
- Experiment runs with hyperparameters, metrics, artifacts
- Query and compare runs
- JSON serialization

This simulates tools like MLflow, Weights & Biases, or TensorBoard
at a conceptual level.
"""

from __future__ import annotations

import numpy as np
import json
import os
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Experiment Run
# ---------------------------------------------------------------------------

@dataclass
class ExperimentRun:
    """A single experiment run.

    Attributes:
        run_id: Unique run identifier.
        name: Human-readable run name.
        hyperparams: Dictionary of hyperparameter name → value.
        metrics: Dictionary of metric name → list of values (per step).
        artifacts: Dictionary of artifact name → file path.
        tags: List of string tags for filtering.
        status: Run status (running, completed, failed).
        created_at: Timestamp of run creation.
    """
    run_id: str
    name: str
    hyperparams: dict = field(default_factory=dict)
    metrics: dict[str, list[float]] = field(default_factory=dict)
    artifacts: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    status: str = "running"
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def log_metric(self, name: str, value: float, step: Optional[int] = None) -> None:
        """Log a metric value.

        Args:
            name: Metric name.
            value: Metric value.
            step: Optional step number (appended to list if None).
        """
        if name not in self.metrics:
            self.metrics[name] = []
        self.metrics[name].append(value)

    def log_metrics(self, metrics_dict: dict[str, float],
                    step: Optional[int] = None) -> None:
        """Log multiple metrics at once.

        Args:
            metrics_dict: Mapping of metric name to value.
            step: Optional step number.
        """
        for name, value in metrics_dict.items():
            self.log_metric(name, value, step)

    def log_hyperparams(self, params: dict) -> None:
        """Log hyperparameters.

        Args:
            params: Dictionary of hyperparameter name → value.
        """
        self.hyperparams.update(params)

    def log_artifact(self, name: str, filepath: str) -> None:
        """Log an artifact.

        Args:
            name: Artifact name.
            filepath: Path to the artifact file.
        """
        self.artifacts[name] = filepath

    def get_best_metric(self, metric_name: str,
                        mode: str = "max") -> float:
        """Get the best (min or max) value of a metric.

        Args:
            metric_name: Name of the metric.
            mode: 'min' or 'max'.

        Returns:
            Best metric value, or -inf/+inf if no data.
        """
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return float("-inf") if mode == "max" else float("inf")
        values = self.metrics[metric_name]
        return max(values) if mode == "max" else min(values)

    def get_final_metric(self, metric_name: str) -> float:
        """Get the last logged value of a metric.

        Args:
            metric_name: Metric name.

        Returns:
            Last metric value, or NaN if no data.
        """
        if metric_name not in self.metrics or not self.metrics[metric_name]:
            return float("nan")
        return self.metrics[metric_name][-1]

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "run_id": self.run_id,
            "name": self.name,
            "hyperparams": self.hyperparams,
            "metrics": self.metrics,
            "artifacts": self.artifacts,
            "tags": self.tags,
            "status": self.status,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExperimentRun":
        """Deserialize from dictionary.

        Args:
            data: Serialized run data.

        Returns:
            ExperimentRun instance.
        """
        return cls(
            run_id=data["run_id"],
            name=data["name"],
            hyperparams=data.get("hyperparams", {}),
            metrics=data.get("metrics", {}),
            artifacts=data.get("artifacts", {}),
            tags=data.get("tags", []),
            status=data.get("status", "completed"),
            created_at=data.get("created_at", ""),
        )


# ---------------------------------------------------------------------------
# Experiment Tracker
# ---------------------------------------------------------------------------

class ExperimentTracker:
    """Manages multiple experiment runs.

    Supports creating runs, logging data, querying, and comparing.

    Attributes:
        runs: Dictionary of run_id → ExperimentRun.
        _counter: Auto-incrementing run ID counter.
    """

    def __init__(self) -> None:
        """Initialize the experiment tracker."""
        self.runs: dict[str, ExperimentRun] = {}
        self._counter: int = 0

    def create_run(
        self,
        name: str,
        hyperparams: Optional[dict] = None,
        tags: Optional[list[str]] = None,
    ) -> ExperimentRun:
        """Create a new experiment run.

        Args:
            name: Run name.
            hyperparams: Initial hyperparameters.
            tags: Optional tags.

        Returns:
            The created ExperimentRun.
        """
        self._counter += 1
        run_id = f"run-{self._counter:04d}"
        run = ExperimentRun(
            run_id=run_id,
            name=name,
            hyperparams=hyperparams or {},
            tags=tags or [],
        )
        self.runs[run_id] = run
        return run

    def get_run(self, run_id: str) -> ExperimentRun:
        """Get a run by ID.

        Args:
            run_id: Run identifier.

        Returns:
            The ExperimentRun.

        Raises:
            KeyError: If run_id not found.
        """
        return self.runs[run_id]

    def query_by_tag(self, tag: str) -> list[ExperimentRun]:
        """Find all runs with a given tag.

        Args:
            tag: Tag to filter by.

        Returns:
            List of matching ExperimentRun objects.
        """
        return [r for r in self.runs.values() if tag in r.tags]

    def query_by_hyperparam(
        self, key: str, value
    ) -> list[ExperimentRun]:
        """Find runs with a specific hyperparameter value.

        Args:
            key: Hyperparameter name.
            value: Expected value.

        Returns:
            List of matching runs.
        """
        return [
            r for r in self.runs.values()
            if key in r.hyperparams and r.hyperparams[key] == value
        ]

    def get_best_run(
        self, metric_name: str, mode: str = "max"
    ) -> Optional[ExperimentRun]:
        """Find the run with the best value of a given metric.

        Args:
            metric_name: Metric to compare.
            mode: 'max' (higher is better) or 'min' (lower is better).

        Returns:
            The best ExperimentRun, or None if no runs have the metric.
        """
        best_run = None
        best_value = float("-inf") if mode == "max" else float("inf")

        for run in self.runs.values():
            if metric_name in run.metrics and run.metrics[metric_name]:
                val = run.get_best_metric(metric_name, mode)
                if (mode == "max" and val > best_value) or \
                   (mode == "min" and val < best_value):
                    best_value = val
                    best_run = run

        return best_run

    def compare_runs(
        self, run_ids: list[str], metric_name: str
    ) -> dict[str, dict]:
        """Compare a set of runs on a specific metric.

        Args:
            run_ids: List of run IDs to compare.
            metric_name: Metric to compare.

        Returns:
            Dictionary mapping run_id → {best_val, final_val, num_steps}.
        """
        result: dict[str, dict] = {}
        for rid in run_ids:
            if rid in self.runs:
                run = self.runs[rid]
                result[rid] = {
                    "name": run.name,
                    "best": run.get_best_metric(metric_name),
                    "final": run.get_final_metric(metric_name),
                    "num_steps": len(run.metrics.get(metric_name, [])),
                    "hyperparams": run.hyperparams,
                }
        return result

    def list_runs(self) -> list[dict]:
        """List summary of all runs.

        Returns:
            List of summary dictionaries.
        """
        return [
            {
                "run_id": r.run_id,
                "name": r.name,
                "status": r.status,
                "tags": r.tags,
            }
            for r in self.runs.values()
        ]

    def to_dict(self) -> dict:
        """Serialize tracker to dictionary."""
        return {
            "runs": {rid: run.to_dict() for rid, run in self.runs.items()},
            "counter": self._counter,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ExperimentTracker":
        """Deserialize tracker from dictionary.

        Args:
            data: Serialized tracker data.

        Returns:
            ExperimentTracker instance.
        """
        tracker = cls()
        for rid, run_data in data.get("runs", {}).items():
            tracker.runs[rid] = ExperimentRun.from_dict(run_data)
        tracker._counter = data.get("counter", len(tracker.runs))
        return tracker


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def save_tracker(tracker: ExperimentTracker, filepath: str) -> None:
    """Save experiment tracker to a JSON file.

    Args:
        tracker: The ExperimentTracker to save.
        filepath: Output file path.
    """
    with open(filepath, "w") as f:
        json.dump(tracker.to_dict(), f, indent=2)


def load_tracker(filepath: str) -> ExperimentTracker:
    """Load experiment tracker from a JSON file.

    Args:
        filepath: Input file path.

    Returns:
        ExperimentTracker instance.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return ExperimentTracker.from_dict(data)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing experiment_tracking.py — Experiment Tracking")
    print("=" * 60)

    all_pass = True

    # Create tracker and runs
    tracker = ExperimentTracker()

    # Run 1: baseline
    run1 = tracker.create_run(
        name="baseline_lr0.01",
        hyperparams={"lr": 0.01, "batch_size": 32, "model": "mlp"},
        tags=["baseline", "mlp"],
    )
    for step in range(10):
        run1.log_metric("loss", 2.0 * np.exp(-0.1 * step) + np.random.randn() * 0.1)
        run1.log_metric("accuracy", 0.5 + 0.04 * step + np.random.randn() * 0.02)

    # Run 2: lr 0.001
    run2 = tracker.create_run(
        name="lr0.001",
        hyperparams={"lr": 0.001, "batch_size": 32, "model": "mlp"},
        tags=["experiment", "mlp"],
    )
    for step in range(10):
        run2.log_metric("loss", 2.5 * np.exp(-0.08 * step) + np.random.randn() * 0.1)
        run2.log_metric("accuracy", 0.5 + 0.03 * step + np.random.randn() * 0.02)

    # Run 3: lr 0.1
    run3 = tracker.create_run(
        name="lr0.1",
        hyperparams={"lr": 0.1, "batch_size": 64, "model": "cnn"},
        tags=["experiment", "cnn"],
    )
    for step in range(10):
        run3.log_metric("loss", 1.8 * np.exp(-0.15 * step) + np.random.randn() * 0.1)
        run3.log_metric("accuracy", 0.5 + 0.05 * step + np.random.randn() * 0.02)

    print(f"\nCreated {len(tracker.runs)} runs")

    # Test 1: Query by tag
    print("\n--- Query by Tag ---")
    mlp_runs = tracker.query_by_tag("mlp")
    print(f"  'mlp' runs: {[r.name for r in mlp_runs]}")
    tag_ok = len(mlp_runs) == 2
    all_pass = all_pass and tag_ok

    # Test 2: Query by hyperparam
    print("\n--- Query by Hyperparam ---")
    lr_runs = tracker.query_by_hyperparam("lr", 0.01)
    print(f"  lr=0.01 runs: {[r.name for r in lr_runs]}")
    hp_ok = len(lr_runs) == 1 and lr_runs[0].name == "baseline_lr0.01"
    all_pass = all_pass and hp_ok

    # Test 3: Get best run by accuracy
    print("\n--- Best Run ---")
    best = tracker.get_best_run("accuracy", mode="max")
    if best:
        best_acc = best.get_best_metric("accuracy", mode="max")
        print(f"  Best run: {best.name} (accuracy={best_acc:.3f})")
    best_ok = best is not None
    all_pass = all_pass and best_ok

    # Test 4: Compare runs
    print("\n--- Compare Runs ---")
    comparison = tracker.compare_runs(
        [run1.run_id, run2.run_id, run3.run_id], "accuracy"
    )
    for rid, info in comparison.items():
        print(f"  {info['name']}: best_acc={info['best']:.3f}, "
              f"final_acc={info['final']:.3f}")
    comp_ok = len(comparison) == 3
    all_pass = all_pass and comp_ok

    # Test 5: Save and load
    print("\n--- Save/Load ---")
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "tracker.json")
        save_tracker(tracker, path)
        print(f"  Saved to: {path}")
        print(f"  File exists: {os.path.exists(path)}")
        all_pass = all_pass and os.path.exists(path)

        loaded = load_tracker(path)
        print(f"  Loaded runs: {len(loaded.runs)}")
        load_ok = len(loaded.runs) == 3
        all_pass = all_pass and load_ok

        # Verify data integrity
        loaded_best = loaded.get_best_run("accuracy", mode="max")
        check_ok = loaded_best is not None
        print(f"  Loaded best run exists: {check_ok}")
        all_pass = all_pass and check_ok

    # Test 6: List runs
    print("\n--- List Runs ---")
    run_list = tracker.list_runs()
    print(f"  Total runs: {len(run_list)}")
    for r in run_list:
        print(f"    {r['run_id']}: {r['name']} [{r['status']}] tags={r['tags']}")

    print(f"\n{'PASS' if all_pass else 'FAIL'}: experiment_tracking.py")
