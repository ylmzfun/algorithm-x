"""Variational Autoencoder (VAE) from scratch using NumPy.

Architecture: Encoder (μ, log σ²) → Reparameterize → Decoder → Reconstruction
Loss: ELBO = reconstruction_loss + KL_divergence
"""

import numpy as np
from typing import Optional


def reparameterize(mu: np.ndarray, logvar: np.ndarray) -> np.ndarray:
    """Reparameterization trick: z = μ + ε * exp(0.5 * log σ²).

    Args:
        mu: Mean of shape (batch_size, latent_dim).
        logvar: Log variance of shape (batch_size, latent_dim).

    Returns:
        Sampled latent vector z of shape (batch_size, latent_dim).
    """
    eps = np.random.randn(*mu.shape)
    return mu + eps * np.exp(0.5 * logvar)


class Encoder:
    """Encoder network: maps input x → μ, log σ²."""

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int,
        latent_dim: int,
        random_seed: Optional[int] = 42,
    ):
        """Initialize Encoder.

        Args:
            input_dim: Input data dimension.
            hidden_dim: Hidden layer dimension.
            latent_dim: Latent space dimension.
            random_seed: Random seed.
        """
        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / input_dim)
        self.W1 = rng.randn(input_dim, hidden_dim) * scale
        self.b1 = np.zeros(hidden_dim)

        # Two heads: mu and logvar
        self.W_mu = rng.randn(hidden_dim, latent_dim) * scale
        self.b_mu = np.zeros(latent_dim)
        self.W_logvar = rng.randn(hidden_dim, latent_dim) * scale
        self.b_logvar = np.zeros(latent_dim)

        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Encode input to latent parameters.

        Args:
            x: Input of shape (batch_size, input_dim).

        Returns:
            Tuple of (mu, logvar), each of shape (batch_size, latent_dim).
        """
        a1 = np.maximum(0, np.dot(x, self.W1) + self.b1)
        mu = np.dot(a1, self.W_mu) + self.b_mu
        logvar = np.dot(a1, self.W_logvar) + self.b_logvar

        self._cache = {"x": x, "a1": a1, "mu": mu, "logvar": logvar}
        return mu, logvar


class Decoder:
    """Decoder network: maps latent z → reconstructed x̂."""

    def __init__(
        self,
        latent_dim: int,
        hidden_dim: int,
        output_dim: int,
        random_seed: Optional[int] = 42,
    ):
        """Initialize Decoder.

        Args:
            latent_dim: Latent space dimension.
            hidden_dim: Hidden layer dimension.
            output_dim: Output/reconstruction dimension.
            random_seed: Random seed.
        """
        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / latent_dim)
        self.W1 = rng.randn(latent_dim, hidden_dim) * scale
        self.b1 = np.zeros(hidden_dim)
        self.W2 = rng.randn(hidden_dim, output_dim) * scale
        self.b2 = np.zeros(output_dim)
        self._cache: dict = {}

    def forward(self, z: np.ndarray) -> np.ndarray:
        """Decode latent to reconstruction.

        Args:
            z: Latent vector of shape (batch_size, latent_dim).

        Returns:
            Reconstructed output of shape (batch_size, output_dim).
        """
        a1 = np.maximum(0, np.dot(z, self.W1) + self.b1)
        out = np.dot(a1, self.W2) + self.b2  # Linear output (MSE loss)

        self._cache = {"z": z, "a1": a1, "out": out}
        return out


class VAE:
    """Variational Autoencoder.

    Loss = MSE(x, x̂) + β * KL(N(μ, σ²) || N(0, I))
    where KL = -0.5 * sum(1 + log σ² - μ² - σ²)
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dim: int = 32,
        latent_dim: int = 8,
        beta: float = 1.0,
        random_seed: Optional[int] = 42,
    ):
        """Initialize VAE.

        Args:
            input_dim: Input data dimension.
            hidden_dim: Hidden layer dimension.
            latent_dim: Latent space dimension.
            beta: Weight for KL divergence (β-VAE).
            random_seed: Random seed.
        """
        self.input_dim = input_dim
        self.latent_dim = latent_dim
        self.beta = beta

        self.encoder = Encoder(input_dim, hidden_dim, latent_dim, random_seed=random_seed)
        self.decoder = Decoder(latent_dim, hidden_dim, input_dim,
                               random_seed=random_seed + 100 if random_seed else None)

    def forward(self, x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Full forward pass.

        Args:
            x: Input of shape (batch_size, input_dim).

        Returns:
            Tuple of (x_recon, mu, logvar, z).
        """
        mu, logvar = self.encoder.forward(x)
        z = reparameterize(mu, logvar)
        x_recon = self.decoder.forward(z)
        return x_recon, mu, logvar, z

    @staticmethod
    def kl_divergence(mu: np.ndarray, logvar: np.ndarray) -> np.ndarray:
        """Compute KL divergence: KL(N(μ,σ²) || N(0,1)).

        KL = -0.5 * sum(1 + log σ² - μ² - σ²)

        Args:
            mu: Mean, shape (batch_size, latent_dim).
            logvar: Log variance, shape (batch_size, latent_dim).

        Returns:
            KL divergence per sample, shape (batch_size,).
        """
        return -0.5 * np.sum(1 + logvar - mu ** 2 - np.exp(logvar), axis=1)

    def loss(
        self,
        x: np.ndarray,
        x_recon: np.ndarray,
        mu: np.ndarray,
        logvar: np.ndarray,
    ) -> tuple[float, float, float]:
        """Compute ELBO loss = reconstruction + KL.

        Args:
            x: Original input.
            x_recon: Reconstructed input.
            mu: Encoder mean.
            logvar: Encoder log variance.

        Returns:
            Tuple of (total_loss, recon_loss, kl_loss).
        """
        batch_size = x.shape[0]
        recon_loss = np.mean(np.sum((x - x_recon) ** 2, axis=1))  # MSE
        kl_loss = np.mean(self.kl_divergence(mu, logvar))
        total_loss = recon_loss + self.beta * kl_loss
        return float(total_loss), float(recon_loss), float(kl_loss)

    def sample(self, n_samples: int) -> np.ndarray:
        """Generate samples from prior N(0, I).

        Args:
            n_samples: Number of samples.

        Returns:
            Generated data of shape (n_samples, input_dim).
        """
        z = np.random.randn(n_samples, self.latent_dim)
        return self.decoder.forward(z)

    def reconstruct(self, x: np.ndarray) -> np.ndarray:
        """Reconstruct input.

        Args:
            x: Input of shape (batch_size, input_dim).

        Returns:
            Reconstruction of same shape.
        """
        x_recon, _, _, _ = self.forward(x)
        return x_recon


def generate_toy_data_2d(n_samples: int = 500, random_seed: int = 42) -> np.ndarray:
    """Generate 2D toy data: mixture of 4 Gaussians.

    Args:
        n_samples: Number of samples.
        random_seed: Random seed.

    Returns:
        Data of shape (n_samples, 2).
    """
    rng = np.random.RandomState(random_seed)
    centers = np.array([[2, 2], [-2, 2], [-2, -2], [2, -2]])
    samples_per = n_samples // 4
    data = np.vstack([
        rng.randn(samples_per, 2) * 0.5 + center
        for center in centers
    ])
    return data


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing VAE...")

    np.random.seed(42)

    # Generate data
    data = generate_toy_data_2d(n_samples=500, random_seed=42)
    print(f"  Data shape: {data.shape}")

    # Test 1: Encoder forward
    enc = Encoder(input_dim=2, hidden_dim=16, latent_dim=4, random_seed=42)
    mu, logvar = enc.forward(data[:8])
    assert mu.shape == (8, 4), f"Wrong mu shape: {mu.shape}"
    assert logvar.shape == (8, 4), f"Wrong logvar shape: {logvar.shape}"
    print(f"  PASS: Encoder output shapes: mu={mu.shape}, logvar={logvar.shape}")

    # Test 2: Reparameterize
    z = reparameterize(mu, logvar)
    assert z.shape == (8, 4), f"Wrong z shape: {z.shape}"
    # Different samples should differ (random eps)
    z2 = reparameterize(mu, logvar)
    assert not np.allclose(z, z2), "Reparameterize should produce different samples"
    print(f"  PASS: Reparameterize shape: {z.shape}")

    # Test 3: Decoder forward
    dec = Decoder(latent_dim=4, hidden_dim=16, output_dim=2, random_seed=42)
    x_recon = dec.forward(z)
    assert x_recon.shape == (8, 2), f"Wrong reconstruction shape: {x_recon.shape}"
    print(f"  PASS: Decoder output shape: {x_recon.shape}")

    # Test 4: VAE forward
    vae = VAE(input_dim=2, hidden_dim=16, latent_dim=4, beta=1.0, random_seed=42)
    xr, mu_v, lv_v, z_v = vae.forward(data[:8])
    assert xr.shape == (8, 2), f"Wrong VAE output shape: {xr.shape}"
    print(f"  PASS: VAE output shape: {xr.shape}")

    # Test 5: Loss computation
    total, recon, kl = vae.loss(data[:8], xr, mu_v, lv_v)
    assert total > 0 and np.isfinite(total), f"Invalid loss: {total}"
    print(f"  PASS: Loss: total={total:.4f}, recon={recon:.4f}, kl={kl:.4f}")

    # Test 6: KL divergence is positive
    assert kl > 0, f"KL divergence should be positive, got {kl:.6f}"
    print(f"  PASS: KL divergence positive: {kl:.6f}")

    # Test 7: Sample from prior
    samples = vae.sample(100)
    assert samples.shape == (100, 2), f"Wrong sample shape: {samples.shape}"
    sample_var = np.var(samples, axis=0)
    assert np.all(sample_var > 0), "Samples should have variance"
    print(f"  PASS: Sampled data shape: {samples.shape}, variance: {sample_var}")

    # Test 8: Reconstruct preserves approximate shape
    x_test = data[:16]
    x_test_recon = vae.reconstruct(x_test)
    assert x_test_recon.shape == (16, 2)
    print(f"  PASS: Reconstruction shape: {x_test_recon.shape}")

    # Test 9: Reparameterize gradient check (approx)
    mu_test = np.array([[1.0, 0.0]])
    lv_test = np.array([[np.log(0.5), np.log(0.5)]])
    z_test = reparameterize(mu_test, lv_test)
    # With mu=1, sigma=0.5, most samples should be near 1
    z_many = np.array([reparameterize(mu_test, lv_test) for _ in range(1000)]).reshape(1000, 2)
    z_mean = np.mean(z_many, axis=0)
    z_std = np.std(z_many, axis=0)
    assert np.allclose(z_mean, [1.0, 0.0], atol=0.1), f"z mean wrong: {z_mean}"
    assert np.allclose(z_std, [np.sqrt(0.5), np.sqrt(0.5)], atol=0.1), f"z std wrong: {z_std}"
    print("  PASS: Reparameterize statistics correct")

    print("\nAll VAE tests passed!")
