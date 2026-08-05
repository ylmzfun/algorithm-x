"""Simplified Proximal Policy Optimization (PPO) from scratch using NumPy.

Implements:
- Actor-Critic architecture (shared backbone)
- Generalized Advantage Estimation (GAE) simplified
- PPO clipped objective
- Multiple epochs per batch of data

Reference: Schulman et al., "Proximal Policy Optimization Algorithms" (2017).

Note: This is a simplified educational implementation using finite-difference
gradients for parameter updates.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Actor-Critic Network
# ---------------------------------------------------------------------------

class ActorCritic:
    """Actor-Critic neural network with shared backbone.

    Architecture:
        Input → Hidden (ReLU) → Actor head (softmax) + Critic head (linear).

    Attributes:
        state_dim: State dimension.
        action_dim: Number of actions.
        W1, b1: Shared backbone.
        W_actor, b_actor: Actor head.
        W_critic, b_critic: Critic head.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dim: int = 64,
        continuous: bool = False,
        seed: int = 42,
    ) -> None:
        """Initialize the actor-critic network.

        Args:
            state_dim: State dimension.
            action_dim: Action dimension.
            hidden_dim: Hidden layer size.
            continuous: Whether actions are continuous (output mean+std).
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.continuous = continuous

        scale = np.sqrt(2.0 / state_dim)
        self.W1: np.ndarray = rng.normal(0, scale, (state_dim, hidden_dim))
        self.b1: np.ndarray = np.zeros(hidden_dim)

        # Actor head
        if continuous:
            # Output: mean (action_dim) + log_std (action_dim)
            self.W_actor: np.ndarray = rng.normal(0, 0.01,
                                                   (hidden_dim, action_dim))
            self.b_actor: np.ndarray = np.zeros(action_dim)
            self.log_std: np.ndarray = np.zeros(action_dim)
        else:
            scale_a = np.sqrt(2.0 / hidden_dim)
            self.W_actor = rng.normal(0, scale_a, (hidden_dim, action_dim))
            self.b_actor = np.zeros(action_dim)

        # Critic head
        scale_c = np.sqrt(2.0 / hidden_dim)
        self.W_critic: np.ndarray = rng.normal(0, scale_c, (hidden_dim, 1))
        self.b_critic: np.ndarray = np.zeros(1)

    def forward(self, state: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Forward pass.

        Args:
            state: State vector [state_dim] or [B, state_dim].

        Returns:
            Tuple of (action_probs [action_dim], state_value scalar).
        """
        h = np.maximum(0, state @ self.W1 + self.b1)  # ReLU

        if self.continuous:
            mean = h @ self.W_actor + self.b_actor
        else:
            logits = h @ self.W_actor + self.b_actor
            probs = _softmax(logits)

        value = float((h @ self.W_critic + self.b_critic).squeeze())

        if self.continuous:
            return mean, value
        return probs, value

    def sample_action(self, state: np.ndarray) -> tuple[int, np.ndarray, float]:
        """Sample an action and return action, probs, log_prob.

        Args:
            state: State vector.

        Returns:
            Tuple of (action, probs, log_prob).

        Raises:
            RuntimeError: If the network is configured for continuous actions.
        """
        if self.continuous:
            raise RuntimeError("sample_action not supported for continuous")
        probs, _ = self.forward(state)
        action = int(np.random.choice(self.action_dim, p=probs))
        log_prob = float(np.log(probs[action] + 1e-12))
        return action, probs, log_prob

    def get_params(self) -> np.ndarray:
        """Get all parameters as a flat array."""
        parts = [
            self.W1.ravel(), self.b1.ravel(),
            self.W_actor.ravel(), self.b_actor.ravel(),
            self.W_critic.ravel(), self.b_critic.ravel(),
        ]
        if self.continuous:
            parts.append(self.log_std.ravel())
        return np.concatenate(parts)

    def set_params(self, flat: np.ndarray) -> None:
        """Set all parameters from a flat array."""
        sizes = [
            self.W1.size, self.b1.size,
            self.W_actor.size, self.b_actor.size,
            self.W_critic.size, self.b_critic.size,
        ]
        if self.continuous:
            sizes.append(self.log_std.size)
        offsets = [0] + list(np.cumsum(sizes))
        self.W1.ravel()[:] = flat[offsets[0]:offsets[1]]
        self.b1.ravel()[:] = flat[offsets[1]:offsets[2]]
        self.W_actor.ravel()[:] = flat[offsets[2]:offsets[3]]
        self.b_actor.ravel()[:] = flat[offsets[3]:offsets[4]]
        self.W_critic.ravel()[:] = flat[offsets[4]:offsets[5]]
        self.b_critic.ravel()[:] = flat[offsets[5]:offsets[6]]
        if self.continuous:
            self.log_std.ravel()[:] = flat[offsets[6]:offsets[7]]


def _softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / np.sum(e, axis=-1, keepdims=True)


# ---------------------------------------------------------------------------
# PPO Agent
# ---------------------------------------------------------------------------

class PPOAgent:
    """Simplified PPO agent with clipped objective.

    Attributes:
        ac: Actor-Critic network.
        gamma: Discount factor.
        lam: GAE lambda parameter.
        clip_epsilon: Clipping range for PPO objective.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dim: int = 64,
        gamma: float = 0.99,
        lam: float = 0.95,
        clip_epsilon: float = 0.2,
        continuous: bool = False,
        seed: int = 42,
    ) -> None:
        """Initialize the PPO agent.

        Args:
            state_dim: State dimension.
            action_dim: Action dimension.
            hidden_dim: Hidden layer size.
            gamma: Discount factor.
            lam: GAE lambda.
            clip_epsilon: PPO clipping parameter.
            continuous: Whether actions are continuous.
            seed: Random seed.
        """
        self.ac = ActorCritic(state_dim, action_dim, hidden_dim,
                              continuous=continuous, seed=seed)
        self.gamma = gamma
        self.lam = lam
        self.clip_epsilon = clip_epsilon

    def collect_trajectory(
        self, env, max_steps: int = 200
    ) -> tuple[list[np.ndarray], list[int], list[float],
               list[float], list[float], float]:
        """Collect one episode trajectory with value estimates.

        Args:
            env: Environment.
            max_steps: Maximum steps per episode.

        Returns:
            Tuple of (states, actions, rewards, values, log_probs, total_reward).
        """
        states: list[np.ndarray] = []
        actions: list[int] = []
        rewards: list[float] = []
        values: list[float] = []
        log_probs: list[float] = []

        state = env.reset()
        total_reward = 0.0

        for _ in range(max_steps):
            _, value = self.ac.forward(state)
            action, probs, log_prob = self.ac.sample_action(state)

            states.append(state.copy())
            actions.append(action)
            values.append(value)
            log_probs.append(log_prob)

            state, reward, done = env.step(action)
            rewards.append(reward)
            total_reward += reward

            if done:
                break

        return states, actions, rewards, values, log_probs, total_reward

    def compute_advantages(
        self, rewards: list[float], values: list[float]
    ) -> tuple[np.ndarray, np.ndarray]:
        """Compute GAE advantages and returns.

        Args:
            rewards: Episode rewards.
            values: Value estimates.

        Returns:
            Tuple of (advantages [T], returns [T]).
        """
        T = len(rewards)
        advantages = np.zeros(T)
        returns = np.zeros(T)

        gae = 0.0
        for t in range(T - 1, -1, -1):
            next_value = values[t + 1] if t + 1 < T else 0.0
            delta = rewards[t] + self.gamma * next_value - values[t]
            gae = delta + self.gamma * self.lam * gae
            advantages[t] = gae
            returns[t] = advantages[t] + values[t]

        # Normalize advantages
        advantages = (advantages - np.mean(advantages)) / (np.std(advantages) + 1e-8)
        return advantages, returns

    def update(
        self,
        states: list[np.ndarray],
        actions: list[int],
        advantages: np.ndarray,
        returns: np.ndarray,
        old_log_probs: list[float],
        lr: float = 0.01,
        epochs_per_batch: int = 4,
    ) -> float:
        """PPO update with clipped objective over multiple epochs.

        Args:
            states: Trajectory states.
            actions: Actions taken.
            advantages: Computed advantages.
            returns: Computed returns.
            old_log_probs: Log probabilities from behavior policy.
            lr: Learning rate.
            epochs_per_batch: Number of update epochs per batch.

        Returns:
            Total loss.
        """
        total_loss = 0.0
        old_params = self.ac.get_params()

        for _ in range(epochs_per_batch):
            loss = self._compute_ppo_loss(
                states, actions, advantages, returns, old_log_probs
            )
            total_loss += loss

            # SGD step via finite differences
            eps_fd = 1e-4
            params = self.ac.get_params()
            grad = np.zeros_like(params)
            subset = np.random.choice(len(params), min(20, len(params)),
                                      replace=False)

            for idx in subset:
                orig = params[idx]
                params[idx] = orig + eps_fd
                self.ac.set_params(params)
                l_plus = self._compute_ppo_loss(
                    states, actions, advantages, returns, old_log_probs)

                params[idx] = orig - eps_fd
                self.ac.set_params(params)
                l_minus = self._compute_ppo_loss(
                    states, actions, advantages, returns, old_log_probs)

                params[idx] = orig
                grad[idx] = (l_plus - l_minus) / (2 * eps_fd)

            params = params - lr * grad
            self.ac.set_params(params)

        return total_loss

    def _compute_ppo_loss(
        self,
        states: list[np.ndarray],
        actions: list[int],
        advantages: np.ndarray,
        returns: np.ndarray,
        old_log_probs: list[float],
    ) -> float:
        """Compute the PPO clipped objective + value loss.

        L = L^CLIP - c1 * L^VF

        Args:
            states, actions, advantages, returns, old_log_probs: Trajectory data.

        Returns:
            Combined loss.
        """
        T = len(states)
        clip_loss = 0.0
        value_loss = 0.0

        for t in range(T):
            probs, value = self.ac.forward(states[t])
            new_log_prob = float(np.log(probs[actions[t]] + 1e-12))
            ratio = np.exp(new_log_prob - old_log_probs[t])

            # PPO clipped objective
            surr1 = ratio * advantages[t]
            surr2 = np.clip(ratio, 1 - self.clip_epsilon,
                            1 + self.clip_epsilon) * advantages[t]
            clip_loss += -min(surr1, surr2)  # Negative because we minimize

            # Value loss (MSE)
            value_loss += (returns[t] - value) ** 2

        return float((clip_loss + 0.5 * value_loss) / T)


# ---------------------------------------------------------------------------
# Continuous Environment
# ---------------------------------------------------------------------------

class ContinuousEnv:
    """Simple 1D continuous control environment: move a point to a target.

    State: [position, velocity].
    Action: continuous force in [-1, 1].
    Reward: negative distance to target (max 0 at target).
    """

    def __init__(self, target: float = 1.0, seed: int = 42) -> None:
        """Initialize the environment.

        Args:
            target: Target position.
            seed: Random seed.
        """
        self.target = target
        self.rng = np.random.default_rng(seed)
        self.max_steps = 100
        self.observation_space_shape = (2,)
        self.action_space_n = 1  # continuous, but this is just a marker

    def reset(self) -> np.ndarray:
        """Reset to random initial state."""
        self.steps = 0
        return self.rng.uniform(-0.5, 0.5, size=2)

    def step(self, action: float) -> tuple[np.ndarray, float, bool]:
        """Take a step.

        Args:
            action: Scalar force in [-1, 1].

        Returns:
            Tuple of (state, reward, done).
        """
        pos, vel = self._state
        force = np.clip(action, -1.0, 1.0)
        # Simple physics: pos += vel * dt, vel += force * dt
        vel = vel + force * 0.1 - 0.05 * vel  # damped
        pos = pos + vel * 0.1
        self._state = np.array([pos, vel])
        self.steps += 1

        reward = -abs(pos - self.target)
        done = self.steps >= self.max_steps
        return self._state.copy(), float(reward), done

    @property
    def _state(self) -> np.ndarray:
        if not hasattr(self, "_s"):
            self._s = np.zeros(2)
        return self._s

    @_state.setter
    def _state(self, val: np.ndarray) -> None:
        self._s = val


# ---------------------------------------------------------------------------
# Training (discrete version used for testing)
# ---------------------------------------------------------------------------

class DiscreteWrapper:
    """Wrap a continuous env into a discrete action space for testing."""

    def __init__(self, env: ContinuousEnv) -> None:
        self.env = env
        self.observation_space_shape = env.observation_space_shape
        self.action_space_n = 3  # left, stay, right

    def reset(self) -> np.ndarray:
        return self.env.reset()

    def step(self, action: int) -> tuple[np.ndarray, float, bool]:
        force = (action - 1) * 0.5  # 0→-0.5, 1→0, 2→0.5
        return self.env.step(force)


def train_ppo(
    agent: PPOAgent,
    env,
    episodes: int = 200,
    gamma: float = 0.99,
    lam: float = 0.95,
    clip_epsilon: float = 0.2,
    lr: float = 0.01,
    epochs_per_batch: int = 4,
) -> list[float]:
    """Train a PPO agent.

    Args:
        agent: PPOAgent.
        env: Environment.
        episodes: Number of episodes.
        gamma: Discount factor.
        lam: GAE lambda.
        clip_epsilon: PPO clipping.
        lr: Learning rate.
        epochs_per_batch: Update epochs per trajectory.

    Returns:
        List of episode rewards.
    """
    agent.gamma = gamma
    agent.lam = lam
    agent.clip_epsilon = clip_epsilon
    episode_rewards: list[float] = []

    for _ in range(episodes):
        (states, actions, rewards, values,
         log_probs, total) = agent.collect_trajectory(env)

        if len(states) > 1:
            advantages, returns = agent.compute_advantages(rewards, values)
            agent.update(states, actions, advantages, returns, log_probs,
                         lr=lr, epochs_per_batch=epochs_per_batch)

        episode_rewards.append(total)

    return episode_rewards


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing ppo_simple.py — Simplified PPO")
    print("=" * 60)

    # Use a discrete-wrapped continuous env for simplicity
    raw_env = ContinuousEnv(target=1.0, seed=42)
    env = DiscreteWrapper(raw_env)
    print(f"\nContinuousEnv (discrete-wrapped): target=1.0")
    print(f"  State: [position, velocity], Actions: 3 (left, stay, right)")

    # Create agent
    agent = PPOAgent(
        state_dim=2,
        action_dim=3,
        hidden_dim=32,
        gamma=0.99,
        lam=0.95,
        clip_epsilon=0.2,
        seed=42,
    )

    # Train
    rewards = train_ppo(agent, env, episodes=200, lr=0.03,
                        epochs_per_batch=4)

    early_avg = np.mean(rewards[:30])
    late_avg = np.mean(rewards[-30:])
    print(f"\n  Early episodes avg reward: {early_avg:.3f}")
    print(f"  Late episodes avg reward:  {late_avg:.3f}")

    all_pass = True

    # Agent should improve (rewards should increase, i.e., get less negative)
    improved = late_avg > early_avg
    print(f"  Reward improved: {improved}")
    all_pass = all_pass and improved

    # Test actor-critic forward
    state = env.reset()
    probs, value = agent.ac.forward(state)
    print(f"  State: {state}, Value: {value:.3f}, Probs: {probs}")
    probs_sum = abs(np.sum(probs) - 1.0) < 0.01
    print(f"  Probabilities sum to 1: {probs_sum}")
    all_pass = all_pass and probs_sum

    # Test advantage computation
    dummy_rewards = [1.0, 0.0, -1.0]
    dummy_values = [0.5, 0.3, 0.1]
    adv, ret = agent.compute_advantages(dummy_rewards, dummy_values)
    print(f"  Advantages shape: {adv.shape} (expected (3,))")
    all_pass = all_pass and adv.shape == (3,)

    print(f"\n{'PASS' if all_pass else 'FAIL'}: ppo_simple.py")
