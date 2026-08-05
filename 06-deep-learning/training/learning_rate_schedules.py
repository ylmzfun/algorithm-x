"""Learning rate schedules implemented as callable classes.

Each schedule implements __call__(epoch) → lr.
"""

import numpy as np
from typing import Optional


class StepDecay:
    """Step decay: lr = initial_lr * gamma^(epoch // step_size)."""

    def __init__(self, initial_lr: float, step_size: int, gamma: float = 0.1):
        """
        Args:
            initial_lr: Starting learning rate.
            step_size: Number of epochs between each decay step.
            gamma: Multiplicative decay factor.
        """
        self.initial_lr = initial_lr
        self.step_size = step_size
        self.gamma = gamma

    def __call__(self, epoch: int) -> float:
        return self.initial_lr * (self.gamma ** (epoch // self.step_size))


class ExponentialDecay:
    """Exponential decay: lr = initial_lr * exp(-decay_rate * epoch)."""

    def __init__(self, initial_lr: float, decay_rate: float = 0.1):
        """
        Args:
            initial_lr: Starting learning rate.
            decay_rate: Decay rate parameter.
        """
        self.initial_lr = initial_lr
        self.decay_rate = decay_rate

    def __call__(self, epoch: int) -> float:
        return self.initial_lr * np.exp(-self.decay_rate * epoch)


class CosineAnnealing:
    """Cosine annealing: lr = lr_min + 0.5*(lr_max - lr_min)*(1 + cos(π*epoch/T_max))."""

    def __init__(self, lr_max: float, lr_min: float, T_max: int):
        """
        Args:
            lr_max: Maximum (initial) learning rate.
            lr_min: Minimum learning rate.
            T_max: Number of epochs for a full cosine cycle.
        """
        self.lr_max = lr_max
        self.lr_min = lr_min
        self.T_max = T_max

    def __call__(self, epoch: int) -> float:
        if epoch >= self.T_max:
            return self.lr_min
        return self.lr_min + 0.5 * (self.lr_max - self.lr_min) * (
            1 + np.cos(np.pi * min(epoch, self.T_max) / self.T_max)
        )


class WarmupCosineDecay:
    """Linear warmup followed by cosine decay.

    - For epoch < warmup_epochs: linear increase from 0 to lr_max.
    - For epoch >= warmup_epochs: cosine decay from lr_max to lr_min.
    """

    def __init__(
        self,
        lr_max: float,
        lr_min: float,
        warmup_epochs: int,
        total_epochs: int,
    ):
        """
        Args:
            lr_max: Peak learning rate after warmup.
            lr_min: Minimum learning rate at end.
            warmup_epochs: Number of warmup epochs.
            total_epochs: Total number of epochs.
        """
        self.lr_max = lr_max
        self.lr_min = lr_min
        self.warmup_epochs = warmup_epochs
        self.total_epochs = total_epochs

    def __call__(self, epoch: int) -> float:
        if epoch < self.warmup_epochs:
            # Linear warmup
            return self.lr_max * (epoch + 1) / self.warmup_epochs
        else:
            # Cosine decay
            t = epoch - self.warmup_epochs
            T = self.total_epochs - self.warmup_epochs
            if t >= T:
                return self.lr_min
            return self.lr_min + 0.5 * (self.lr_max - self.lr_min) * (
                1 + np.cos(np.pi * t / T)
            )


class CyclicLR:
    """Triangular cyclic learning rate.

    Cycles between base_lr and max_lr with triangular pattern.
    """

    def __init__(
        self,
        base_lr: float,
        max_lr: float,
        step_size_up: int,
        step_size_down: Optional[int] = None,
    ):
        """
        Args:
            base_lr: Minimum learning rate.
            max_lr: Maximum learning rate.
            step_size_up: Number of epochs to go from base_lr to max_lr.
            step_size_down: Number of epochs to go from max_lr to base_lr.
                            Defaults to step_size_up if None.
        """
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.step_size_up = step_size_up
        self.step_size_down = step_size_down if step_size_down is not None else step_size_up
        self.cycle_length = self.step_size_up + self.step_size_down

    def __call__(self, epoch: int) -> float:
        cycle_pos = epoch % self.cycle_length
        if cycle_pos < self.step_size_up:
            # Increasing phase
            return self.base_lr + (self.max_lr - self.base_lr) * (cycle_pos / self.step_size_up)
        else:
            # Decreasing phase
            pos = cycle_pos - self.step_size_up
            return self.max_lr - (self.max_lr - self.base_lr) * (pos / self.step_size_down)


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing Learning Rate Schedules...")

    # Test 1: StepDecay
    sd = StepDecay(initial_lr=0.1, step_size=30, gamma=0.1)
    assert abs(sd(0) - 0.1) < 1e-10
    assert abs(sd(29) - 0.1) < 1e-10
    assert abs(sd(30) - 0.01) < 1e-10
    assert abs(sd(60) - 0.001) < 1e-10
    print("  PASS: StepDecay values correct")

    # Test 2: ExponentialDecay
    ed = ExponentialDecay(initial_lr=1.0, decay_rate=0.5)
    assert abs(ed(0) - 1.0) < 1e-10
    assert abs(ed(1) - np.exp(-0.5)) < 1e-10
    assert ed(10) < ed(0), "Should decay over time"
    print("  PASS: ExponentialDecay values correct")

    # Test 3: CosineAnnealing
    ca = CosineAnnealing(lr_max=0.1, lr_min=0.001, T_max=100)
    assert abs(ca(0) - 0.1) < 1e-6, f"Cosine start: {ca(0)}"
    assert abs(ca(50) - (0.001 + 0.5 * 0.099 * (1 + np.cos(np.pi * 0.5)))) < 1e-6
    assert abs(ca(100) - 0.001) < 1e-6, f"Cosine end: {ca(100)}"
    print("  PASS: CosineAnnealing values correct")

    # Test 4: WarmupCosineDecay
    wcd = WarmupCosineDecay(lr_max=0.1, lr_min=0.0, warmup_epochs=10, total_epochs=100)
    assert abs(wcd(0) - 0.01) < 1e-6, f"Warmup step 1: {wcd(0)}"
    assert abs(wcd(9) - 0.1) < 1e-6, f"Warmup end: {wcd(9)}"
    assert abs(wcd(10) - 0.1) < 1e-6, f"Cosine start: {wcd(10)}"
    assert abs(wcd(100) - 0.0) < 1e-6, f"Cosine end: {wcd(100)}"
    print("  PASS: WarmupCosineDecay values correct")

    # Test 5: CyclicLR
    clr = CyclicLR(base_lr=0.001, max_lr=0.1, step_size_up=10, step_size_down=20)
    assert abs(clr(0) - 0.001) < 1e-6, f"Cycle start: {clr(0)}"
    assert abs(clr(10) - 0.1) < 1e-6, f"Cycle peak: {clr(10)}"
    assert abs(clr(30) - 0.001) < 1e-6, f"Cycle end: {clr(30)}"
    assert abs(clr(31) - clr(1)) < 1e-6, f"Cycle repeat: {clr(31)} vs {clr(1)}"
    print("  PASS: CyclicLR values correct")

    # Test 6: Monotonicity
    schedules = [
        ("StepDecay", StepDecay(1.0, 10, 0.5)),
        ("ExponentialDecay", ExponentialDecay(1.0, 0.1)),
        ("CosineAnnealing", CosineAnnealing(1.0, 0.0, 50)),
    ]
    for name, sched in schedules:
        lrs = [sched(e) for e in range(50)]
        # Should be non-increasing (or non-decreasing for cosine at the start)
        if name == "CosineAnnealing":
            assert lrs[0] >= lrs[-1], f"{name}: should end lower"
        else:
            for i in range(1, len(lrs)):
                assert lrs[i] <= lrs[i - 1] + 1e-10, f"{name}: not monotonic at {i}"
    print("  PASS: Monotonicity verified")

    # Test 7: Visualization (optional)
    try:
        import matplotlib.pyplot as plt

        epochs = np.arange(200)
        schedules_vis = {
            "StepDecay": StepDecay(0.1, 40, 0.5),
            "ExponentialDecay": ExponentialDecay(0.1, 0.02),
            "CosineAnnealing": CosineAnnealing(0.1, 0.001, 200),
            "WarmupCosineDecay": WarmupCosineDecay(0.1, 0.0, 20, 200),
            "CyclicLR": CyclicLR(0.001, 0.1, 30, 50),
        }

        fig, axes = plt.subplots(2, 3, figsize=(15, 8))
        axes = axes.flatten()
        for ax, (name, sched) in zip(axes, schedules_vis.items()):
            lrs = [sched(e) for e in epochs]
            ax.plot(epochs, lrs)
            ax.set_title(name)
            ax.set_xlabel("Epoch")
            ax.set_ylabel("LR")
            ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig("/tmp/lr_schedules.png", dpi=100)
        plt.close()
        print("  PASS: Visualization saved to /tmp/lr_schedules.png")
    except ImportError:
        print("  SKIP: matplotlib not available")

    print("\nAll LR Schedule tests passed!")
