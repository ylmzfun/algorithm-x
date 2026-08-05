"""PyTorch fundamentals: tensor operations, autograd, nn.Module, training loop, save/load.

All PyTorch-dependent code wrapped in try/except for graceful degradation.
"""

import numpy as np
from typing import Optional

_HAS_TORCH = False
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset
    _HAS_TORCH = True
except ImportError:
    pass


def tensor_operations_demo() -> dict:
    """Demonstrate basic PyTorch tensor operations.

    Returns:
        Dict with demo results.
    """
    if not _HAS_TORCH:
        return {"status": "torch_not_installed"}

    results = {}

    # Creation
    t1 = torch.tensor([1, 2, 3, 4])
    results["creation"] = t1.tolist()

    # Indexing
    results["indexing"] = t1[1:3].tolist()  # [2, 3]

    # Reshaping
    t2 = torch.arange(12).reshape(3, 4)
    results["reshape"] = t2.shape  # (3, 4)

    # Broadcasting
    t3 = torch.ones(3, 1)
    t4 = torch.ones(1, 4)
    t5 = t3 + t4
    results["broadcast"] = t5.shape  # (3, 4)

    # Device management
    results["device"] = str(t1.device)  # 'cpu'

    # Dtype
    results["dtype"] = str(t1.dtype)  # 'torch.int64'

    return results


def autograd_demo() -> dict:
    """Demonstrate PyTorch autograd.

    Returns:
        Dict with autograd demo results.
    """
    if not _HAS_TORCH:
        return {"status": "torch_not_installed"}

    results = {}

    # Basic autograd
    x = torch.tensor([2.0], requires_grad=True)
    y = x ** 2 + 3 * x + 1  # f(x) = x^2 + 3x + 1
    y.backward()
    # f'(x) = 2x + 3, at x=2: 4+3=7
    results["grad"] = float(x.grad)  # 7.0
    results["grad_correct"] = abs(x.grad.item() - 7.0) < 1e-6

    # Computational graph
    a = torch.tensor([3.0], requires_grad=True)
    b = torch.tensor([2.0], requires_grad=True)
    c = a * b + b ** 2  # c = a*b + b^2
    c.backward()
    results["a_grad"] = float(a.grad)  # ∂c/∂a = b = 2
    results["b_grad"] = float(b.grad)  # ∂c/∂b = a + 2b = 3+4 = 7

    # no_grad context
    with torch.no_grad():
        d = a * b
    results["no_grad_requires"] = not d.requires_grad  # True

    return results


class SimpleModule(nn.Module if _HAS_TORCH else object):
    """Simple MLP using nn.Module pattern."""

    def __init__(self, input_dim: int = 10, hidden_dim: int = 32, output_dim: int = 2):
        """Initialize simple MLP.

        Args:
            input_dim: Input feature dimension.
            hidden_dim: Hidden layer dimension.
            output_dim: Output dimension.
        """
        if not _HAS_TORCH:
            raise ImportError("PyTorch required")
        super().__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.fc2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, x: "torch.Tensor") -> "torch.Tensor":
        """Forward pass."""
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return x


def training_loop_template(
    model: "nn.Module",
    train_loader: "DataLoader",
    val_loader: Optional["DataLoader"],
    epochs: int,
    lr: float,
    device: str = "cpu",
) -> dict[str, list[float]]:
    """Complete training loop template.

    Args:
        model: PyTorch model.
        train_loader: Training data loader.
        val_loader: Optional validation data loader.
        epochs: Number of training epochs.
        lr: Learning rate.
        device: Device string ('cpu' or 'cuda').

    Returns:
        Dict with train_losses and val_losses lists.
    """
    if not _HAS_TORCH:
        return {"train_losses": [], "val_losses": []}

    model = model.to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.CrossEntropyLoss()

    train_losses: list[float] = []
    val_losses: list[float] = []

    for epoch in range(epochs):
        # Training
        model.train()
        epoch_loss = 0.0
        for batch_x, batch_y in train_loader:
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)
            optimizer.zero_grad()
            outputs = model(batch_x)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item() * len(batch_x)
        epoch_loss /= len(train_loader.dataset)
        train_losses.append(epoch_loss)

        # Validation
        if val_loader is not None:
            model.eval()
            val_loss = 0.0
            with torch.no_grad():
                for batch_x, batch_y in val_loader:
                    batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                    outputs = model(batch_x)
                    loss = criterion(outputs, batch_y)
                    val_loss += loss.item() * len(batch_x)
            val_loss /= len(val_loader.dataset)
            val_losses.append(val_loss)

    return {"train_losses": train_losses, "val_losses": val_losses}


def save_load_demo(
    model: "nn.Module",
    path: str = "/tmp/model_demo.pt",
) -> dict:
    """Demonstrate model save and load.

    Args:
        model: PyTorch model to save.
        path: File path for saving.

    Returns:
        Dict with demo results.
    """
    if not _HAS_TORCH:
        return {"status": "torch_not_installed"}

    import os

    # Save state dict
    torch.save(model.state_dict(), path)
    file_size = os.path.getsize(path)

    # Load
    loaded_state = torch.load(path, weights_only=True)

    # Create new model and load state
    model2 = SimpleModule()
    model2.load_state_dict(loaded_state)
    model2.eval()

    # Verify parameters match
    params_match = all(
        torch.allclose(p1, p2)
        for p1, p2 in zip(model.parameters(), model2.parameters())
    )

    # Cleanup
    os.remove(path)

    return {
        "file_size": file_size,
        "params_match": params_match,
        "save_load_ok": params_match,
    }


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    if not _HAS_TORCH:
        print("SKIP: PyTorch not installed. Install with: pip install torch")
        exit(0)

    print("Testing PyTorch Basics...")

    # Test 1: Tensor operations
    results = tensor_operations_demo()
    assert results["reshape"] == torch.Size([3, 4])
    assert results["broadcast"] == torch.Size([3, 4])
    print("  PASS: Tensor operations")

    # Test 2: Autograd
    auto_results = autograd_demo()
    assert auto_results["grad_correct"]
    assert abs(auto_results["a_grad"] - 2.0) < 1e-6
    assert abs(auto_results["b_grad"] - 7.0) < 1e-6
    print("  PASS: Autograd gradient computation")

    # Test 3: nn.Module forward
    model = SimpleModule()
    x = torch.randn(8, 10)
    out = model(x)
    assert out.shape == (8, 2), f"Wrong output shape: {out.shape}"
    n_params = sum(p.numel() for p in model.parameters())
    print(f"  PASS: nn.Module forward shape: {out.shape}, params: {n_params}")

    # Test 4: Training loop template
    X_train = torch.randn(100, 10)
    y_train = torch.randint(0, 2, (100,))
    X_val = torch.randn(20, 10)
    y_val = torch.randint(0, 2, (20,))

    train_dataset = TensorDataset(X_train, y_train)
    val_dataset = TensorDataset(X_val, y_val)
    train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=16)

    model2 = SimpleModule()
    metrics = training_loop_template(model2, train_loader, val_loader, epochs=5, lr=0.01)
    assert len(metrics["train_losses"]) == 5
    assert len(metrics["val_losses"]) == 5
    assert metrics["train_losses"][-1] < metrics["train_losses"][0], "Loss should decrease"
    print(f"  PASS: Training loop: loss {metrics['train_losses'][0]:.4f} → {metrics['train_losses'][-1]:.4f}")

    # Test 5: Save/load
    demo_result = save_load_demo(model)
    assert demo_result["save_load_ok"], "Save/load failed"
    print(f"  PASS: Save/load: {demo_result['file_size']} bytes, params match: {demo_result['params_match']}")

    # Test 6: Device management
    t = torch.tensor([1.0, 2.0, 3.0])
    assert str(t.device) == "cpu"
    print("  PASS: Device is CPU")

    print("\nAll PyTorch Basics tests passed!")
