"""Markov Decision Process from scratch using NumPy.

Implements:
- Configurable GridWorld environment
- Value Iteration algorithm
- Policy Iteration algorithm
- Policy Evaluation

Reference: Sutton & Barto, "Reinforcement Learning: An Introduction" (2018).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# GridWorld Environment
# ---------------------------------------------------------------------------

class GridWorld:
    """Configurable grid world MDP environment.

    States are cells in an n_rows x n_cols grid. Actions are:
    0=UP, 1=RIGHT, 2=DOWN, 3=LEFT.

    Attributes:
        n_rows, n_cols: Grid dimensions.
        n_states: Total number of states.
        n_actions: Number of actions (4).
        start_state: Index of the starting state.
        terminal_states: Set of terminal state indices.
        obstacles: Set of obstacle state indices (cannot be entered).
        rewards: Reward for each (state, action, next_state) transition.
        P: Transition probabilities [n_states, n_actions, n_states].
    """

    def __init__(
        self,
        n_rows: int = 4,
        n_cols: int = 4,
        goal_states: Optional[list[tuple[int, int]]] = None,
        trap_states: Optional[list[tuple[int, int]]] = None,
        obstacle_positions: Optional[list[tuple[int, int]]] = None,
        step_reward: float = -1.0,
        goal_reward: float = 10.0,
        trap_reward: float = -10.0,
    ) -> None:
        """Initialize the GridWorld environment.

        Args:
            n_rows: Number of rows.
            n_cols: Number of columns.
            goal_states: List of (row, col) goal positions.
            trap_states: List of (row, col) trap positions.
            obstacle_positions: List of (row, col) obstacle positions.
            step_reward: Default reward per step.
            goal_reward: Reward for reaching a goal.
            trap_reward: Reward for falling into a trap.
        """
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.n_states = n_rows * n_cols
        self.n_actions = 4
        self.step_reward = step_reward

        self.start_state = 0
        self.goal_states: set[int] = set()
        self.trap_states: set[int] = set()
        self.obstacles: set[int] = set()

        if goal_states:
            for r, c in goal_states:
                self.goal_states.add(self._rc_to_s(r, c))
        if trap_states:
            for r, c in trap_states:
                self.trap_states.add(self._rc_to_s(r, c))
        if obstacle_positions:
            for r, c in obstacle_positions:
                self.obstacles.add(self._rc_to_s(r, c))

        self.terminal_states = self.goal_states | self.trap_states
        self.terminal_states |= self.obstacles

        # Build transition probabilities and rewards
        self.P = np.zeros((self.n_states, self.n_actions, self.n_states))
        self.R = np.zeros((self.n_states, self.n_actions, self.n_states))

        for s in range(self.n_states):
            if s in self.terminal_states:
                # Terminal/obstacle states: no transitions
                self.P[s, :, s] = 1.0
                continue

            r, c = self._s_to_rc(s)
            for a, (dr, dc) in enumerate([(-1, 0), (0, 1), (1, 0), (0, -1)]):
                nr, nc = r + dr, c + dc
                # Bounce off walls and obstacles
                if nr < 0 or nr >= n_rows or nc < 0 or nc >= n_cols:
                    ns = s  # Stay in place
                else:
                    ns = self._rc_to_s(nr, nc)
                    if ns in self.obstacles:
                        ns = s  # Can't enter obstacle

                self.P[s, a, ns] = 1.0
                # Set reward
                if ns in self.goal_states:
                    self.R[s, a, ns] = goal_reward
                elif ns in self.trap_states:
                    self.R[s, a, ns] = trap_reward
                else:
                    self.R[s, a, ns] = step_reward

    def _rc_to_s(self, r: int, c: int) -> int:
        return r * self.n_cols + c

    def _s_to_rc(self, s: int) -> tuple[int, int]:
        return s // self.n_cols, s % self.n_cols

    def get_expected_reward(self) -> np.ndarray:
        """Compute expected immediate reward R(s, a) = sum_s' P(s'|s,a) * R(s,a,s').

        Returns:
            Expected rewards [n_states, n_actions].
        """
        return np.sum(self.P * self.R, axis=2)


# ---------------------------------------------------------------------------
# Value Iteration
# ---------------------------------------------------------------------------

def value_iteration(
    env: GridWorld,
    gamma: float = 0.9,
    theta: float = 1e-6,
    max_iter: int = 10000,
) -> tuple[np.ndarray, np.ndarray]:
    """Value Iteration algorithm.

    Iteratively updates the value function using the Bellman optimality
    equation until convergence:
        V(s) = max_a [ R(s,a) + gamma * sum_s' P(s'|s,a) * V(s') ]

    Args:
        env: The MDP environment.
        gamma: Discount factor [0, 1).
        theta: Convergence threshold.
        max_iter: Maximum number of iterations.

    Returns:
        Tuple of (V [n_states], policy [n_states]).
    """
    V = np.zeros(env.n_states)
    R_exp = env.get_expected_reward()

    for _ in range(max_iter):
        delta = 0.0
        for s in range(env.n_states):
            if s in env.terminal_states:
                continue
            v_old = V[s]
            # Bellman optimality backup
            q_sa = R_exp[s] + gamma * (env.P[s] @ V)
            V[s] = np.max(q_sa)
            delta = max(delta, abs(v_old - V[s]))
        if delta < theta:
            break

    # Extract optimal policy
    policy = np.zeros(env.n_states, dtype=np.int64)
    for s in range(env.n_states):
        if s in env.terminal_states:
            policy[s] = 0
        else:
            q_sa = R_exp[s] + gamma * (env.P[s] @ V)
            policy[s] = int(np.argmax(q_sa))

    return V, policy


# ---------------------------------------------------------------------------
# Policy Evaluation
# ---------------------------------------------------------------------------

def policy_evaluation(
    policy: np.ndarray,
    env: GridWorld,
    gamma: float = 0.9,
    theta: float = 1e-6,
) -> np.ndarray:
    """Evaluate a given policy by solving the Bellman expectation equation.

    Iterative policy evaluation:
        V(s) = R(s, pi(s)) + gamma * sum_s' P(s'|s, pi(s)) * V(s')

    Args:
        policy: Policy array [n_states] with action indices.
        env: The MDP environment.
        gamma: Discount factor.
        theta: Convergence threshold.

    Returns:
        Value function V [n_states].
    """
    V = np.zeros(env.n_states)

    while True:
        delta = 0.0
        for s in range(env.n_states):
            if s in env.terminal_states:
                continue
            v_old = V[s]
            a = policy[s]
            V[s] = np.sum(env.P[s, a] * (env.R[s, a] + gamma * V))
            delta = max(delta, abs(v_old - V[s]))
        if delta < theta:
            break

    return V


# ---------------------------------------------------------------------------
# Policy Iteration
# ---------------------------------------------------------------------------

def policy_iteration(
    env: GridWorld,
    gamma: float = 0.9,
    theta: float = 1e-6,
) -> tuple[np.ndarray, np.ndarray]:
    """Policy Iteration algorithm.

    Alternates between policy evaluation and policy improvement:
    1. Policy Evaluation: compute V^pi
    2. Policy Improvement: pi(s) = argmax_a Q(s,a)
    Stop when the policy is stable.

    Args:
        env: The MDP environment.
        gamma: Discount factor.
        theta: Convergence threshold.

    Returns:
        Tuple of (V [n_states], optimal_policy [n_states]).
    """
    n_states, n_actions = env.n_states, env.n_actions
    R_exp = env.get_expected_reward()

    # Initialize random deterministic policy
    policy = np.zeros(n_states, dtype=np.int64)
    for s in range(n_states):
        if s not in env.terminal_states:
            policy[s] = np.random.randint(n_actions)

    while True:
        # Policy evaluation
        V = policy_evaluation(policy, env, gamma, theta)

        # Policy improvement
        policy_stable = True
        for s in range(n_states):
            if s in env.terminal_states:
                continue
            old_action = policy[s]
            q_sa = R_exp[s] + gamma * (env.P[s] @ V)
            policy[s] = int(np.argmax(q_sa))
            if old_action != policy[s]:
                policy_stable = False

        if policy_stable:
            break

    return V, policy


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing mdp.py — Markov Decision Process")
    print("=" * 60)

    # Create a 4x4 GridWorld with a goal and a trap
    env = GridWorld(
        n_rows=4,
        n_cols=4,
        goal_states=[(3, 3)],     # bottom-right is goal
        trap_states=[(1, 1)],     # trap in the middle
    )

    print(f"\nEnvironment: {env.n_rows}x{env.n_cols} grid")
    print(f"  Goal: (3,3), Trap: (1,1)")
    print(f"  States: {env.n_states}, Actions: {env.n_actions}")

    # Value Iteration
    V_vi, pi_vi = value_iteration(env, gamma=0.9, theta=1e-6)
    print(f"\n--- Value Iteration ---")
    print(f"  Optimal values:\n{V_vi.reshape(env.n_rows, env.n_cols)}")

    # Policy Iteration
    V_pi, pi_pi = policy_iteration(env, gamma=0.9, theta=1e-6)
    print(f"\n--- Policy Iteration ---")
    print(f"  Optimal values:\n{V_pi.reshape(env.n_rows, env.n_cols)}")

    # Action names
    action_names = ["UP", "RIGHT", "DOWN", "LEFT"]

    # Compare policies
    pi_vi_grid = np.array([action_names[a] for a in pi_vi]).reshape(4, 4)
    pi_pi_grid = np.array([action_names[a] for a in pi_pi]).reshape(4, 4)
    print(f"\n  VI policy:\n{pi_vi_grid}")
    print(f"\n  PI policy:\n{pi_pi_grid}")

    # Verify policies are consistent
    all_pass = True
    policy_match = np.all(pi_vi == pi_pi)
    print(f"\n  Policies match: {policy_match}")
    all_pass = all_pass and policy_match

    # Verify values are similar
    value_close = np.allclose(V_vi, V_pi, rtol=0.1)
    print(f"  Values close: {value_close}")
    all_pass = all_pass and value_close

    # Verify goal state has reasonable value
    goal_s = env._rc_to_s(3, 3)
    print(f"  Goal value (VI): {V_vi[goal_s]:.2f} (should be 0, terminal)")

    # Verify non-terminal states have finite values
    for s in range(env.n_states):
        if s not in env.terminal_states:
            assert np.isfinite(V_vi[s]), f"Non-terminating V[{s}] should be finite"

    print(f"\n{'PASS' if all_pass else 'FAIL'}: mdp.py")
