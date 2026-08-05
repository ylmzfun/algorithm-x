"""GRU (Gated Recurrent Unit) cell and layer from scratch using NumPy.

GRU equations:
    z_t = σ(W_z @ [h_{t-1}, x_t] + b_z)     # update gate
    r_t = σ(W_r @ [h_{t-1}, x_t] + b_r)     # reset gate
    n_t = tanh(W_n @ [r_t * h_{t-1}, x_t] + b_n)  # new gate (candidate)
    h_t = (1 - z_t) * h_{t-1} + z_t * n_t   # hidden state
"""

import numpy as np
from typing import Optional


class GRUCell:
    """A single GRU cell.

    More parameter-efficient than LSTM (2 gates vs 3).
    """

    def __init__(self, input_size: int, hidden_size: int, random_seed: Optional[int] = 42):
        """Initialize GRU cell.

        Args:
            input_size: Dimension of input features.
            hidden_size: Dimension of hidden state.
            random_seed: Seed for weight initialization.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        rng = np.random.RandomState(random_seed)

        scale = np.sqrt(1.0 / hidden_size)
        # Update gate
        self.W_z = rng.randn(input_size + hidden_size, hidden_size) * scale
        self.b_z = np.zeros((1, hidden_size))
        # Reset gate
        self.W_r = rng.randn(input_size + hidden_size, hidden_size) * scale
        self.b_r = np.zeros((1, hidden_size))
        # New gate
        self.W_n = rng.randn(input_size + hidden_size, hidden_size) * scale
        self.b_n = np.zeros((1, hidden_size))

        self._cache: dict = {}

    def forward(self, x: np.ndarray, h_prev: np.ndarray) -> np.ndarray:
        """Forward pass for one time step.

        Args:
            x: Input of shape (batch_size, input_size).
            h_prev: Previous hidden state of shape (batch_size, hidden_size).

        Returns:
            Next hidden state of shape (batch_size, hidden_size).
        """
        # Concatenate x and h_prev for update and reset gates
        xh = np.hstack((x, h_prev))

        # Update gate
        z = 1.0 / (1.0 + np.exp(-np.clip(np.dot(xh, self.W_z) + self.b_z, -500, 500)))
        # Reset gate
        r = 1.0 / (1.0 + np.exp(-np.clip(np.dot(xh, self.W_r) + self.b_r, -500, 500)))

        # New gate: concatenate x and (r * h_prev)
        x_rh = np.hstack((x, r * h_prev))
        n = np.tanh(np.dot(x_rh, self.W_n) + self.b_n)

        # Hidden state update
        h_next = (1 - z) * h_prev + z * n

        self._cache = {
            "x": x, "h_prev": h_prev,
            "z": z, "r": r, "n": n,
            "h_next": h_next,
        }
        return h_next

    def backward(self, dh_next: np.ndarray
                 ) -> tuple[np.ndarray, np.ndarray, dict]:
        """Backward pass for one GRU time step.

        Args:
            dh_next: Gradient w.r.t. h_next, shape (batch, hidden_size).

        Returns:
            Tuple of (dx, dh_prev, grads) where grads is dict with dW_z, db_z, dW_r, db_r, dW_n, db_n.
        """
        cache = self._cache
        x = cache["x"]
        h_prev = cache["h_prev"]
        z = cache["z"]
        r = cache["r"]
        n = cache["n"]

        # h_next = (1-z) * h_prev + z * n
        dz = dh_next * (n - h_prev)     # d/dz
        dn = dh_next * z                 # d/dn
        dh_prev = dh_next * (1 - z)      # direct path

        # Gradient through n = tanh(W_n @ [x, r*h_prev] + b_n)
        dn_raw = dn * (1 - n ** 2)       # tanh gradient

        # W_n gradients
        x_rh = np.hstack((x, r * h_prev))
        dW_n = np.dot(x_rh.T, dn_raw)
        db_n = np.sum(dn_raw, axis=0, keepdims=True)

        dx_n = np.dot(dn_raw, self.W_n[:self.input_size].T)
        d_rh = np.dot(dn_raw, self.W_n[self.input_size:].T)  # gradient w.r.t (r * h_prev)

        # Through r * h_prev
        dr = d_rh * h_prev
        dh_prev += d_rh * r

        # Gradient through reset gate: r = sigmoid(W_r @ [x, h_prev] + b_r)
        dr_raw = dr * r * (1 - r)
        xh = np.hstack((x, h_prev))
        dW_r = np.dot(xh.T, dr_raw)
        db_r = np.sum(dr_raw, axis=0, keepdims=True)
        dx_r = np.dot(dr_raw, self.W_r[:self.input_size].T)
        dh_r = np.dot(dr_raw, self.W_r[self.input_size:].T)
        dh_prev += dh_r

        # Gradient through update gate: z = sigmoid(W_z @ [x, h_prev] + b_z)
        dz_raw = dz * z * (1 - z)
        dW_z = np.dot(xh.T, dz_raw)
        db_z = np.sum(dz_raw, axis=0, keepdims=True)
        dx_z = np.dot(dz_raw, self.W_z[:self.input_size].T)
        dh_z = np.dot(dz_raw, self.W_z[self.input_size:].T)
        dh_prev += dh_z

        dx = dx_n + dx_r + dx_z

        grads = {
            "dW_z": dW_z, "db_z": db_z,
            "dW_r": dW_r, "db_r": db_r,
            "dW_n": dW_n, "db_n": db_n,
        }
        return dx, dh_prev, grads


class GRU:
    """Multi-layer GRU processing full sequences."""

    def __init__(self, input_size: int, hidden_size: int,
                 num_layers: int = 1, random_seed: Optional[int] = 42):
        """Initialize GRU.

        Args:
            input_size: Input feature dimension.
            hidden_size: Hidden state dimension.
            num_layers: Number of stacked GRU layers.
            random_seed: Random seed.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.cells: list[GRUCell] = []
        for layer in range(num_layers):
            in_size = input_size if layer == 0 else hidden_size
            cell = GRUCell(in_size, hidden_size,
                           random_seed=random_seed + layer if random_seed else None)
            self.cells.append(cell)

        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through sequence.

        Args:
            x: Input of shape (seq_len, batch_size, input_size).

        Returns:
            Hidden states from last layer, shape (seq_len, batch_size, hidden_size).
        """
        seq_len, batch_size, _ = x.shape
        h_states = [[np.zeros((batch_size, self.hidden_size))] for _ in range(self.num_layers)]

        for t in range(seq_len):
            inp = x[t]
            for layer in range(self.num_layers):
                h_prev = h_states[layer][-1]
                h_new = self.cells[layer].forward(inp, h_prev)
                h_states[layer].append(h_new)
                inp = h_new

        outputs = np.array([h_states[-1][i] for i in range(1, seq_len + 1)])
        self._cache = {"x": x, "h_states": h_states, "outputs": outputs}
        return outputs


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing GRU from scratch...")

    np.random.seed(42)

    # Test 1: GRUCell forward/backward shapes
    cell = GRUCell(input_size=4, hidden_size=3, random_seed=42)
    x = np.random.randn(2, 4)
    h_prev = np.zeros((2, 3))
    h_next = cell.forward(x, h_prev)
    assert h_next.shape == (2, 3), f"Wrong h_next shape: {h_next.shape}"

    dx, dh_p, grads = cell.backward(np.ones_like(h_next))
    assert dx.shape == (2, 4), f"Wrong dx shape: {dx.shape}"
    assert dh_p.shape == (2, 3), f"Wrong dh_prev shape: {dh_p.shape}"
    assert "dW_z" in grads and grads["dW_z"].shape == (7, 3)
    print("  PASS: GRUCell forward/backward shapes correct")

    # Test 2: Gradient check for GRUCell
    cell2 = GRUCell(input_size=2, hidden_size=2, random_seed=99)
    x2 = np.array([[0.5, -0.3], [0.1, 0.8]])
    h2 = np.zeros((2, 2))
    h_out = cell2.forward(x2, h2)
    dx2, _, _ = cell2.backward(np.ones_like(h_out))

    eps = 1e-5
    num_dx = np.zeros_like(x2)
    for i in range(x2.size):
        idx = np.unravel_index(i, x2.shape)
        orig = x2[idx]
        x2[idx] = orig + eps
        hp = cell2.forward(x2, h2)
        lp = np.sum(hp)
        x2[idx] = orig - eps
        hm = cell2.forward(x2, h2)
        lm = np.sum(hm)
        x2[idx] = orig
        num_dx[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(dx2 - num_dx)) / (np.max(np.abs(num_dx)) + 1e-10)
    assert max_err < 1e-4, f"GRU gradient check failed: {max_err:.2e}"
    print(f"  PASS: GRU gradient check, max rel error = {max_err:.2e}")

    # Test 3: GRU sequence forward
    gru = GRU(input_size=3, hidden_size=5, num_layers=1, random_seed=42)
    x_seq = np.random.randn(5, 2, 3)
    outputs = gru.forward(x_seq)
    assert outputs.shape == (5, 2, 5), f"GRU output shape wrong: {outputs.shape}"
    assert np.all(np.isfinite(outputs)), "GRU output contains NaN/Inf"
    print(f"  PASS: GRU output shape: {outputs.shape}, all finite")

    # Test 4: Multi-layer GRU
    gru2 = GRU(input_size=2, hidden_size=3, num_layers=2, random_seed=42)
    x_seq2 = np.random.randn(4, 2, 2)
    outputs2 = gru2.forward(x_seq2)
    assert outputs2.shape == (4, 2, 3), f"Multi-layer GRU output shape: {outputs2.shape}"
    print(f"  PASS: Multi-layer GRU output shape: {outputs2.shape}")

    # Test 5: GRU hidden state range
    # GRU hidden state should remain bounded
    x_long = np.random.randn(100, 1, 2) * 2.0
    gru_long = GRU(input_size=2, hidden_size=4, num_layers=1, random_seed=42)
    out_long = gru_long.forward(x_long)
    assert np.max(np.abs(out_long)) < 100, "Hidden states exploded"
    print(f"  PASS: Hidden states bounded: max|h| = {np.max(np.abs(out_long)):.2f}")

    print("\nAll GRU tests passed!")
