"""Simple model registry from scratch.

Implements:
- Model versioning with metadata
- Stage transitions (none → staging → production → archived)
- Model listing and comparison
- JSON serialization

Simulates model registries like MLflow Model Registry at a conceptual level.
"""

from __future__ import annotations

import json
import os
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Model Version
# ---------------------------------------------------------------------------

@dataclass
class ModelVersion:
    """A single version of a registered model.

    Attributes:
        name: Model name.
        version: Version string (e.g., "1.0.0").
        stage: Current stage: none, staging, production, archived.
        metrics: Evaluation metrics dict.
        metadata: Arbitrary metadata dict.
        file_path: Path to the model artifact.
        description: Human-readable description.
        created_at: Timestamp.
    """
    name: str
    version: str
    stage: str = "none"
    metrics: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    file_path: str = ""
    description: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def promote_to(self, new_stage: str) -> None:
        """Transition to a new stage.

        Valid transitions:
            none → staging
            staging → production
            staging → archived
            production → archived

        Args:
            new_stage: Target stage ('staging', 'production', or 'archived').

        Raises:
            ValueError: If the transition is invalid.
        """
        valid_transitions = {
            "none": {"staging"},
            "staging": {"production", "archived"},
            "production": {"archived"},
            "archived": set(),
        }

        allowed = valid_transitions.get(self.stage, set())
        if new_stage not in allowed:
            raise ValueError(
                f"Cannot transition from '{self.stage}' to '{new_stage}'. "
                f"Allowed: {allowed}"
            )
        self.stage = new_stage

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "stage": self.stage,
            "metrics": self.metrics,
            "metadata": self.metadata,
            "file_path": self.file_path,
            "description": self.description,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelVersion":
        """Deserialize from dictionary.

        Args:
            data: Serialized model version data.

        Returns:
            ModelVersion instance.
        """
        return cls(
            name=data["name"],
            version=data["version"],
            stage=data.get("stage", "none"),
            metrics=data.get("metrics", {}),
            metadata=data.get("metadata", {}),
            file_path=data.get("file_path", ""),
            description=data.get("description", ""),
            created_at=data.get("created_at", ""),
        )


# ---------------------------------------------------------------------------
# Model Registry
# ---------------------------------------------------------------------------

class ModelRegistry:
    """Manages registered models and their versions.

    Supports:
    - Registering new model versions
    - Stage transitions (staging → production → archived)
    - Querying models by name, stage
    - Comparing versions
    """

    VALID_STAGES = {"none", "staging", "production", "archived"}

    def __init__(self) -> None:
        """Initialize the model registry."""
        # model_name → list of ModelVersion (sorted by creation date)
        self._models: dict[str, list[ModelVersion]] = {}

    def register_model(
        self,
        name: str,
        version: str,
        metrics: Optional[dict] = None,
        metadata: Optional[dict] = None,
        file_path: str = "",
        description: str = "",
    ) -> ModelVersion:
        """Register a new model version.

        Args:
            name: Model name.
            version: Version string.
            metrics: Evaluation metrics.
            metadata: Additional metadata.
            file_path: Path to the model artifact.
            description: Description of this version.

        Returns:
            The registered ModelVersion.

        Raises:
            ValueError: If a version with this string already exists.
        """
        if name not in self._models:
            self._models[name] = []

        # Check for duplicate version
        for mv in self._models[name]:
            if mv.version == version:
                raise ValueError(
                    f"Version '{version}' already exists for model '{name}'"
                )

        mv = ModelVersion(
            name=name,
            version=version,
            metrics=metrics or {},
            metadata=metadata or {},
            file_path=file_path,
            description=description,
        )
        self._models[name].append(mv)
        # Sort by version string (simple semver-like sort)
        self._models[name].sort(key=lambda m: _version_key(m.version))
        return mv

    def get_model(self, name: str) -> list[ModelVersion]:
        """Get all versions of a model.

        Args:
            name: Model name.

        Returns:
            List of ModelVersion sorted by version.

        Raises:
            KeyError: If model not found.
        """
        if name not in self._models:
            raise KeyError(f"Model '{name}' not found in registry")
        return self._models[name]

    def get_version(self, name: str, version: str) -> ModelVersion:
        """Get a specific model version.

        Args:
            name: Model name.
            version: Version string.

        Returns:
            The ModelVersion.

        Raises:
            KeyError: If model or version not found.
        """
        for mv in self.get_model(name):
            if mv.version == version:
                return mv
        raise KeyError(f"Version '{version}' not found for model '{name}'")

    def get_production_model(self, name: str) -> Optional[ModelVersion]:
        """Get the production version of a model.

        Args:
            name: Model name.

        Returns:
            The production ModelVersion, or None.
        """
        if name not in self._models:
            return None
        for mv in self._models[name]:
            if mv.stage == "production":
                return mv
        return None

    def get_latest_version(self, name: str) -> ModelVersion:
        """Get the most recently created version of a model.

        Args:
            name: Model name.

        Returns:
            The latest ModelVersion.
        """
        return self.get_model(name)[-1]

    def promote_to_stage(
        self, name: str, version: str, stage: str
    ) -> ModelVersion:
        """Promote a model version to a new stage.

        If promoting to 'production', the previous production version
        (if any) is automatically archived.

        Args:
            name: Model name.
            version: Version string.
            stage: Target stage.

        Returns:
            The promoted ModelVersion.

        Raises:
            ValueError: If stage is invalid or transition not allowed.
        """
        if stage not in self.VALID_STAGES:
            raise ValueError(f"Invalid stage: '{stage}'. "
                             f"Valid: {self.VALID_STAGES}")

        mv = self.get_version(name, version)

        # If promoting to production, archive the current production version
        if stage == "production":
            current_prod = self.get_production_model(name)
            if current_prod and current_prod.version != version:
                current_prod.stage = "archived"

        mv.promote_to(stage)
        return mv

    def archive_version(self, name: str, version: str) -> ModelVersion:
        """Archive a model version.

        Args:
            name: Model name.
            version: Version string.

        Returns:
            The archived ModelVersion.
        """
        return self.promote_to_stage(name, version, "archived")

    def list_models(self) -> list[str]:
        """List all registered model names.

        Returns:
            List of model names.
        """
        return sorted(self._models.keys())

    def list_versions_by_stage(
        self, name: str, stage: str
    ) -> list[ModelVersion]:
        """List versions of a model filtered by stage.

        Args:
            name: Model name.
            stage: Stage to filter by.

        Returns:
            List of ModelVersion in the given stage.
        """
        return [mv for mv in self.get_model(name) if mv.stage == stage]

    def compare_versions(
        self, name: str, version_a: str, version_b: str
    ) -> dict:
        """Compare two versions of a model.

        Args:
            name: Model name.
            version_a: First version.
            version_b: Second version.

        Returns:
            Comparison dictionary.
        """
        mv_a = self.get_version(name, version_a)
        mv_b = self.get_version(name, version_b)

        all_metrics = set(mv_a.metrics.keys()) | set(mv_b.metrics.keys())
        metric_comparison: dict[str, dict] = {}
        for m in all_metrics:
            metric_comparison[m] = {
                version_a: mv_a.metrics.get(m),
                version_b: mv_b.metrics.get(m),
            }

        return {
            "model": name,
            "versions": [version_a, version_b],
            "stages": {version_a: mv_a.stage, version_b: mv_b.stage},
            "metrics": metric_comparison,
        }

    def to_dict(self) -> dict:
        """Serialize registry to dictionary."""
        return {
            name: [mv.to_dict() for mv in versions]
            for name, versions in self._models.items()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ModelRegistry":
        """Deserialize registry from dictionary.

        Args:
            data: Serialized registry.

        Returns:
            ModelRegistry instance.
        """
        registry = cls()
        for name, versions in data.items():
            registry._models[name] = [
                ModelVersion.from_dict(v) for v in versions
            ]
        return registry


def _version_key(v: str) -> tuple:
    """Parse a semver-like version string for sorting."""
    try:
        parts = v.split(".")
        return tuple(int(p) for p in parts)
    except (ValueError, AttributeError):
        return (0,)


# ---------------------------------------------------------------------------
# Serialization
# ---------------------------------------------------------------------------

def save_registry(registry: ModelRegistry, filepath: str) -> None:
    """Save model registry to JSON.

    Args:
        registry: ModelRegistry instance.
        filepath: Output file path.
    """
    with open(filepath, "w") as f:
        json.dump(registry.to_dict(), f, indent=2)


def load_registry(filepath: str) -> ModelRegistry:
    """Load model registry from JSON.

    Args:
        filepath: Input file path.

    Returns:
        ModelRegistry instance.
    """
    with open(filepath, "r") as f:
        data = json.load(f)
    return ModelRegistry.from_dict(data)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing model_registry.py — Model Registry")
    print("=" * 60)

    all_pass = True

    # Create registry
    registry = ModelRegistry()

    # Register model versions
    v1 = registry.register_model(
        name="recommender",
        version="1.0.0",
        metrics={"rmse": 0.95, "precision@10": 0.72},
        metadata={"framework": "numpy", "training_date": "2024-01-01"},
        description="Initial baseline model",
    )

    v2 = registry.register_model(
        name="recommender",
        version="1.1.0",
        metrics={"rmse": 0.88, "precision@10": 0.76},
        metadata={"framework": "numpy", "training_date": "2024-02-01"},
        description="Added feature interactions",
    )

    v3 = registry.register_model(
        name="recommender",
        version="2.0.0",
        metrics={"rmse": 0.82, "precision@10": 0.81},
        metadata={"framework": "numpy", "training_date": "2024-03-01"},
        description="Deep learning model",
    )

    print(f"\nRegistered 3 versions of 'recommender'")

    # Test 1: List models
    print("\n--- List Models ---")
    models = registry.list_models()
    print(f"  Models: {models}")
    list_ok = "recommender" in models
    all_pass = all_pass and list_ok

    # Test 2: Stage promotions
    print("\n--- Stage Transitions ---")
    # Promote v1 to staging
    registry.promote_to_stage("recommender", "1.0.0", "staging")
    v1_stage = registry.get_version("recommender", "1.0.0").stage
    print(f"  v1.0.0 stage: {v1_stage} (expected staging)")
    all_pass = all_pass and v1_stage == "staging"

    # Promote v2 to staging then production
    registry.promote_to_stage("recommender", "1.1.0", "staging")
    registry.promote_to_stage("recommender", "1.1.0", "production")
    v2_stage = registry.get_version("recommender", "1.1.0").stage
    print(f"  v1.1.0 stage: {v2_stage} (expected production)")
    all_pass = all_pass and v2_stage == "production"

    # Get production model
    prod = registry.get_production_model("recommender")
    print(f"  Production version: {prod.version if prod else 'None'}")
    prod_ok = prod is not None and prod.version == "1.1.0"
    all_pass = all_pass and prod_ok

    # Promote v3 to staging then production (should archive v2)
    registry.promote_to_stage("recommender", "2.0.0", "staging")
    registry.promote_to_stage("recommender", "2.0.0", "production")
    v3_stage = registry.get_version("recommender", "2.0.0").stage
    v2_after = registry.get_version("recommender", "1.1.0").stage
    print(f"  v2.0.0 stage: {v3_stage} (expected production)")
    print(f"  v1.1.0 stage after: {v2_after} (expected archived)")
    all_pass = all_pass and v3_stage == "production"
    all_pass = all_pass and v2_after == "archived"

    # Test 3: Invalid transition
    print("\n--- Invalid Transition ---")
    # Try promoting archived v1.1.0 directly to production — should fail
    try:
        registry.promote_to_stage("recommender", "1.1.0", "production")
        print("  Archived → production: Should have raised ValueError")
        all_pass = False
    except ValueError as e:
        print(f"  Archived → production rejected: {e}")

    # v1.0.0 (staging) → production is valid (just verifying allowed transitions)
    registry.promote_to_stage("recommender", "1.0.0", "production")
    v1_new = registry.get_version("recommender", "1.0.0").stage
    print(f"  v1.0.0 promoted to: {v1_new}")
    all_pass = all_pass and v1_new == "production"

    # Test 4: Get latest version
    print("\n--- Latest Version ---")
    latest = registry.get_latest_version("recommender")
    print(f"  Latest: {latest.version} (expected 2.0.0)")
    latest_ok = latest.version == "2.0.0"
    all_pass = all_pass and latest_ok

    # Test 5: Compare versions
    print("\n--- Compare Versions ---")
    comp = registry.compare_versions("recommender", "1.0.0", "2.0.0")
    print(f"  Metrics: {comp['metrics']}")
    comp_ok = "rmse" in comp["metrics"]
    all_pass = all_pass and comp_ok

    # Test 6: Duplicate version
    print("\n--- Duplicate Version ---")
    try:
        registry.register_model("recommender", "1.0.0")
        print("  Duplicate should have raised ValueError")
        all_pass = False
    except ValueError as e:
        print(f"  Duplicate rejected: {e}")

    # Test 7: Save and load
    print("\n--- Save/Load ---")
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "registry.json")
        save_registry(registry, path)
        print(f"  Saved to: {path}")

        loaded = load_registry(path)
        loaded_models = loaded.list_models()
        print(f"  Loaded models: {loaded_models}")
        load_ok = "recommender" in loaded_models
        all_pass = all_pass and load_ok

        # Check production model (1.0.0 was promoted last)
        loaded_prod = loaded.get_production_model("recommender")
        if loaded_prod:
            print(f"  Loaded production: {loaded_prod.version}")
            all_pass = all_pass and loaded_prod.version == "1.0.0"
        else:
            print("  Loaded production: None")
            all_pass = False

    print(f"\n{'PASS' if all_pass else 'FAIL'}: model_registry.py")
