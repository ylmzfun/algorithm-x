"""Distributed training concepts and simulations.

Explains DataParallel and DistributedDataParallel (DDP), with
simulated implementations to demonstrate the core ideas.
"""

import numpy as np
from typing import Optional


def explain_data_parallel() -> str:
    """Explain DataParallel concept.

    Returns:
        Explanation string.
    """
    return (
        "DataParallel (DP):\n"
        "  - Single-process, multi-GPU training.\n"
        "  - Model is replicated to each GPU.\n"
        "  - Input batch is split across GPUs (scatter).\n"
        "  - Forward pass runs independently on each GPU.\n"
        "  - Outputs are gathered back to the main GPU.\n"
        "  - Loss is computed on the main GPU.\n"
        "  - Gradients are computed and summed on the main GPU.\n"
        "  - Limitation: GPU 0 has higher memory usage (bottleneck).\n"
    )


def explain_ddp() -> str:
    """Explain DistributedDataParallel concept.

    Returns:
        Explanation string.
    """
    return (
        "DistributedDataParallel (DDP):\n"
        "  - Multi-process, multi-GPU training.\n"
        "  - Each process owns one GPU.\n"
        "  - Model is replicated on each GPU at initialization.\n"
        "  - Each GPU processes its own data shard.\n"
        "  - Gradients are synchronized via all-reduce (averaged).\n"
        "  - No single GPU bottleneck (symmetric).\n"
        "  - Scales better than DataParallel.\n"
        "  - Requires process group initialization (NCCL/GLOO backend).\n"
    )


class DataParallelWrapper:
    """Simulate DataParallel behavior on a single device.

    Demonstrates: scatter inputs across "GPUs", forward on each replica,
    gather outputs.
    """

    def __init__(self, model_weights: list[dict], num_gpus: int = 2):
        """Initialize DataParallel simulation.

        Args:
            model_weights: List of weight dicts (one per GPU replica).
            num_gpus: Number of simulated GPUs.
        """
        self.weights_list = model_weights
        self.num_gpus = num_gpus

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Simulate DataParallel forward pass.

        Args:
            x: Input of shape (batch_size, input_dim).

        Returns:
            Combined output from all GPUs.
        """
        batch_size = x.shape[0]
        chunk_size = batch_size // self.num_gpus
        outputs = []

        for gpu in range(self.num_gpus):
            start = gpu * chunk_size
            end = start + chunk_size if gpu < self.num_gpus - 1 else batch_size
            x_chunk = x[start:end]

            # Simulate forward on GPU gpu
            W = self.weights_list[gpu]["W"]
            b = self.weights_list[gpu]["b"]
            out_chunk = np.dot(x_chunk, W) + b
            outputs.append(out_chunk)

        return np.vstack(outputs)  # Gather outputs


class DDPWrapper:
    """Simulate DistributedDataParallel behavior.

    Demonstrates: independent forward per process, all-reduce gradient sync.
    """

    def __init__(self, model_weights: dict, num_processes: int = 2):
        """Initialize DDP simulation.

        Args:
            model_weights: Single model's weights (replicated).
            num_processes: Number of simulated processes.
        """
        self.weights_list = [
            {k: v.copy() for k, v in model_weights.items()}
            for _ in range(num_processes)
        ]
        self.num_processes = num_processes

    def forward(self, x_list: list[np.ndarray]) -> list[np.ndarray]:
        """Forward pass independently per process.

        Args:
            x_list: List of inputs, one per process.

        Returns:
            List of outputs, one per process.
        """
        outputs = []
        for gpu, x in enumerate(x_list):
            W = self.weights_list[gpu]["W"]
            b = self.weights_list[gpu]["b"]
            out = np.dot(x, W) + b
            outputs.append(out)
        return outputs

    def backward_and_sync(self, grads_list: list[dict]) -> dict:
        """Simulate backward pass with gradient all-reduce.

        Args:
            grads_list: List of gradient dicts, one per process.

        Returns:
            Averaged gradients (after all-reduce).
        """
        # All-reduce: average gradients across all processes
        avg_grads = {}
        for key in grads_list[0]:
            stacked = np.stack([g[key] for g in grads_list])
            avg_grads[key] = np.mean(stacked, axis=0)

        # Apply same averaged gradients to all replicas
        for gpu in range(self.num_processes):
            for key in avg_grads:
                self.weights_list[gpu][key] -= 0.01 * avg_grads[key]

        return avg_grads


def all_reduce_simulation(grads_list: list[dict]) -> dict:
    """Simulate all-reduce by averaging gradients across devices.

    In real DDP, each GPU sends its gradients to all others, and each
    sums/averages them independently. This simulates the averaging step.

    Args:
        grads_list: List of gradient dicts from each device.

    Returns:
        Averaged gradient dict.
    """
    avg_grads = {}
    for key in grads_list[0]:
        stacked = np.stack([g[key] for g in grads_list])
        avg_grads[key] = np.mean(stacked, axis=0)
    return avg_grads


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Distributed Training...")

    np.random.seed(42)

    # Test 1: DataParallel forward shape matches single GPU
    weights = [
        {"W": np.random.randn(10, 5) * 0.1, "b": np.zeros(5)},
        {"W": np.random.randn(10, 5) * 0.1, "b": np.zeros(5)},
    ]
    dp = DataParallelWrapper(weights, num_gpus=2)
    x = np.random.randn(8, 10)
    out_dp = dp.forward(x)

    # Single GPU output
    out_single = np.dot(x, weights[0]["W"]) + weights[0]["b"]
    # Shape should match
    assert out_dp.shape == (8, 5), f"DP output shape wrong: {out_dp.shape}"
    assert out_single.shape == (8, 5)
    print(f"  PASS: DataParallel output shape: {out_dp.shape}")

    # Test 2: DataParallel output differs from single GPU (different weights)
    assert not np.allclose(out_dp, out_single), "DP with different weights should differ"
    print("  PASS: DataParallel with different weights produces different output")

    # Test 3: DDP forward per process
    weights_shared = {"W": np.random.randn(6, 3) * 0.1, "b": np.zeros(3)}
    ddp = DDPWrapper(weights_shared, num_processes=2)
    x_list = [np.random.randn(4, 6), np.random.randn(4, 6)]
    out_list = ddp.forward(x_list)
    assert len(out_list) == 2
    assert out_list[0].shape == (4, 3)
    print(f"  PASS: DDP forward per process: shapes {out_list[0].shape}")

    # Test 4: Gradient all-reduce
    grads_list = [
        {"dW": np.array([[1.0, 2.0], [3.0, 4.0]])},
        {"dW": np.array([[5.0, 6.0], [7.0, 8.0]])},
    ]
    avg = all_reduce_simulation(grads_list)
    expected = np.array([[3.0, 4.0], [5.0, 6.0]])
    assert np.allclose(avg["dW"], expected), f"All-reduce wrong: {avg['dW']}"
    print("  PASS: All-reduce averages gradients correctly")

    # Test 5: All-reduce with 4 devices
    grads_4 = [
        {"dW": np.ones((2, 2)) * i} for i in range(4)
    ]
    avg_4 = all_reduce_simulation(grads_4)
    expected_4 = np.ones((2, 2)) * 1.5  # (0+1+2+3)/4 = 1.5
    assert np.allclose(avg_4["dW"], expected_4), f"4-device all-reduce: {avg_4['dW']}"
    print("  PASS: All-reduce with 4 devices correct")

    # Test 6: DDP backward and sync updates all replicas
    ddp2 = DDPWrapper(weights_shared, num_processes=2)
    before_w = ddp2.weights_list[0]["W"].copy()
    grads = [
        {"W": np.random.randn(6, 3) * 0.1},
        {"W": np.random.randn(6, 3) * 0.1},
    ]
    avg_grads = ddp2.backward_and_sync(grads)
    # Both replicas should be updated identically
    assert np.allclose(ddp2.weights_list[0]["W"], ddp2.weights_list[1]["W"])
    assert not np.allclose(ddp2.weights_list[0]["W"], before_w), "Weights should be updated"
    print("  PASS: DDP sync updates all replicas identically")

    # Test 7: Explanation strings
    dp_explain = explain_data_parallel()
    ddp_explain = explain_ddp()
    assert "DataParallel" in dp_explain
    assert "DistributedDataParallel" in ddp_explain
    assert "all-reduce" in ddp_explain
    print("  PASS: Explanation strings generated")

    # Test 8: Scatter works correctly
    x_big = np.array([[i] * 10 for i in range(10)])
    dp3 = DataParallelWrapper(weights, num_gpus=2)
    out_split = dp3.forward(x_big)
    # First 5 rows use GPU 0 weights, last 5 use GPU 1 weights
    assert out_split.shape == (10, 5)
    print(f"  PASS: Scatter-gather preserves batch: {out_split.shape}")

    print("\nAll Distributed Training tests passed!")
