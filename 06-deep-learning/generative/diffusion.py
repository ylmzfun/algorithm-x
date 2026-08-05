"""Simple DDPM (Denoising Diffusion Probabilistic Model) concept implementation.

Implements:
- Forward diffusion: add noise to data at timestep t
- Simple U-Net-like denoising model (MLP-based)
- Reverse diffusion: iterative denoising from noise
"""

import numpy as np
from typing import Optional


def linear_beta_schedule(num_steps: int, beta_start: float = 1e-4,
                         beta_end: float = 0.02) -> np.ndarray:
    """Linear beta schedule for DDPM.

    Args:
        num_steps: Number of diffusion timesteps.
        beta_start: Starting beta value.
        beta_end: Ending beta value.

    Returns:
        Beta array of shape (num_steps,).
    """
    return np.linspace(beta_start, beta_end, num_steps)


def compute_alphas(betas: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute alpha-related quantities from betas.

    Args:
        betas: Beta schedule of shape (T,).

    Returns:
        Tuple of (alphas, alpha_bars, sqrt_alpha_bars, sqrt_one_minus_alpha_bars).
    """
    alphas = 1.0 - betas
    alpha_bars = np.cumprod(alphas)
    sqrt_alpha_bars = np.sqrt(alpha_bars)
    sqrt_one_minus_alpha_bars = np.sqrt(1.0 - alpha_bars)
    return alphas, alpha_bars, sqrt_alpha_bars, sqrt_one_minus_alpha_bars


def forward_diffusion(
    x_0: np.ndarray,
    t: np.ndarray,
    sqrt_alpha_bars: np.ndarray,
    sqrt_one_minus_alpha_bars: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Add noise to data at timesteps t.

    x_t = sqrt(alpha_bar_t) * x_0 + sqrt(1 - alpha_bar_t) * epsilon

    Args:
        x_0: Clean data of shape (batch_size, data_dim).
        t: Timesteps of shape (batch_size,).
        sqrt_alpha_bars: Precomputed sqrt(alpha_bar_t) of shape (T,).
        sqrt_one_minus_alpha_bars: Precomputed sqrt(1-alpha_bar_t) of shape (T,).

    Returns:
        Tuple of (x_t, noise).
    """
    noise = np.random.randn(*x_0.shape)
    sqrt_alpha = sqrt_alpha_bars[t][:, np.newaxis]
    sqrt_one_minus = sqrt_one_minus_alpha_bars[t][:, np.newaxis]
    x_t = sqrt_alpha * x_0 + sqrt_one_minus * noise
    return x_t, noise


class SimpleUNet:
    """Simplified denoising model (MLP with time embedding).

    Predicts the noise epsilon given noisy input x_t and timestep t.
    """

    def __init__(
        self,
        data_dim: int,
        hidden_dim: int = 64,
        num_steps: int = 200,
        random_seed: Optional[int] = 42,
    ):
        """Initialize SimpleUNet.

        Args:
            data_dim: Data dimension.
            hidden_dim: Hidden layer dimension.
            num_steps: Number of diffusion timesteps (for time embedding).
            random_seed: Random seed.
        """
        self.data_dim = data_dim
        self.num_steps = num_steps

        rng = np.random.RandomState(random_seed)
        scale = np.sqrt(2.0 / data_dim)

        # Time embedding
        self.time_embed = rng.randn(num_steps, data_dim) * 0.02

        # MLP layers
        self.W1 = rng.randn(data_dim + data_dim, hidden_dim) * scale
        self.b1 = np.zeros(hidden_dim)
        self.W2 = rng.randn(hidden_dim, hidden_dim) * scale
        self.b2 = np.zeros(hidden_dim)
        self.W3 = rng.randn(hidden_dim, data_dim) * scale
        self.b3 = np.zeros(data_dim)
        self._cache: dict = {}

    def forward(self, x_t: np.ndarray, t: np.ndarray) -> np.ndarray:
        """Predict noise given noisy input and timestep.

        Args:
            x_t: Noisy input of shape (batch_size, data_dim).
            t: Timesteps of shape (batch_size,).

        Returns:
            Predicted noise of shape (batch_size, data_dim).
        """
        t_embed = self.time_embed[t]  # (batch, data_dim)
        h = np.hstack((x_t, t_embed))  # (batch, 2*data_dim)

        a1 = np.maximum(0, np.dot(h, self.W1) + self.b1)
        a2 = np.maximum(0, np.dot(a1, self.W2) + self.b2)
        out = np.dot(a2, self.W3) + self.b3

        self._cache = {"x_t": x_t, "t": t, "t_embed": t_embed, "h": h,
                       "a1": a1, "a2": a2, "out": out}
        return out

    def backward(self, dout: np.ndarray) -> dict:
        """Backward pass.

        Args:
            dout: Gradient w.r.t. predicted noise.

        Returns:
            Dict of gradients.
        """
        cache = self._cache

        dW3 = np.dot(cache["a2"].T, dout)
        db3 = np.sum(dout, axis=0)
        da2 = np.dot(dout, self.W3.T)

        dz2 = da2 * (cache["a2"] > 0).astype(float)
        dW2 = np.dot(cache["a1"].T, dz2)
        db2 = np.sum(dz2, axis=0)
        da1 = np.dot(dz2, self.W2.T)

        dz1 = da1 * (cache["a1"] > 0).astype(float)
        dW1 = np.dot(cache["h"].T, dz1)
        db1 = np.sum(dz1, axis=0)

        # Time embedding gradients
        d_time_embed = np.zeros_like(self.time_embed)
        # gradient flows through h concatenation
        dh = np.dot(dz1, self.W1.T)
        d_time = dh[:, self.data_dim:]  # time embedding part
        for i in range(len(cache["t"])):
            d_time_embed[cache["t"][i]] += d_time[i]

        return {
            "dW1": dW1, "db1": db1,
            "dW2": dW2, "db2": db2,
            "dW3": dW3, "db3": db3,
            "d_time_embed": d_time_embed,
        }


class DDPM:
    """Denoising Diffusion Probabilistic Model."""

    def __init__(
        self,
        data_dim: int,
        num_steps: int = 200,
        hidden_dim: int = 64,
        beta_start: float = 1e-4,
        beta_end: float = 0.02,
        random_seed: Optional[int] = 42,
    ):
        """Initialize DDPM.

        Args:
            data_dim: Data dimension.
            num_steps: Number of diffusion timesteps.
            hidden_dim: Hidden dimension for denoising model.
            beta_start: Starting beta for schedule.
            beta_end: Ending beta for schedule.
            random_seed: Random seed.
        """
        self.data_dim = data_dim
        self.num_steps = num_steps

        # Beta schedule
        self.betas = linear_beta_schedule(num_steps, beta_start, beta_end)
        self.alphas, self.alpha_bars, self.sqrt_alpha_bars, self.sqrt_one_minus_alpha_bars = \
            compute_alphas(self.betas)
        self.sqrt_recip_alphas = np.sqrt(1.0 / self.alphas)
        self.posterior_variance = self.betas * (1.0 - self.alpha_bars) / (1.0 - self.alpha_bars + 1e-10)

        # Denoising model
        self.model = SimpleUNet(data_dim, hidden_dim, num_steps, random_seed=random_seed)

    def train_step(self, x_0: np.ndarray, lr: float = 0.001) -> float:
        """One training step: sample t, add noise, predict noise, compute MSE.

        Args:
            x_0: Clean data batch of shape (batch_size, data_dim).
            lr: Learning rate.

        Returns:
            MSE loss.
        """
        batch_size = x_0.shape[0]
        t = np.random.randint(0, self.num_steps, batch_size)
        x_t, noise = forward_diffusion(x_0, t, self.sqrt_alpha_bars,
                                        self.sqrt_one_minus_alpha_bars)
        noise_pred = self.model.forward(x_t, t)

        # MSE loss
        diff = noise_pred - noise
        loss = float(np.mean(diff ** 2))
        dout = 2.0 * diff / batch_size

        grads = self.model.backward(dout)

        # Update parameters
        self.model.W1 -= lr * grads["dW1"]
        self.model.b1 -= lr * grads["db1"]
        self.model.W2 -= lr * grads["dW2"]
        self.model.b2 -= lr * grads["db2"]
        self.model.W3 -= lr * grads["dW3"]
        self.model.b3 -= lr * grads["db3"]
        self.model.time_embed -= lr * grads["d_time_embed"]

        return loss

    def _p_sample(self, x_t: np.ndarray, t: int) -> np.ndarray:
        """One reverse diffusion step: predict x_{t-1} from x_t.

        Args:
            x_t: Noisy sample at step t, shape (batch, data_dim).
            t: Current timestep.

        Returns:
            x_{t-1}: slightly denoised sample.
        """
        t_arr = np.full(x_t.shape[0], t)
        noise_pred = self.model.forward(x_t, t_arr)

        alpha_t = self.alphas[t]
        alpha_bar_t = self.alpha_bars[t]
        beta_t = self.betas[t]

        # Predicted x_0
        x_0_pred = (x_t - np.sqrt(1 - alpha_bar_t) * noise_pred) / np.sqrt(alpha_bar_t + 1e-10)

        # Clamp to prevent extreme values
        x_0_pred = np.clip(x_0_pred, -10, 10)

        # Compute mean for posterior
        coef1 = beta_t * np.sqrt(self.alpha_bars[t - 1] + 1e-10) / (1 - alpha_bar_t + 1e-10) if t > 0 else 0
        coef2 = (1 - self.alpha_bars[t - 1]) * np.sqrt(alpha_t) / (1 - alpha_bar_t + 1e-10) if t > 0 else 0
        mean = coef1 * x_0_pred + coef2 * x_t

        if t > 0:
            noise = np.random.randn(*x_t.shape)
            var = np.sqrt(self.posterior_variance[t])
            return mean + var * noise
        else:
            return mean

    def sample(self, n_samples: int) -> np.ndarray:
        """Generate samples by iterative denoising from pure noise.

        Args:
            n_samples: Number of samples to generate.

        Returns:
            Generated data of shape (n_samples, data_dim).
        """
        x = np.random.randn(n_samples, self.data_dim)
        for t in reversed(range(self.num_steps)):
            x = self._p_sample(x, t)
        return x


def generate_swiss_roll(n_samples: int = 500, noise: float = 0.1,
                        random_seed: int = 42) -> np.ndarray:
    """Generate 2D swiss roll data.

    Args:
        n_samples: Number of samples.
        noise: Amount of noise.
        random_seed: Random seed.

    Returns:
        Data of shape (n_samples, 2).
    """
    rng = np.random.RandomState(random_seed)
    t = 1.5 * np.pi * (1 + 2 * rng.rand(n_samples))
    x = t * np.cos(t)
    y = t * np.sin(t)
    data = np.column_stack([x, y])
    data += rng.randn(n_samples, 2) * noise
    # Normalize
    data = (data - data.mean(axis=0)) / data.std(axis=0)
    return data


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing DDPM...")

    np.random.seed(42)

    # Generate toy data
    data = generate_swiss_roll(n_samples=300, noise=0.05, random_seed=42)
    print(f"  Data shape: {data.shape}, range: [{data.min():.2f}, {data.max():.2f}]")

    # Test 1: Beta schedule
    betas = linear_beta_schedule(200)
    assert betas.shape == (200,), f"Wrong betas shape: {betas.shape}"
    assert betas[0] < betas[-1], "Betas should increase"
    print(f"  PASS: Beta schedule: β_0={betas[0]:.6f}, β_T={betas[-1]:.4f}")

    # Test 2: Alpha bars decrease
    alphas, alpha_bars, sqrt_ab, sqrt_1m_ab = compute_alphas(betas)
    assert alpha_bars[0] > alpha_bars[-1], "Alpha bars should decrease"
    assert 0 < alpha_bars[-1] < 1, f"Alpha_bar_T should be close to 0: {alpha_bars[-1]:.6f}"
    print(f"  PASS: Alpha bars: ᾱ₀={alpha_bars[0]:.6f}, ᾱ_T={alpha_bars[-1]:.6f}")

    # Test 3: Forward diffusion
    x_0 = data[:8]
    t = np.array([0, 50, 100, 150, 199, 199, 100, 50])
    x_t, noise = forward_diffusion(x_0, t, sqrt_ab, sqrt_1m_ab)
    assert x_t.shape == (8, 2), f"Wrong x_t shape: {x_t.shape}"
    assert noise.shape == (8, 2)
    # At t=0, x_t should be close to x_0
    assert np.allclose(x_t[0], x_0[0], atol=1e-2), "t=0 should be clean"
    # At t=199, x_t should be mostly noise
    assert not np.allclose(x_t[4], x_0[4], atol=0.1), "t=199 should be noisy"
    print("  PASS: Forward diffusion: t=0 clean, t=199 noisy")

    # Test 4: SimpleUNet forward
    model = SimpleUNet(data_dim=2, hidden_dim=32, num_steps=200, random_seed=42)
    noise_pred = model.forward(x_t, t)
    assert noise_pred.shape == (8, 2), f"Wrong noise_pred shape: {noise_pred.shape}"
    print(f"  PASS: SimpleUNet output shape: {noise_pred.shape}")

    # Test 5: DDPM training step
    ddpm = DDPM(data_dim=2, num_steps=100, hidden_dim=32,
                beta_start=1e-4, beta_end=0.02, random_seed=42)
    loss = ddpm.train_step(data[:32], lr=0.01)
    assert np.isfinite(loss), f"Non-finite loss: {loss}"
    print(f"  PASS: Training step loss: {loss:.4f}")

    # Test 6: DDPM sampling (from untrained model - any variance is fine)
    samples = ddpm.sample(50)
    assert samples.shape == (50, 2), f"Wrong sample shape: {samples.shape}"
    print(f"  PASS: DDPM sampling shape: {samples.shape}")

    # Test 7: Training improves (loss decreases)
    ddpm2 = DDPM(data_dim=2, num_steps=100, hidden_dim=32, random_seed=123)
    initial_loss = ddpm2.train_step(data[:32], lr=0.01)
    losses = []
    for _ in range(100):
        idx = np.random.choice(len(data), 32)
        loss = ddpm2.train_step(data[idx], lr=0.01)
        losses.append(loss)
    assert losses[-1] < initial_loss, f"Loss did not decrease: {initial_loss:.4f} → {losses[-1]:.4f}"
    print(f"  PASS: Training reduced loss: {initial_loss:.4f} → {losses[-1]:.4f}")

    # Test 8: Forward diffusion variance
    x_ones = np.ones((100, 2))
    t_mid = np.full(100, 100)
    x_mid, _ = forward_diffusion(x_ones, t_mid, sqrt_ab, sqrt_1m_ab)
    x_var = np.var(x_mid)
    assert x_var > 0.1, f"Diffused data should have variance, got {x_var:.4f}"
    print(f"  PASS: Forward diffusion variance at t=100: {x_var:.4f}")

    print("\nAll DDPM tests passed!")
