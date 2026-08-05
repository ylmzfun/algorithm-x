"""Simple GAN (Generative Adversarial Network) from scratch using NumPy.

Trains on 2D toy data (mixture of 8 Gaussians arranged in a circle).
"""

import numpy as np
from typing import Optional


class Generator:
    """Generator: maps latent noise z → data space."""

    def __init__(
        self,
        z_dim: int = 10,
        hidden_dim: int = 64,
        output_dim: int = 2,
        random_seed: Optional[int] = 42,
    ):
        """Initialize Generator.

        Args:
            z_dim: Latent noise dimension.
            hidden_dim: Hidden layer dimension.
            output_dim: Output (data) dimension.
            random_seed: Random seed.
        """
        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / z_dim)
        self.W1 = rng.randn(z_dim, hidden_dim) * scale
        self.b1 = np.zeros(hidden_dim)
        self.W2 = rng.randn(hidden_dim, hidden_dim) * scale
        self.b2 = np.zeros(hidden_dim)
        self.W3 = rng.randn(hidden_dim, output_dim) * scale
        self.b3 = np.zeros(output_dim)
        self._cache: dict = {}

    def forward(self, z: np.ndarray) -> np.ndarray:
        """Generate data from latent noise.

        Args:
            z: Latent noise of shape (batch_size, z_dim).

        Returns:
            Generated samples of shape (batch_size, output_dim).
        """
        a1 = np.maximum(0, np.dot(z, self.W1) + self.b1)
        a2 = np.maximum(0, np.dot(a1, self.W2) + self.b2)
        out = np.dot(a2, self.W3) + self.b3

        self._cache = {"z": z, "a1": a1, "a2": a2, "out": out}
        return out

    def backward(self, dout: np.ndarray) -> dict:
        """Backward pass.

        Args:
            dout: Gradient w.r.t. generator output.

        Returns:
            Dict of gradients.
        """
        cache = self._cache

        # Layer 3
        dW3 = np.dot(cache["a2"].T, dout)
        db3 = np.sum(dout, axis=0)
        da2 = np.dot(dout, self.W3.T)

        # ReLU
        dz2 = da2 * (cache["a2"] > 0).astype(float)
        dW2 = np.dot(cache["a1"].T, dz2)
        db2 = np.sum(dz2, axis=0)
        da1 = np.dot(dz2, self.W2.T)

        # ReLU
        dz1 = da1 * (cache["a1"] > 0).astype(float)
        dW1 = np.dot(cache["z"].T, dz1)
        db1 = np.sum(dz1, axis=0)

        return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2, "dW3": dW3, "db3": db3}

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate samples.

        Args:
            n_samples: Number of samples to generate.

        Returns:
            Generated data of shape (n_samples, output_dim).
        """
        z = np.random.randn(n_samples, self.W1.shape[0])
        return self.forward(z)


class Discriminator:
    """Discriminator: binary classifier (real vs fake)."""

    def __init__(
        self,
        input_dim: int = 2,
        hidden_dim: int = 64,
        random_seed: Optional[int] = 42,
    ):
        """Initialize Discriminator.

        Args:
            input_dim: Data dimension.
            hidden_dim: Hidden layer dimension.
            random_seed: Random seed.
        """
        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / input_dim)
        self.W1 = rng.randn(input_dim, hidden_dim) * scale
        self.b1 = np.zeros(hidden_dim)
        self.W2 = rng.randn(hidden_dim, hidden_dim) * scale
        self.b2 = np.zeros(hidden_dim)
        self.W3 = rng.randn(hidden_dim, 1) * scale
        self.b3 = np.zeros(1)
        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Classify input as real or fake.

        Args:
            x: Input data of shape (batch_size, input_dim).

        Returns:
            Sigmoid probabilities of shape (batch_size, 1).
        """
        a1 = np.maximum(0, np.dot(x, self.W1) + self.b1)
        a2 = np.maximum(0, np.dot(a1, self.W2) + self.b2)
        z3 = np.dot(a2, self.W3) + self.b3
        out = 1.0 / (1.0 + np.exp(-np.clip(z3, -500, 500)))

        self._cache = {"x": x, "a1": a1, "a2": a2, "z3": z3, "out": out}
        return out

    def backward(self, dout: np.ndarray) -> dict:
        """Backward pass.

        Args:
            dout: Gradient w.r.t. discriminator output.

        Returns:
            Dict of gradients.
        """
        cache = self._cache

        # Sigmoid gradient
        dz3 = dout * cache["out"] * (1 - cache["out"])

        # Layer 3
        dW3 = np.dot(cache["a2"].T, dz3)
        db3 = np.sum(dz3, axis=0)
        da2 = np.dot(dz3, self.W3.T)

        # ReLU
        dz2 = da2 * (cache["a2"] > 0).astype(float)
        dW2 = np.dot(cache["a1"].T, dz2)
        db2 = np.sum(dz2, axis=0)
        da1 = np.dot(dz2, self.W2.T)

        # ReLU
        dz1 = da1 * (cache["a1"] > 0).astype(float)
        dW1 = np.dot(cache["x"].T, dz1)
        db1 = np.sum(dz1, axis=0)

        return {"dW1": dW1, "db1": db1, "dW2": dW2, "db2": db2, "dW3": dW3, "db3": db3}


class GAN:
    """Generative Adversarial Network.

    Trains generator and discriminator in alternating steps.
    """

    def __init__(
        self,
        z_dim: int = 10,
        data_dim: int = 2,
        g_hidden: int = 64,
        d_hidden: int = 64,
        random_seed: Optional[int] = 42,
    ):
        """Initialize GAN.

        Args:
            z_dim: Latent noise dimension.
            data_dim: Data dimension.
            g_hidden: Generator hidden dimension.
            d_hidden: Discriminator hidden dimension.
            random_seed: Random seed.
        """
        self.z_dim = z_dim
        self.generator = Generator(z_dim, g_hidden, data_dim, random_seed=random_seed)
        self.discriminator = Discriminator(data_dim, d_hidden, random_seed=random_seed + 100)

    def train_step(
        self,
        real_data: np.ndarray,
        lr_g: float = 0.001,
        lr_d: float = 0.001,
    ) -> tuple[float, float]:
        """One adversarial training step.

        Args:
            real_data: Real data batch of shape (batch_size, data_dim).
            lr_g: Generator learning rate.
            lr_d: Discriminator learning rate.

        Returns:
            Tuple of (d_loss, g_loss).
        """
        batch_size = real_data.shape[0]

        # --- Discriminator step ---
        # Real data
        d_real = self.discriminator.forward(real_data)
        # Real labels = 1, fake labels = 0
        d_real_loss_grad = -(1.0 / (d_real + 1e-12)) / batch_size  # d(-log(D(x)))/dD = -1/D
        grads_d_real = self.discriminator.backward(d_real_loss_grad)

        # Fake data
        z = np.random.randn(batch_size, self.z_dim)
        fake_data = self.generator.forward(z)
        d_fake = self.discriminator.forward(fake_data)
        # For fake: label = 0, loss = -log(1 - D(G(z)))
        d_fake_loss_grad = (1.0 / (1 - d_fake + 1e-12)) / batch_size
        grads_d_fake = self.discriminator.backward(d_fake_loss_grad)

        # Update discriminator
        for key in grads_d_real:
            param_key = key[1:]  # strip 'd' prefix: "dW1" → "W1"
            val = getattr(self.discriminator, param_key) - lr_d * (grads_d_real[key] + grads_d_fake[key])
            setattr(self.discriminator, param_key, val)

        d_loss = -np.mean(np.log(d_real + 1e-12) + np.log(1 - d_fake + 1e-12))

        # --- Generator step ---
        z2 = np.random.randn(batch_size, self.z_dim)
        fake_data2 = self.generator.forward(z2)
        d_fake2 = self.discriminator.forward(fake_data2)

        # Generator loss: -log(D(G(z))) → gradient: -1/D * dD/dG
        g_loss = -np.mean(np.log(d_fake2 + 1e-12))
        g_grad = -(1.0 / (d_fake2 + 1e-12)) / batch_size

        # Backprop through discriminator
        disc_grads = self.discriminator.backward(g_grad)

        # Backprop gradient through fake_data to generator
        # dL/dxfake = disc_grads["dW1"] contribution... simplified:
        # The gradient w.r.t. fake_data is the discriminator's gradient w.r.t. its input
        d_fake_input = np.dot(disc_grads["dW1"], self.discriminator.W1.T)  # approx
        # Better: chain rule: d(fake_data) from discriminator's backward
        # For simplicity, we compute the discriminator gradient w.r.t. input directly
        cache_d = self.discriminator._cache
        dz3_d = g_grad * cache_d["out"] * (1 - cache_d["out"])
        da2_d = np.dot(dz3_d, self.discriminator.W3.T)
        dz2_d = da2_d * (cache_d["a2"] > 0)
        da1_d = np.dot(dz2_d, self.discriminator.W2.T)
        dz1_d = da1_d * (cache_d["a1"] > 0)
        d_fake = np.dot(dz1_d, self.discriminator.W1.T)

        gen_grads = self.generator.backward(d_fake)

        for key in gen_grads:
            param_key = key[1:]  # strip 'd' prefix: "dW1" → "W1"
            val = getattr(self.generator, param_key) - lr_g * gen_grads[key]
            setattr(self.generator, param_key, val)

        return float(d_loss), float(g_loss)

    def generate(self, n_samples: int) -> np.ndarray:
        """Generate samples.

        Args:
            n_samples: Number of samples.

        Returns:
            Generated data of shape (n_samples, data_dim).
        """
        return self.generator.generate(n_samples)


def generate_toy_data(n_samples: int = 1000, random_seed: int = 42) -> np.ndarray:
    """Generate toy 2D data: 8 Gaussians arranged in a circle.

    Args:
        n_samples: Number of samples.
        random_seed: Random seed.

    Returns:
        Data of shape (n_samples, 2).
    """
    rng = np.random.RandomState(random_seed)
    n_centers = 8
    radius = 5.0
    samples_per_center = n_samples // n_centers

    data = []
    for i in range(n_centers):
        angle = 2 * np.pi * i / n_centers
        center = np.array([radius * np.cos(angle), radius * np.sin(angle)])
        samples = rng.randn(samples_per_center, 2) * 0.3 + center
        data.append(samples)

    return np.vstack(data)


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing GAN...")

    np.random.seed(42)

    # Generate toy data
    real_data = generate_toy_data(n_samples=500, random_seed=42)
    print(f"  Real data shape: {real_data.shape}")

    # Test 1: Generator forward
    gen = Generator(z_dim=10, hidden_dim=32, output_dim=2, random_seed=42)
    z = np.random.randn(8, 10)
    fake = gen.forward(z)
    assert fake.shape == (8, 2), f"Wrong generator shape: {fake.shape}"
    print(f"  PASS: Generator output shape: {fake.shape}")

    # Test 2: Discriminator forward
    disc = Discriminator(input_dim=2, hidden_dim=32, random_seed=42)
    d_out = disc.forward(real_data[:8])
    assert d_out.shape == (8, 1), f"Wrong discriminator shape: {d_out.shape}"
    assert np.all((d_out >= 0) & (d_out <= 1)), "Sigmoid output out of range"
    print(f"  PASS: Discriminator output in [0, 1], shape: {d_out.shape}")

    # Test 3: GAN training step
    gan = GAN(z_dim=10, data_dim=2, g_hidden=32, d_hidden=32, random_seed=42)
    d_loss, g_loss = gan.train_step(real_data[:32], lr_g=0.001, lr_d=0.001)
    assert np.isfinite(d_loss) and np.isfinite(g_loss), "Non-finite losses"
    print(f"  PASS: GAN training step, d_loss={d_loss:.4f}, g_loss={g_loss:.4f}")

    # Test 4: Generator produces diverse outputs
    samples1 = gan.generate(100)
    samples2 = gan.generate(100)
    assert samples1.shape == (100, 2)
    # Generated points should not be identical
    assert not np.allclose(samples1, samples2), "Samples should be different"
    print(f"  PASS: Generator produces diverse samples, shape: {samples1.shape}")

    # Test 5: Training progresses (losses change)
    gan2 = GAN(z_dim=10, data_dim=2, g_hidden=32, d_hidden=32, random_seed=123)
    d_losses, g_losses = [], []
    for _ in range(200):
        idx = np.random.choice(len(real_data), 32)
        dl, gl = gan2.train_step(real_data[idx], lr_g=0.01, lr_d=0.01)
        d_losses.append(dl)
        g_losses.append(gl)

    # Losses should be finite and changing
    assert np.all(np.isfinite(d_losses)), "Non-finite d_losses"
    assert len(set([f"{l:.3f}" for l in d_losses[-10:]])) > 1, "Losses should change"
    print(f"  PASS: Training: d_loss range [{min(d_losses):.4f}, {max(d_losses):.4f}]")

    # Test 6: Generator output variance > 0
    gen_samples = gan2.generate(500)
    gen_var = np.var(gen_samples, axis=0)
    assert np.all(gen_var > 0.01), f"Generator collapsed: var={gen_var}"
    print(f"  PASS: Generator variance: {gen_var}")

    print("\nAll GAN tests passed!")
