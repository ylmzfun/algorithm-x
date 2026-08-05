"""Tabular Q-Learning from scratch using NumPy.

Implements:
- FrozenLake-like stochastic grid environment
- Epsilon-greedy exploration
- Q-table update (temporal difference learning)
- Agent evaluation

Reference: Watkins & Dayan, "Q-Learning" (1992);
Sutton & Barto, "Reinforcement Learning: An Introduction" (2018).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# FrozenLake Environment
# ---------------------------------------------------------------------------

class FrozenLakeEnv:
    """Simplified FrozenLake-like grid environment with stochastic dynamics.

    Grid cells: F=frozen(safe), H=hole(danger), G=goal, S=start.
    Actions: 0=LEFT, 1=DOWN, 2=RIGHT, 3=UP.
    The agent slips with some probability (moves in a random direction).

    Attributes:
        n_rows, n_cols: Grid dimensions.
        n_states: Total states.
        n_actions: 4 actions.
        grid: String grid representation.
        slip_prob: Probability of moving in a random direction.
    """

    ACTION_EFFECTS = [(0, -1), (1, 0), (0, 1), (-1, 0)]  # LEFT, DOWN, RIGHT, UP

    def __init__(
        self, grid: Optional[list[str]] = None, slip_prob: float = 0.1
    ) -> None:
        """Initialize the FrozenLake environment.

        Args:
            grid: List of strings, one per row. Use F/S/G/H characters.
            slip_prob: Probability of slipping to a random action.
        """
        if grid is None:
            grid = [
                "SFFF",
                "FHFH",
                "FFFH",
                "HFFG",
            ]
        self.grid = grid
        self.n_rows = len(grid)
        self.n_cols = len(grid[0])
        self.n_states = self.n_rows * self.n_cols
        self.n_actions = 4
        self.slip_prob = slip_prob

        # Identify special states
        self.holes: set[int] = set()
        self.goal: int = 0
        self.start: int = 0
        for r in range(self.n_rows):
            for c in range(self.n_cols):
                s = self._rc_to_s(r, c)
                ch = grid[r][c]
                if ch == "S":
                    self.start = s
                elif ch == "G":
                    self.goal = s
                elif ch == "H":
                    self.holes.add(s)

        self.terminal_states = {self.goal} | self.holes

    def _rc_to_s(self, r: int, c: int) -> int:
        return r * self.n_cols + c

    def _s_to_rc(self, s: int) -> tuple[int, int]:
        return s // self.n_cols, s % self.n_cols

    def reset(self) -> int:
        """Reset the environment to start state."""
        return self.start

    def step(self, state: int, action: int) -> tuple[int, float, bool]:
        """Take a step in the environment.

        Args:
            state: Current state index.
            action: Action index (0-3).

        Returns:
            Tuple of (next_state, reward, done).
        """
        # With slip_prob, take a random action instead
        if np.random.random() < self.slip_prob:
            action = np.random.randint(self.n_actions)

        r, c = self._s_to_rc(state)
        dr, dc = self.ACTION_EFFECTS[action]
        nr, nc = r + dr, c + dc

        # Stay within bounds
        nr = max(0, min(self.n_rows - 1, nr))
        nc = max(0, min(self.n_cols - 1, nc))
        next_state = self._rc_to_s(nr, nc)

        if next_state == self.goal:
            return next_state, 1.0, True
        elif next_state in self.holes:
            return next_state, -1.0, True
        else:
            return next_state, -0.01, False  # Small negative reward per step


# ---------------------------------------------------------------------------
# Q-Learning Agent
# ---------------------------------------------------------------------------

class QLearningAgent:
    """Tabular Q-Learning agent.

    Maintains a Q-table Q[s, a] and updates it using the TD(0) update:
        Q(s,a) ← Q(s,a) + α [r + γ max_a' Q(s',a') - Q(s,a)]

    Attributes:
        n_states: Number of states.
        n_actions: Number of actions.
        Q: Q-table [n_states, n_actions].
    """

    def __init__(self, n_states: int, n_actions: int, seed: int = 42) -> None:
        """Initialize the Q-Learning agent.

        Args:
            n_states: Number of states.
            n_actions: Number of actions.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.n_states = n_states
        self.n_actions = n_actions
        self.Q: np.ndarray = rng.normal(0, 0.01, (n_states, n_actions))

    def select_action(
        self, state: int, epsilon: float = 0.1
    ) -> int:
        """Epsilon-greedy action selection.

        Args:
            state: Current state.
            epsilon: Exploration probability.

        Returns:
            Selected action index.
        """
        if np.random.random() < epsilon:
            return np.random.randint(self.n_actions)
        return int(np.argmax(self.Q[state]))

    def update(
        self,
        state: int,
        action: int,
        reward: float,
        next_state: int,
        done: bool,
        alpha: float = 0.1,
        gamma: float = 0.99,
    ) -> None:
        """Q-table TD(0) update.

        Args:
            state: Current state.
            action: Action taken.
            reward: Reward received.
            next_state: Resulting state.
            done: Whether the episode terminated.
            alpha: Learning rate.
            gamma: Discount factor.
        """
        target = reward
        if not done:
            target += gamma * np.max(self.Q[next_state])
        td_error = target - self.Q[state, action]
        self.Q[state, action] += alpha * td_error


# ---------------------------------------------------------------------------
# Training and Evaluation
# ---------------------------------------------------------------------------

def train_q_learning(
    env: FrozenLakeEnv,
    agent: QLearningAgent,
    episodes: int = 500,
    max_steps: int = 100,
    alpha: float = 0.1,
    gamma: float = 0.99,
    epsilon_start: float = 1.0,
    epsilon_end: float = 0.01,
    epsilon_decay: float = 0.995,
) -> list[float]:
    """Train a Q-Learning agent.

    Args:
        env: The FrozenLake environment.
        agent: The QLearningAgent.
        episodes: Number of training episodes.
        max_steps: Maximum steps per episode.
        alpha: Learning rate.
        gamma: Discount factor.
        epsilon_start: Initial exploration rate.
        epsilon_end: Minimum exploration rate.
        epsilon_decay: Per-episode epsilon decay factor.

    Returns:
        List of episode rewards.
    """
    epsilon = epsilon_start
    episode_rewards: list[float] = []

    for _ in range(episodes):
        state = env.reset()
        total_reward = 0.0

        for _ in range(max_steps):
            action = agent.select_action(state, epsilon)
            next_state, reward, done = env.step(state, action)
            agent.update(state, action, reward, next_state, done, alpha, gamma)
            total_reward += reward
            state = next_state
            if done:
                break

        episode_rewards.append(total_reward)
        epsilon = max(epsilon_end, epsilon * epsilon_decay)

    return episode_rewards


def evaluate_agent(
    env: FrozenLakeEnv,
    agent: QLearningAgent,
    episodes: int = 100,
    max_steps: int = 100,
) -> float:
    """Evaluate the agent without exploration (greedy).

    Args:
        env: The environment.
        agent: The trained agent.
        episodes: Number of evaluation episodes.
        max_steps: Maximum steps per episode.

    Returns:
        Success rate (fraction of episodes reaching the goal).
    """
    successes = 0
    for _ in range(episodes):
        state = env.reset()
        for _ in range(max_steps):
            action = agent.select_action(state, epsilon=0.0)
            next_state, reward, done = env.step(state, action)
            if done:
                if next_state == env.goal:
                    successes += 1
                break
            state = next_state
    return successes / episodes


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing q_learning.py — Tabular Q-Learning")
    print("=" * 60)

    # Create environment
    env = FrozenLakeEnv(
        grid=["SFF", "FHF", "FFG"],
        slip_prob=0.1,
    )
    print(f"\nEnvironment: {env.n_rows}x{env.n_cols}, "
          f"{len(env.holes)} holes, 1 goal")
    print(f"  Grid:")
    for row in env.grid:
        print(f"    {row}")

    # Create agent and train
    agent = QLearningAgent(env.n_states, env.n_actions, seed=42)
    rewards = train_q_learning(
        env, agent,
        episodes=500, max_steps=100,
        alpha=0.1, gamma=0.99,
    )

    # Check learning progress
    early_reward = np.mean(rewards[:50])
    late_reward = np.mean(rewards[-50:])
    print(f"\n  Early episodes average reward: {early_reward:.3f}")
    print(f"  Late episodes average reward:  {late_reward:.3f}")

    # Evaluate
    success_rate = evaluate_agent(env, agent, episodes=200, max_steps=50)
    print(f"  Success rate: {success_rate:.2%}")

    all_pass = True

    # Q-table should have learned something
    q_max = np.max(agent.Q)
    q_min = np.min(agent.Q)
    print(f"  Q-table range: [{q_min:.3f}, {q_max:.3f}]")
    q_learned = q_max > q_min  # Q-values differ
    all_pass = all_pass and q_learned

    # Success rate should be reasonable
    rate_ok = success_rate > 0.3
    print(f"  Success rate > 30%: {rate_ok}")
    all_pass = all_pass and rate_ok

    # Late rewards should be higher than early
    improved = late_reward > early_reward
    print(f"  Reward improved: {improved}")
    all_pass = all_pass and improved

    # Test with simpler environment (no slip, no holes)
    env_simple = FrozenLakeEnv(
        grid=["SG"],
        slip_prob=0.0,
    )
    agent_simple = QLearningAgent(env_simple.n_states, env_simple.n_actions, seed=42)
    train_q_learning(env_simple, agent_simple, episodes=200, max_steps=10,
                     alpha=0.5, gamma=0.99)
    sr_simple = evaluate_agent(env_simple, agent_simple, episodes=50, max_steps=5)
    print(f"\n  Simple env (1-row) success rate: {sr_simple:.0%}")
    all_pass = all_pass and sr_simple > 0.8

    print(f"\n{'PASS' if all_pass else 'FAIL'}: q_learning.py")
