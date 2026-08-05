"""Model export and serialization from scratch.

Implements:
- Simple neural network model with save/load
- NumPy .npz serialization
- JSON-based model architecture + weights export
- Inference with loaded model

In practice, frameworks like PyTorch use TorchScript/ONNX;
this module demonstrates the underlying concepts.
"""

from __future__ import annotations

import numpy as np
import json
import os
from typing import Optional


# ---------------------------------------------------------------------------
# Simple Model
# ---------------------------------------------------------------------------

class SimpleModel:
    """A simple feed-forward neural network for export demonstration.

    Architecture: Input → Hidden (ReLU) → Hidden (ReLU) → Output.

    Attributes:
        layers: List of (W, b) tuples.
        layer_sizes: List of layer dimensions.
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dims: tuple[int, ...] = (64, 32),
        output_dim: int = 10,
        seed: int = 42,
    ) -> None:
        """Initialize the model.

        Args:
            input_dim: Input feature dimension.
            hidden_dims: Hidden layer sizes.
            output_dim: Output dimension.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        dims = [input_dim] + list(hidden_dims) + [output_dim]
        self.layer_sizes = dims
        self.layers: list[tuple[np.ndarray, np.ndarray]] = []

        for i in range(len(dims) - 1):
            fan_in = dims[i]
            fan_out = dims[i + 1]
            scale = np.sqrt(2.0 / fan_in)
            W = rng.normal(0, scale, (fan_in, fan_out))
            b = np.zeros(fan_out)
            self.layers.append((W, b))

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass.

        Args:
            x: Input [B, input_dim] or [input_dim].

        Returns:
            Output [B, output_dim] or [output_dim].
        """
        out = x
        for i, (W, b) in enumerate(self.layers):
            out = out @ W + b
            if i < len(self.layers) - 1:
                out = np.maximum(0, out)  # ReLU
        return out

    def get_weights_dict(self) -> dict:
        """Get all weights as a dictionary.

        Returns:
            Dictionary with keys 'W0', 'b0', 'W1', 'b1', ...
            and 'layer_sizes'.
        """
        result: dict = {"layer_sizes": self.layer_sizes}
        for i, (W, b) in enumerate(self.layers):
            result[f"W{i}"] = W
            result[f"b{i}"] = b
        return result

    def set_weights_dict(self, weights: dict) -> None:
        """Load weights from a dictionary.

        Args:
            weights: Dictionary from get_weights_dict().
        """
        for i in range(len(self.layers)):
            self.layers[i] = (weights[f"W{i}"], weights[f"b{i}"])

    @classmethod
    def from_weights_dict(cls, weights: dict) -> "SimpleModel":
        """Create a model from a weights dictionary.

        Args:
            weights: Dictionary with layer_sizes and weight arrays.

        Returns:
            A new SimpleModel with loaded weights.
        """
        sizes = weights["layer_sizes"]
        model = cls.__new__(cls)
        model.layer_sizes = sizes
        model.layers = []
        i = 0
        while f"W{i}" in weights:
            model.layers.append((weights[f"W{i}"], weights[f"b{i}"]))
            i += 1
        return model


# ---------------------------------------------------------------------------
# NumPy Export
# ---------------------------------------------------------------------------

def export_to_numpy(model: SimpleModel, filepath: str) -> None:
    """Export model weights to a .npz file.

    Args:
        model: The SimpleModel to export.
        filepath: Output file path (should end with .npz).
    """
    weights = model.get_weights_dict()
    # Convert to flat arrays for npz
    save_dict: dict[str, np.ndarray] = {}
    for key, val in weights.items():
        if isinstance(val, np.ndarray):
            save_dict[key] = val
        elif isinstance(val, list):
            save_dict[key] = np.array(val)
    np.savez_compressed(filepath, **save_dict)


def load_from_numpy(filepath: str) -> SimpleModel:
    """Load model weights from a .npz file.

    Args:
        filepath: Input .npz file path.

    Returns:
        A SimpleModel with loaded weights.
    """
    data = np.load(filepath, allow_pickle=True)
    weights: dict = {}
    for key in data.files:
        arr = data[key]
        if arr.ndim == 1 and arr.dtype == object:
            # Likely layer_sizes
            weights[key] = arr.tolist()
        else:
            weights[key] = arr
    data.close()
    return SimpleModel.from_weights_dict(weights)


# ---------------------------------------------------------------------------
# JSON Export
# ---------------------------------------------------------------------------

def export_to_json(model: SimpleModel, filepath: str) -> None:
    """Export model architecture and weights as JSON.

    Args:
        model: The SimpleModel to export.
        filepath: Output JSON file path.
    """
    weights = model.get_weights_dict()
    json_data: dict = {
        "layer_sizes": weights["layer_sizes"],
        "weights": {},
    }
    for key, val in weights.items():
        if key != "layer_sizes":
            json_data["weights"][key] = val.tolist()

    with open(filepath, "w") as f:
        json.dump(json_data, f, indent=2)


def load_from_json(filepath: str) -> SimpleModel:
    """Load model from a JSON file.

    Args:
        filepath: Input JSON file path.

    Returns:
        A SimpleModel with loaded weights.
    """
    with open(filepath, "r") as f:
        data = json.load(f)

    sizes = data["layer_sizes"]
    model = SimpleModel.__new__(SimpleModel)
    model.layer_sizes = sizes
    model.layers = []
    i = 0
    while f"W{i}" in data["weights"]:
        W = np.array(data["weights"][f"W{i}"])
        b = np.array(data["weights"][f"b{i}"])
        model.layers.append((W, b))
        i += 1
    return model


# ---------------------------------------------------------------------------
# Inference helper
# ---------------------------------------------------------------------------

def run_inference(model: SimpleModel, input_data: np.ndarray) -> np.ndarray:
    """Run a forward pass (inference) with the model.

    Args:
        model: The loaded model.
        input_data: Input data.

    Returns:
        Model predictions.
    """
    return model.forward(input_data)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing model_export.py — Model Export")
    print("=" * 60)

    # Create a model
    model = SimpleModel(input_dim=10, hidden_dims=(32, 16), output_dim=5, seed=42)
    test_input = np.random.randn(3, 10)
    original_output = model.forward(test_input)

    print(f"\nModel: input=10, hidden=(32,16), output=5")
    print(f"  Original output shape: {original_output.shape}")

    all_pass = True
    import tempfile

    with tempfile.TemporaryDirectory() as tmpdir:
        # Test 1: NumPy export/import
        print("\n--- NumPy Export ---")
        npz_path = os.path.join(tmpdir, "model.npz")
        export_to_numpy(model, npz_path)
        print(f"  Exported to: {npz_path}")
        print(f"  File exists: {os.path.exists(npz_path)}")
        all_pass = all_pass and os.path.exists(npz_path)

        loaded_np = load_from_numpy(npz_path)
        np_output = loaded_np.forward(test_input)
        np_match = np.allclose(original_output, np_output, rtol=1e-6)
        print(f"  NumPy loaded output matches: {np_match}")
        all_pass = all_pass and np_match

        # Test 2: JSON export/import
        print("\n--- JSON Export ---")
        json_path = os.path.join(tmpdir, "model.json")
        export_to_json(model, json_path)
        print(f"  Exported to: {json_path}")
        print(f"  File exists: {os.path.exists(json_path)}")
        all_pass = all_pass and os.path.exists(json_path)

        loaded_json = load_from_json(json_path)
        json_output = loaded_json.forward(test_input)
        json_match = np.allclose(original_output, json_output, rtol=1e-6)
        print(f"  JSON loaded output matches: {json_match}")
        all_pass = all_pass and json_match

        # Test 3: Verify JSON is human-readable
        with open(json_path, "r") as f:
            content = f.read()
        has_sizes = "layer_sizes" in content
        has_weights = "weights" in content
        print(f"\n  JSON contains 'layer_sizes': {has_sizes}")
        print(f"  JSON contains 'weights': {has_weights}")
        all_pass = all_pass and has_sizes and has_weights

    # Test 4: Inference function
    print("\n--- Inference ---")
    pred = run_inference(model, test_input)
    print(f"  Inference output shape: {pred.shape}")
    all_pass = all_pass and pred.shape == (3, 5)

    print(f"\n{'PASS' if all_pass else 'FAIL'}: model_export.py")
