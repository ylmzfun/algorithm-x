"""Simple ETL data pipeline from scratch.

Implements:
- Data source loading (CSV-like, JSON-like)
- Data transformation (normalize, one-hot encode, missing value handling)
- Schema validation
- Data sink (save processed data)

Simulates a typical ML data pipeline at the conceptual level.
"""

from __future__ import annotations

import numpy as np
import json
import os
from typing import Optional, Any
from dataclasses import dataclass, field
from collections import defaultdict


# ---------------------------------------------------------------------------
# Data Source
# ---------------------------------------------------------------------------

class DataSource:
    """Simulates loading data from various sources.

    Supports CSV-like (structured rows) and JSON-like (dict records) formats.
    """

    @staticmethod
    def from_csv_like(
        data: list[list[Any]],
        columns: list[str],
    ) -> tuple[list[dict], list[str]]:
        """Load data in a CSV-like row format.

        Args:
            data: List of rows, each a list of values.
            columns: Column names.

        Returns:
            Tuple of (records as list of dicts, column names).
        """
        records = []
        for row in data:
            record = {col: row[i] for i, col in enumerate(columns)}
            records.append(record)
        return records, columns

    @staticmethod
    def from_dicts(records: list[dict]) -> tuple[list[dict], list[str]]:
        """Load data from a list of dictionaries.

        Args:
            records: List of record dictionaries.

        Returns:
            Tuple of (records, column names).
        """
        if not records:
            return [], []
        columns = list(records[0].keys())
        return records, columns

    @staticmethod
    def generate_synthetic(
        n_rows: int, columns: list[tuple[str, str]],
        seed: int = 42,
    ) -> tuple[list[dict], list[str]]:
        """Generate synthetic data for testing.

        Args:
            n_rows: Number of rows.
            columns: List of (name, type) pairs, e.g.,
                     [("age", "int"), ("income", "float"), ("city", "cat")].
            seed: Random seed.

        Returns:
            Tuple of (records, column names).
        """
        rng = np.random.default_rng(seed)
        records = []
        col_names = [c[0] for c in columns]

        for _ in range(n_rows):
            record: dict = {}
            for name, dtype in columns:
                if dtype == "int":
                    record[name] = int(rng.integers(0, 100))
                elif dtype == "float":
                    record[name] = float(rng.normal(50, 20))
                elif dtype == "cat":
                    record[name] = str(rng.choice(["A", "B", "C"]))
                else:
                    record[name] = None
            records.append(record)

        # Introduce some missing values
        for record in records:
            if rng.random() < 0.1:
                record[col_names[rng.integers(0, len(col_names))]] = None

        return records, col_names


# ---------------------------------------------------------------------------
# Data Transformer
# ---------------------------------------------------------------------------

class DataTransformer:
    """Applies transformations to data records.

    Supports:
    - Numeric normalization (z-score)
    - One-hot encoding for categorical variables
    - Missing value imputation (mean for numeric, mode for categorical)
    """

    def __init__(self) -> None:
        """Initialize the transformer."""
        self._stats: dict = {}

    def fit_transform(
        self, records: list[dict], columns: list[str]
    ) -> tuple[np.ndarray, list[str]]:
        """Fit transformation parameters and transform the data.

        Args:
            records: List of record dictionaries.
            columns: Column names.

        Returns:
            Tuple of (transformed array [N, D], feature names).
        """
        # Separate numeric and categorical columns
        numeric_cols: list[str] = []
        cat_cols: list[str] = []

        for col in columns:
            values = [r.get(col) for r in records if r.get(col) is not None]
            if not values:
                continue
            if all(isinstance(v, (int, float)) for v in values):
                numeric_cols.append(col)
            else:
                cat_cols.append(col)

        # Compute stats
        self._stats["numeric_cols"] = numeric_cols
        self._stats["cat_cols"] = cat_cols

        # Numeric stats
        for col in numeric_cols:
            vals = [float(r[col]) for r in records if r.get(col) is not None]
            mean_val = np.mean(vals) if vals else 0.0
            std_val = np.std(vals) if vals else 1.0
            self._stats[col] = {"mean": mean_val, "std": max(std_val, 1e-8)}

        # Categorical stats
        for col in cat_cols:
            unique_vals = sorted(set(
                str(r[col]) for r in records if r.get(col) is not None
            ))
            self._stats[col] = {"categories": unique_vals}

        # Transform
        return self.transform(records)

    def transform(
        self, records: list[dict]
    ) -> tuple[np.ndarray, list[str]]:
        """Transform records using fitted statistics.

        Args:
            records: List of record dictionaries.

        Returns:
            Tuple of (transformed array [N, D], feature names).
        """
        numeric_cols = self._stats.get("numeric_cols", [])
        cat_cols = self._stats.get("cat_cols", [])

        n = len(records)
        features: list[np.ndarray] = []
        feature_names: list[str] = []

        # Numeric features
        for col in numeric_cols:
            stats = self._stats[col]
            col_vals = np.array([
                float(r[col]) if r.get(col) is not None else stats["mean"]
                for r in records
            ])
            normalized = (col_vals - stats["mean"]) / stats["std"]
            features.append(normalized.reshape(-1, 1))
            feature_names.append(col)

        # One-hot categorical features
        for col in cat_cols:
            categories = self._stats[col]["categories"]
            one_hot = np.zeros((n, len(categories)))
            mode_val = categories[0] if categories else "UNK"
            for i, r in enumerate(records):
                val = str(r.get(col, mode_val)) if r.get(col) is not None else mode_val
                if val in categories:
                    one_hot[i, categories.index(val)] = 1.0
                else:
                    one_hot[i, 0] = 1.0  # Default to first category
            features.append(one_hot)
            for cat in categories:
                feature_names.append(f"{col}_{cat}")

        if not features:
            return np.zeros((n, 0)), []

        return np.hstack(features), feature_names


# ---------------------------------------------------------------------------
# Schema Validator
# ---------------------------------------------------------------------------

class SchemaValidator:
    """Validates data against an expected schema.

    Checks:
    - Required columns are present
    - Column types match
    - Value ranges (for numeric columns)
    """

    def __init__(
        self,
        required_columns: list[str],
        column_types: dict[str, type],
        value_ranges: Optional[dict[str, tuple[float, float]]] = None,
    ) -> None:
        """Initialize schema validator.

        Args:
            required_columns: Columns that must be present.
            column_types: Expected type for each column.
            value_ranges: Optional (min, max) for numeric columns.
        """
        self.required_columns = required_columns
        self.column_types = column_types
        self.value_ranges = value_ranges or {}

    def validate(self, records: list[dict]) -> tuple[bool, list[str]]:
        """Validate a list of records.

        Args:
            records: List of record dictionaries.

        Returns:
            Tuple of (is_valid, list of error messages).
        """
        errors: list[str] = []

        if not records:
            errors.append("No records provided")
            return False, errors

        for i, record in enumerate(records):
            prefix = f"Row {i}"

            # Check required columns
            for col in self.required_columns:
                if col not in record:
                    errors.append(f"{prefix}: missing required column '{col}'")

            # Check types
            for col, expected_type in self.column_types.items():
                if col in record and record[col] is not None:
                    if not isinstance(record[col], expected_type):
                        errors.append(
                            f"{prefix}: column '{col}' expected "
                            f"{expected_type.__name__}, got "
                            f"{type(record[col]).__name__}"
                        )

            # Check value ranges
            for col, (lo, hi) in self.value_ranges.items():
                if col in record and record[col] is not None:
                    val = record[col]
                    if isinstance(val, (int, float)) and (val < lo or val > hi):
                        errors.append(
                            f"{prefix}: column '{col}' value {val} "
                            f"out of range [{lo}, {hi}]"
                        )

        return len(errors) == 0, errors


# ---------------------------------------------------------------------------
# Data Sink
# ---------------------------------------------------------------------------

class DataSink:
    """Saves processed data to a destination.

    Supports in-memory storage and file-based output.
    """

    def __init__(self) -> None:
        """Initialize data sink."""
        self.saved_data: list[dict] = []

    def save(self, records: list[dict]) -> None:
        """Save records in memory.

        Args:
            records: List of record dictionaries.
        """
        self.saved_data.extend(records)

    def save_to_file(self, records: list[dict], filepath: str) -> None:
        """Save records to a JSON file.

        Args:
            records: Records to save.
            filepath: Output file path.
        """
        with open(filepath, "w") as f:
            json.dump(records, f, indent=2)

    def get_saved(self) -> list[dict]:
        """Get all in-memory saved records.

        Returns:
            List of saved records.
        """
        return self.saved_data


# ---------------------------------------------------------------------------
# ETL Pipeline
# ---------------------------------------------------------------------------

class ETLPipeline:
    """Orchestrates the Extract → Transform → Validate → Load pipeline.

    Attributes:
        source: DataSource instance.
        transformer: DataTransformer instance.
        validator: SchemaValidator instance.
        sink: DataSink instance.
    """

    def __init__(
        self,
        transformer: Optional[DataTransformer] = None,
        validator: Optional[SchemaValidator] = None,
        sink: Optional[DataSink] = None,
    ) -> None:
        """Initialize the ETL pipeline.

        Args:
            transformer: Data transformer.
            validator: Schema validator.
            sink: Data sink.
        """
        self.transformer = transformer or DataTransformer()
        self.validator = validator
        self.sink = sink or DataSink()
        self.logs: list[str] = []

    def run(
        self,
        records: list[dict],
        columns: Optional[list[str]] = None,
    ) -> tuple[np.ndarray, list[str], bool]:
        """Run the full ETL pipeline.

        Args:
            records: Raw data records.
            columns: Column names (inferred if None).

        Returns:
            Tuple of (transformed_array, feature_names, success).
        """
        self.logs = []

        # Extract
        if columns is None and records:
            columns = list(records[0].keys())
        self.logs.append(f"EXTRACT: {len(records)} records, "
                         f"{len(columns) if columns else 0} columns")

        # Validate
        if self.validator:
            valid, errors = self.validator.validate(records)
            self.logs.append(f"VALIDATE: {'PASS' if valid else 'FAIL'}")
            if errors:
                for err in errors[:3]:  # Log first 3 errors
                    self.logs.append(f"  ERROR: {err}")
            if not valid:
                return np.zeros((len(records), 0)), [], False

        # Transform
        X, feature_names = self.transformer.fit_transform(records, columns or [])
        self.logs.append(f"TRANSFORM: {X.shape[0]} rows, "
                         f"{X.shape[1]} features")

        # Load
        self.sink.save(records)
        self.logs.append(f"LOAD: {len(self.sink.get_saved())} records saved")

        return X, feature_names, True


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing data_pipeline.py — ETL Data Pipeline")
    print("=" * 60)

    all_pass = True

    # Generate synthetic data
    columns_def = [
        ("age", "int"),
        ("income", "float"),
        ("score", "float"),
        ("city", "cat"),
    ]
    records, col_names = DataSource.generate_synthetic(
        n_rows=100, columns=columns_def, seed=42
    )
    print(f"\nSynthetic data: {len(records)} records, "
          f"{len(col_names)} columns")
    print(f"  Sample: {records[0]}")

    # Test 1: Schema validation
    print("\n--- Schema Validation ---")
    validator = SchemaValidator(
        required_columns=["age", "income", "score", "city"],
        column_types={"age": int, "income": float, "score": float,
                       "city": str},
        value_ranges={"age": (0, 150)},
    )
    valid, errors = validator.validate(records)
    print(f"  Validation: {'PASS' if valid else 'FAIL'}")
    all_pass = all_pass and valid

    # Test with invalid data
    bad_records = records.copy()
    bad_records.append({"age": -5, "income": 100.0, "score": 50.0, "city": "D"})
    valid2, errors2 = validator.validate(bad_records)
    print(f"  Bad record validation: {'PASS' if valid2 else 'FAIL'}")
    print(f"  Errors: {errors2}")
    # Should have errors for age out of range
    all_pass = all_pass and not valid2

    # Test 2: Transformation
    print("\n--- Data Transformation ---")
    transformer = DataTransformer()
    X, feature_names = transformer.fit_transform(records, col_names)
    print(f"  Transformed shape: {X.shape}")
    print(f"  Feature names: {feature_names}")

    # Verify numeric columns are standardized
    age_col_idx = feature_names.index("age")
    age_mean = np.mean(X[:, age_col_idx])
    age_std = np.std(X[:, age_col_idx])
    print(f"  Age mean: {age_mean:.4f} (expected ~0.0)")
    print(f"  Age std:  {age_std:.4f} (expected ~1.0)")
    norm_ok = abs(age_mean) < 0.1 and abs(age_std - 1.0) < 0.2
    all_pass = all_pass and norm_ok

    # Verify one-hot columns sum to 1 per row
    city_cols = [i for i, n in enumerate(feature_names) if n.startswith("city_")]
    if city_cols:
        city_sum = np.sum(X[:, city_cols], axis=1)
        sums_ok = np.allclose(city_sum, 1.0)
        print(f"  City one-hot rows sum to 1: {sums_ok}")
        all_pass = all_pass and sums_ok

    # Test 3: Full pipeline
    print("\n--- Full ETL Pipeline ---")
    pipeline = ETLPipeline(validator=validator)
    X_out, f_names, success = pipeline.run(records)
    print(f"  Pipeline success: {success}")
    print(f"  Pipeline logs:")
    for log in pipeline.logs:
        print(f"    {log}")
    pipeline_ok = success and len(pipeline.sink.get_saved()) == 100
    all_pass = all_pass and pipeline_ok

    # Test 4: Missing value handling
    print("\n--- Missing Value Handling ---")
    # Introduce some None values
    records_with_nulls = records[:5].copy()
    records_with_nulls[0]["age"] = None
    records_with_nulls[2]["income"] = None
    X_null, _ = transformer.transform(records_with_nulls)
    has_nan = np.any(np.isnan(X_null))
    print(f"  NaN in transformed output: {has_nan} (expected False)")
    all_pass = all_pass and not has_nan

    # Test 5: Save/load sink
    print("\n--- Data Sink ---")
    sink = DataSink()
    sink.save(records[:3])
    print(f"  Saved records: {len(sink.get_saved())}")

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, "output.json")
        sink.save_to_file(records[:3], path)
        print(f"  File saved: {os.path.exists(path)}")
        all_pass = all_pass and os.path.exists(path)

    print(f"\n{'PASS' if all_pass else 'FAIL'}: data_pipeline.py")
