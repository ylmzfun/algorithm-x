"""REINFORCE Policy Gradient from scratch using NumPy.

Implements:
- Stochastic policy network (action probabilities via softmax)
- Trajectory collection
- Monte Carlo returns with discounting
- Policy gradient update

Reference: Williams, "Simple Statistical Gradient-Following Algorithms
for Connectionist Reinforcement Learning" (1992);
Sutton & Barto, "Reinforcement Learning: An Introduction" (2018).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Policy Network
# ---------------------------------------------------------------------------

class PolicyNetwork:
    """Simple neural network that outputs action probabilities.

    Architecture: Input → Hidden (ReLU) → Softmax over actions.

    Attributes:
        W1, b1: Input-to-hidden weights and bias.
        W2, b2: Hidden-to-output weights and bias.
        state_dim: Dimension of state vectors.
        action_dim: Number of actions.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dim: int = 32,
        seed: int = 42,
    ) -> None:
        """Initialize the policy network.

        Args:
            state_dim: Input state dimension.
            action_dim: Number of possible actions.
            hidden_dim: Hidden layer size.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        scale1 = np.sqrt(2.0 / state_dim)
        scale2 = np.sqrt(2.0 / hidden_dim)
        self.W1: np.ndarray = rng.normal(0, scale1, (state_dim, hidden_dim))
        self.b1: np.ndarray = np.zeros(hidden_dim)
        self.W2: np.ndarray = rng.normal(0, scale2, (hidden_dim, action_dim))
        self.b2: np.ndarray = np.zeros(action_dim)
        self.state_dim = state_dim
        self.action_dim = action_dim

    def forward(self, state: np.ndarray) -> np.ndarray:
        """Compute action probabilities for a given state.

        Args:
            state: State vector [state_dim] or [B, state_dim].

        Returns:
            Action probabilities [action_dim] or [B, action_dim].
        """
        h = np.maximum(0, state @ self.W1 + self.b1)  # ReLU
        logits = h @ self.W2 + self.b2
        return _softmax(logits)

    def sample_action(self, state: np.ndarray) -> tuple[int, np.ndarray]:
        """Sample an action from the policy distribution.

        Args:
            state: State vector [state_dim].

        Returns:
            Tuple of (action_index, action_probabilities).
        """
        probs = self.forward(state)
        action = int(np.random.choice(self.action_dim, p=probs))
        return action, probs

    def get_params(self) -> np.ndarray:
        """Get all parameters as a flat array."""
        return np.concatenate([
            self.W1.ravel(), self.b1.ravel(),
            self.W2.ravel(), self.b2.ravel(),
        ])

    def set_params(self, flat: np.ndarray) -> None:
        """Set all parameters from a flat array."""
        sizes = [
            self.W1.size, self.b1.size,
            self.W2.size, self.b2.size,
        ]
        offsets = [0] + list(np.cumsum(sizes))
        self.W1.ravel()[:] = flat[offsets[0]:offsets[1]]
        self.b1.ravel()[:] = flat[offsets[1]:offsets[2]]
        self.W2.ravel()[:] = flat[offsets[2]:offsets[3]]
        self.b2.ravel()[:] = flat[offsets[3]:offsets[4]]


def _softmax(x: np.ndarray) -> np.ndarray:
    """Stable softmax along last axis."""
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / np.sum(e, axis=-1, keepdims=True)


# ---------------------------------------------------------------------------
# REINFORCE Agent
# ---------------------------------------------------------------------------

class REINFORCEAgent:
    """REINFORCE agent with Monte Carlo policy gradients.

    Collects full trajectories and updates the policy using:
        ∇J ≈ Σ_t γ^t G_t ∇ log π(a_t|s_t)

    Attributes:
        policy_net: The policy network.
        gamma: Discount factor.
    """

    def __init__(
        self,
        state_dim: int,
        action_dim: int,
        hidden_dim: int = 32,
        gamma: float = 0.99,
        seed: int = 42,
    ) -> None:
        """Initialize the REINFORCE agent.

        Args:
            state_dim: State dimension.
            action_dim: Number of actions.
            hidden_dim: Hidden layer size.
            gamma: Discount factor.
            seed: Random seed.
        """
        self.policy_net = PolicyNetwork(state_dim, action_dim, hidden_dim, seed=seed)
        self.gamma = gamma
        self.action_dim = action_dim

    def collect_trajectory(
        self, env
    ) -> tuple[list[np.ndarray], list[int], list[float], float]:
        """Collect one episode trajectory.

        Args:
            env: Environment with reset() and step().

        Returns:
            Tuple of (states, actions, rewards, total_reward).
        """
        states: list[np.ndarray] = []
        actions: list[int] = []
        rewards: list[float] = []

        state = env.reset()
        done = False
        total_reward = 0.0

        while not done:
            states.append(state.copy())
            action, _ = self.policy_net.sample_action(state)
            actions.append(action)
            state, reward, done = env.step(action)
            rewards.append(reward)
            total_reward += reward

        return states, actions, rewards, total_reward

    def _compute_returns(self, rewards: list[float]) -> np.ndarray:
        """Compute discounted returns G_t = Σ_{k=0} γ^k r_{t+k}.

        Args:
            rewards: List of episode rewards.

        Returns:
            Discounted returns [T].
        """
        T = len(rewards)
        returns = np.zeros(T)
        G = 0.0
        for t in range(T - 1, -1, -1):
            G = rewards[t] + self.gamma * G
            returns[t] = G
        # Normalize returns (baseline subtraction)
        returns = (returns - np.mean(returns)) / (np.std(returns) + 1e-8)
        return returns

    def update(
        self,
        states: list[np.ndarray],
        actions: list[int],
        rewards: list[float],
        lr: float = 0.01,
    ) -> float:
        """One REINFORCE update step.

        Args:
            states: Episode states.
            actions: Actions taken.
            rewards: Rewards received.
            lr: Learning rate.

        Returns:
            Loss value.
        """
        returns = self._compute_returns(rewards)

        # Finite-difference gradient on policy parameters
        old_params = self.policy_net.get_params()
        eps_fd = 1e-4
        grad = np.zeros_like(old_params)
        subset = np.random.choice(len(old_params), min(30, len(old_params)), replace=False)

        for idx in subset:
            orig = old_params[idx]
            old_params[idx] = orig + eps_fd
            self.policy_net.set_params(old_params)
            loss_plus = self._policy_loss(states, actions, returns)

            old_params[idx] = orig - eps_fd
            self.policy_net.set_params(old_params)
            loss_minus = self._policy_loss(states, actions, returns)

            old_params[idx] = orig
            grad[idx] = (loss_plus - loss_minus) / (2 * eps_fd)

        new_params = old_params - lr * grad
        self.policy_net.set_params(new_params)

        return float(self._policy_loss(states, actions, returns))

    def _policy_loss(
        self,
        states: list[np.ndarray],
        actions: list[int],
        returns: np.ndarray,
    ) -> float:
        """Compute the REINFORCE loss (negative log-prob weighted by returns).

        Args:
            states: Episode states.
            actions: Actions taken.
            returns: Discounted and normalized returns.

        Returns:
            Negative of the policy gradient objective.
        """
        loss = 0.0
        for t, state in enumerate(states):
            probs = self.policy_net.forward(state)
            log_prob = np.log(probs[actions[t]] + 1e-12)
            loss -= returns[t] * log_prob  # negative because we minimize
        return float(loss)


# ---------------------------------------------------------------------------
# Simple Bandit Environment
# ---------------------------------------------------------------------------

class SimpleBanditEnv:
    """Simple multi-state bandit-like environment for policy gradient demo.

    There are 4 states (0-3), each with 2 actions (0, 1).
    Action 0 gives reward with p=0.3 in all states.
    Action 1 gives reward with p=0.7 in even states, p=0.2 in odd states.
    The optimal policy: action 1 in states 0,2; action 0 in states 1,3.

    Attributes:
        n_states: Number of states (4).
        n_actions: Number of actions (2).
        optimal_rewards: True reward probabilities [n_states, n_actions].
    """

    def __init__(self, seed: int = 42) -> None:
        """Initialize the bandit environment.

        Args:
            seed: Random seed.
        """
        self.rng = np.random.default_rng(seed)
        self.n_states = 4
        self.n_actions = 2
        # Optimal: action 1 in even states, action 0 in odd states
        self.optimal_rewards = np.array([
            [0.3, 0.7],  # state 0: action 1 is better
            [0.6, 0.2],  # state 1: action 0 is better
            [0.3, 0.7],  # state 2: action 1 is better
            [0.6, 0.2],  # state 3: action 0 is better
        ])
        self.current_state = 0
        self.observation_space_shape = (4,)
        self.action_space_n = 2

    def reset(self) -> np.ndarray:
        """Reset to a random state.

        Returns:
            One-hot state vector [4].
        """
        self.current_state = np.random.randint(self.n_states)
        return self._one_hot(self.current_state)

    def step(self, action: int) -> tuple[np.ndarray, float, bool]:
        """Take an action and receive reward.

        Args:
            action: 0 or 1.

        Returns:
            Tuple of (next_state_one_hot, reward, done).
        """
        prob = self.optimal_rewards[self.current_state, action]
        reward = 1.0 if self.rng.random() < prob else 0.0
        # Move to next state (cyclic for longer trajectories)
        self.current_state = (self.current_state + 1) % self.n_states
        return self._one_hot(self.current_state), reward, False  # never ends

    def _one_hot(self, s: int) -> np.ndarray:
        vec = np.zeros(self.n_states)
        vec[s] = 1.0
        return vec


# ---------------------------------------------------------------------------
# Training
# ---------------------------------------------------------------------------

def train_reinforce(
    agent: REINFORCEAgent,
    env,
    episodes: int = 200,
    gamma: float = 0.99,
    lr: float = 0.01,
) -> list[float]:
    """Train a REINFORCE agent.

    Args:
        agent: REINFORCEAgent.
        env: Environment.
        episodes: Number of episodes.
        gamma: Discount factor (overrides agent's default).
        lr: Learning rate.

    Returns:
        List of episode total rewards.
    """
    agent.gamma = gamma
    episode_rewards: list[float] = []

    for _ in range(episodes):
        states, actions, rewards, total = agent.collect_trajectory(env)
        agent.update(states, actions, rewards, lr=lr)
        episode_rewards.append(total)

    return episode_rewards


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing policy_gradient.py — REINFORCE")
    print("=" * 60)

    # Create environment
    env = SimpleBanditEnv(seed=42)
    print(f"\nSimpleBanditEnv: 4 states, 2 actions")
    print(f"  Optimal: action 1 in states 0,2; action 0 in states 1,3")

    # Create agent
    agent = REINFORCEAgent(
        state_dim=4,
        action_dim=2,
        hidden_dim=16,
        gamma=0.99,
        seed=42,
    )

    # Train
    rewards = train_reinforce(agent, env, episodes=300, gamma=0.99, lr=0.05)

    early_avg = np.mean(rewards[:50])
    late_avg = np.mean(rewards[-50:])
    print(f"\n  Early episodes avg reward: {early_avg:.3f}")
    print(f"  Late episodes avg reward:  {late_avg:.3f}")

    # Evaluate policy
    print("\n  Learned policy:")
    all_pass = True
    optimal_actions = [1, 0, 1, 0]
    for s in range(4):
        one_hot = np.zeros(4)
        one_hot[s] = 1.0
        probs = agent.policy_net.forward(one_hot)
        best_action = int(np.argmax(probs))
        print(f"    State {s}: probs={probs}, "
              f"best_action={best_action} "
              f"(optimal={optimal_actions[s]})")
        if best_action != optimal_actions[s]:
            all_pass = False

    improved = late_avg > early_avg
    print(f"\n  Reward improved: {improved}")
    all_pass = all_pass and improved

    print(f"\n{'PASS' if all_pass else 'FAIL'}: policy_gradient.py")
