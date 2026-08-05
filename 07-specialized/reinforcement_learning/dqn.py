"""Deep Q-Network (DQN) from scratch using NumPy.

Implements:
- Experience replay buffer
- Neural network Q-function approximator
- Target network with periodic weight updates
- Epsilon-greedy exploration
- Simplified CartPole simulation

Reference: Mnih et al., "Playing Atari with Deep Reinforcement Learning" (2013);
Mnih et al., "Human-level control through deep reinforcement learning" (2015).
"""

from __future__ import annotations

import numpy as np
from typing import Optional
from collections import deque


# ---------------------------------------------------------------------------
# Replay Buffer
# ---------------------------------------------------------------------------

class ReplayBuffer:
    """Fixed-size circular replay buffer for experience replay.

    Stores (state, action, reward, next_state, done) transitions and
    samples random mini-batches to break temporal correlations.

    Attributes:
        capacity: Maximum number of transitions stored.
        buffer: Deque of transitions.
    """

    def __init__(self, capacity: int = 10000) -> None:
        """Initialize the replay buffer.

        Args:
            capacity: Maximum number of transitions to store.
        """
        self.capacity = capacity
        self.buffer: deque = deque(maxlen=capacity)

    def push(
        self,
        state: np.ndarray,
        action: int,
        reward: float,
        next_state: np.ndarray,
        done: bool,
    ) -> None:
        """Store a transition.

        Args:
            state: Current state vector.
            action: Action taken.
            reward: Reward received.
            next_state: Next state vector.
            done: Whether episode terminated.
        """
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size: int) -> tuple[np.ndarray, ...]:
        """Sample a random mini-batch.

        Args:
            batch_size: Number of transitions to sample.

        Returns:
            Tuple of (states, actions, rewards, next_states, dones).
        """
        indices = np.random.choice(len(self.buffer), batch_size, replace=False)
        states, actions, rewards, next_states, dones = [], [], [], [], []
        for i in indices:
            s, a, r, ns, d = self.buffer[i]
            states.append(s)
            actions.append(a)
            rewards.append(r)
            next_states.append(ns)
            dones.append(d)
        return (
            np.array(states),
            np.array(actions, dtype=np.int64),
            np.array(rewards, dtype=np.float64),
            np.array(next_states),
            np.array(dones, dtype=bool),
        )

    def __len__(self) -> int:
        return len(self.buffer)


# ---------------------------------------------------------------------------
# Simple DQN Network
# ---------------------------------------------------------------------------

class SimpleDQN:
    """Small feed-forward neural network for DQN.

    Architecture: input → hidden → hidden → Q-values (one per action).

    Attributes:
        layers: List of (W, b) tuples.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dims: tuple[int, ...] = (64, 64),
        seed: int = 42,
    ) -> None:
        """Initialize the Q-network.

        Args:
            state_dim: Dimension of state space.
            action_dim: Number of actions.
            hidden_dims: Hidden layer sizes.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.layers: list[tuple[np.ndarray, np.ndarray]] = []

        dims = [state_dim] + list(hidden_dims) + [action_dim]
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
            x: State vector [state_dim] or batch [B, state_dim].

        Returns:
            Q-values [action_dim] or [B, action_dim].
        """
        out = x
        for i, (W, b) in enumerate(self.layers):
            out = out @ W + b
            if i < len(self.layers) - 1:  # ReLU for hidden layers
                out = np.maximum(0, out)
        return out

    def copy_weights_from(self, other: "SimpleDQN") -> None:
        """Copy weights from another network (for target network updates).

        Args:
            other: Source network to copy from.
        """
        for (W_self, b_self), (W_other, b_other) in zip(self.layers, other.layers):
            W_self[:] = W_other
            b_self[:] = b_other

    def get_flat_params(self) -> np.ndarray:
        """Get all parameters as a single flat array."""
        parts = [W.ravel() for W, b in self.layers] + [b.ravel() for W, b in self.layers]
        return np.concatenate(parts)

    def set_flat_params(self, flat: np.ndarray) -> None:
        """Set all parameters from a flat array."""
        offset = 0
        for W, b in self.layers:
            size = W.size
            W.ravel()[:] = flat[offset:offset + size]
            offset += size
        for W, b in self.layers:
            size = b.size
            b.ravel()[:] = flat[offset:offset + size]
            offset += size


# ---------------------------------------------------------------------------
# DQN Agent
# ---------------------------------------------------------------------------

class DQNAgent:
    """DQN agent with replay buffer and target network.

    Attributes:
        q_net: Online Q-network.
        target_net: Target Q-network (updated periodically).
        replay_buffer: Experience replay buffer.
        action_dim: Number of actions.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dims: tuple[int, ...] = (64, 64),
        buffer_capacity: int = 10000,
        seed: int = 42,
    ) -> None:
        """Initialize the DQN agent.

        Args:
            state_dim: State dimension.
            action_dim: Number of actions.
            hidden_dims: Hidden layer sizes.
            buffer_capacity: Replay buffer capacity.
            seed: Random seed.
        """
        self.action_dim = action_dim
        self.q_net = SimpleDQN(state_dim, action_dim, hidden_dims, seed=seed)
        self.target_net = SimpleDQN(state_dim, action_dim, hidden_dims, seed=seed + 1)
        self.target_net.copy_weights_from(self.q_net)
        self.replay_buffer = ReplayBuffer(buffer_capacity)

    def select_action(self, state: np.ndarray, epsilon: float = 0.1) -> int:
        """Epsilon-greedy action selection.

        Args:
            state: Current state vector [state_dim].
            epsilon: Exploration probability.

        Returns:
            Selected action index.
        """
        if np.random.random() < epsilon:
            return np.random.randint(self.action_dim)
        q_values = self.q_net.forward(state)
        return int(np.argmax(q_values))

    def update_target(self) -> None:
        """Copy online network weights to target network."""
        self.target_net.copy_weights_from(self.q_net)

    def train_step(
        self, batch_size: int, gamma: float, lr: float
    ) -> float:
        """One training step with a sampled mini-batch.

        Args:
            batch_size: Mini-batch size.
            gamma: Discount factor.
            lr: Learning rate.

        Returns:
            Average TD loss.
        """
        if len(self.replay_buffer) < batch_size:
            return 0.0

        states, actions, rewards, next_states, dones = \
            self.replay_buffer.sample(batch_size)

        # Current Q-values
        q_values = self.q_net.forward(states)  # [B, A]
        q_current = q_values[np.arange(batch_size), actions]  # [B]

        # Target Q-values
        q_next = self.target_net.forward(next_states)  # [B, A]
        q_next_max = np.max(q_next, axis=1)  # [B]
        q_target = rewards + gamma * q_next_max * (~dones)

        # Loss and gradient (simple weight perturbation SGD)
        loss = np.mean((q_current - q_target) ** 2)

        # SGD via finite differences on a subset of parameters
        eps_fd = 1e-4
        param_parts = []
        for W, b in self.q_net.layers:
            param_parts.append(W.ravel())
            param_parts.append(b.ravel())
        flat_params = np.concatenate(param_parts)
        total_size = len(flat_params)

        grad = np.zeros(total_size)
        subset_size = min(50, total_size)
        for idx in np.random.choice(total_size, subset_size, replace=False):
            orig = flat_params[idx]
            flat_params[idx] = orig + eps_fd
            self.q_net.set_flat_params(flat_params)
            q_plus = self.q_net.forward(states)[np.arange(batch_size), actions]
            loss_plus = np.mean((q_plus - q_target) ** 2)

            flat_params[idx] = orig - eps_fd
            self.q_net.set_flat_params(flat_params)
            q_minus = self.q_net.forward(states)[np.arange(batch_size), actions]
            loss_minus = np.mean((q_minus - q_target) ** 2)

            flat_params[idx] = orig
            grad[idx] = (loss_plus - loss_minus) / (2 * eps_fd)

        flat_params -= lr * grad
        self.q_net.set_flat_params(flat_params)

        return float(loss)


# ---------------------------------------------------------------------------
# CartPole Simulation
# ---------------------------------------------------------------------------

class CartPoleSim:
    """Simplified CartPole-like simulation using NumPy physics.

    State: [cart_position, cart_velocity, pole_angle, pole_angular_velocity].
    Action: 0 = push left, 1 = push right.

    Uses simple Euler integration with configurable physics parameters.
    """

    def __init__(
        self,
        gravity: float = 9.8,
        cart_mass: float = 1.0,
        pole_mass: float = 0.1,
        pole_length: float = 0.5,
        force_mag: float = 10.0,
        dt: float = 0.02,
        seed: int = 42,
    ) -> None:
        """Initialize the CartPole simulation.

        Args:
            gravity: Gravitational acceleration.
            cart_mass: Mass of the cart.
            pole_mass: Mass of the pole.
            pole_length: Half-length of the pole.
            force_mag: Magnitude of applied force.
            dt: Time step for Euler integration.
            seed: Random seed.
        """
        self.gravity = gravity
        self.cart_mass = cart_mass
        self.pole_mass = pole_mass
        self.total_mass = cart_mass + pole_mass
        self.pole_length = pole_length
        self.force_mag = force_mag
        self.dt = dt
        self.rng = np.random.default_rng(seed)

        # State bounds for termination
        self.x_threshold = 2.4
        self.theta_threshold = np.radians(18)  # ~18 degrees
        self.max_steps = 200

        # Gym compatibility
        self.observation_space_shape = (4,)
        self.action_space_n = 2

    def reset(self) -> np.ndarray:
        """Reset the environment to a random initial state.

        Returns:
            Initial state vector [4].
        """
        self.steps = 0
        return self.rng.uniform(-0.05, 0.05, size=4)

    def step(self, action: int) -> tuple[np.ndarray, float, bool]:
        """Take a step in the simulation.

        Args:
            action: 0 = push left, 1 = push right.

        Returns:
            Tuple of (state, reward, done).
        """
        x, x_dot, theta, theta_dot = self._state
        force = self.force_mag if action == 1 else -self.force_mag

        cos_theta = np.cos(theta)
        sin_theta = np.sin(theta)

        # Pole angular acceleration
        temp = (
            force + self.pole_mass * self.pole_length * theta_dot**2 * sin_theta
        ) / self.total_mass
        theta_acc = (self.gravity * sin_theta - cos_theta * temp) / (
            self.pole_length
            * (4.0 / 3.0 - self.pole_mass * cos_theta**2 / self.total_mass)
        )

        # Cart acceleration
        x_acc = temp - self.pole_mass * self.pole_length * theta_acc * cos_theta / self.total_mass

        # Euler integration
        x = x + self.dt * x_dot
        x_dot = x_dot + self.dt * x_acc
        theta = theta + self.dt * theta_dot
        theta_dot = theta_dot + self.dt * theta_acc

        self._state = np.array([x, x_dot, theta, theta_dot])
        self.steps += 1

        # Check termination
        done = bool(
            abs(x) > self.x_threshold
            or abs(theta) > self.theta_threshold
            or self.steps >= self.max_steps
        )

        reward = 1.0 if not done else 0.0

        return self._state.copy(), reward, done

    @property
    def _state(self) -> np.ndarray:
        if not hasattr(self, "_state_val"):
            self._state_val = np.zeros(4)
        return self._state_val

    @_state.setter
    def _state(self, val: np.ndarray) -> None:
        self._state_val = val


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_dqn(
    env: CartPoleSim,
    agent: DQNAgent,
    episodes: int = 200,
    batch_size: int = 32,
    gamma: float = 0.99,
    lr: float = 0.01,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.05,
    epsilon_decay: float = 0.98,
    target_update_freq: int = 10,
) -> list[float]:
    """Train a DQN agent on CartPole.

    Args:
        env: CartPole simulation.
        agent: DQNAgent.
        episodes: Number of training episodes.
        batch_size: Mini-batch size.
        gamma: Discount factor.
        lr: Learning rate.
        epsilon_start: Initial epsilon.
        epsilon_end: Minimum epsilon.
        epsilon_decay: Per-episode epsilon decay.
        target_update_freq: Episodes between target network updates.

    Returns:
        List of episode total rewards.
    """
    epsilon = epsilon_start
    episode_rewards: list[float] = []

    for ep in range(episodes):
        state = env.reset()
        total_reward = 0.0

        while True:
            action = agent.select_action(state, epsilon)
            next_state, reward, done = env.step(action)
            agent.replay_buffer.push(state, action, reward, next_state, done)
            agent.train_step(batch_size, gamma, lr)
            total_reward += reward
            state = next_state
            if done:
                break

        episode_rewards.append(total_reward)
        epsilon = max(epsilon_end, epsilon * epsilon_decay)

        if (ep + 1) % target_update_freq == 0:
            agent.update_target()

    return episode_rewards


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing dqn.py — Deep Q-Network")
    print("=" * 60)

    # Create environment
    env = CartPoleSim(seed=42)
    print(f"\nCartPoleSim: state_dim=4, actions=2")

    # Create agent
    agent = DQNAgent(
        state_dim=4,
        action_dim=2,
        hidden_dims=(32, 32),
        buffer_capacity=5000,
        seed=42,
    )

    # Train
    print("\nTraining DQN...")
    rewards = train_dqn(
        env, agent,
        episodes=150, batch_size=16,
        gamma=0.99, lr=0.01,
        target_update_freq=10,
    )

    early_avg = np.mean(rewards[:30])
    late_avg = np.mean(rewards[-30:])
    print(f"  Early episodes avg reward: {early_avg:.1f}")
    print(f"  Late episodes avg reward:  {late_avg:.1f}")
    print(f"  Best episode reward: {max(rewards):.0f}")

    # Test: run a few episodes greedy
    test_rewards: list[float] = []
    for _ in range(10):
        state = env.reset()
        total = 0.0
        while True:
            action = agent.select_action(state, epsilon=0.0)
            state, reward, done = env.step(action)
            total += reward
            if done:
                break
        test_rewards.append(total)
    avg_test = np.mean(test_rewards)
    print(f"  Greedy evaluation avg reward: {avg_test:.1f}")

    all_pass = True

    # Agent should improve
    improved = late_avg > early_avg
    print(f"\n  Reward improved: {improved}")
    all_pass = all_pass and improved

    # Replay buffer test
    print(f"  Replay buffer size: {len(agent.replay_buffer)}")
    buf_ok = len(agent.replay_buffer) > 0
    all_pass = all_pass and buf_ok

    # Target network should differ from online initially
    q1 = agent.q_net.forward(np.zeros(4))
    q2 = agent.target_net.forward(np.zeros(4))
    # After training they may differ; update target to make them same
    agent.update_target()
    q3 = agent.target_net.forward(np.zeros(4))
    synced = np.allclose(q1, q3)
    print(f"  Target network sync works: {synced}")
    all_pass = all_pass and synced

    print(f"\n{'PASS' if all_pass else 'FAIL'}: dqn.py")
