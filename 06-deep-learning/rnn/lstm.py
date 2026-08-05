"""LSTM (Long Short-Term Memory) cell and layer from scratch using NumPy.

LSTM equations:
    f_t = σ(W_f @ [h_{t-1}, x_t] + b_f)     # forget gate
    i_t = σ(W_i @ [h_{t-1}, x_t] + b_i)     # input gate
    g_t = tanh(W_g @ [h_{t-1}, x_t] + b_g)  # candidate cell
    o_t = σ(W_o @ [h_{t-1}, x_t] + b_o)     # output gate
    c_t = f_t * c_{t-1} + i_t * g_t         # cell state
    h_t = o_t * tanh(c_t)                   # hidden state
"""

import numpy as np
from typing import Optional


class LSTMCell:
    """A single LSTM cell."""

    def __init__(self, input_size: int, hidden_size: int, random_seed: Optional[int] = 42):
        """Initialize LSTM cell.

        Args:
            input_size: Dimension of input features.
            hidden_size: Dimension of hidden/cell state.
            random_seed: Seed for reproducible weight initialization.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        rng = np.random.RandomState(random_seed)

        # Combined weights: (input_size + hidden_size, 4 * hidden_size)
        scale = np.sqrt(1.0 / hidden_size)
        self.W = rng.randn(input_size + hidden_size, 4 * hidden_size) * scale
        self.b = np.zeros((1, 4 * hidden_size))

        # Initialize forget gate bias to 1.0 (helps with gradient flow)
        self.b[0, hidden_size:2 * hidden_size] = 1.0

        self._cache: dict = {}

    def forward(self, x: np.ndarray, h_prev: np.ndarray,
                c_prev: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Forward pass for one time step.

        Args:
            x: Input of shape (batch_size, input_size).
            h_prev: Previous hidden state of shape (batch_size, hidden_size).
            c_prev: Previous cell state of shape (batch_size, hidden_size).

        Returns:
            Tuple of (h_next, c_next), each of shape (batch_size, hidden_size).
        """
        # Concatenate input and previous hidden
        xh = np.hstack((x, h_prev))  # (batch, input_size + hidden_size)

        # Compute all gates at once
        gates = np.dot(xh, self.W) + self.b  # (batch, 4 * hidden_size)

        # Split gates
        f = gates[:, 0:self.hidden_size]                           # forget gate
        i = gates[:, self.hidden_size:2 * self.hidden_size]        # input gate
        g = gates[:, 2 * self.hidden_size:3 * self.hidden_size]    # candidate
        o = gates[:, 3 * self.hidden_size:4 * self.hidden_size]    # output gate

        # Apply activations
        f = 1.0 / (1.0 + np.exp(-f))          # sigmoid
        i = 1.0 / (1.0 + np.exp(-np.clip(i, -500, 500)))  # sigmoid
        g = np.tanh(g)                          # tanh
        o = 1.0 / (1.0 + np.exp(-np.clip(o, -500, 500)))  # sigmoid

        # Cell state update
        c_next = f * c_prev + i * g
        h_next = o * np.tanh(c_next)

        # Cache for backward pass
        self._cache = {
            "x": x, "h_prev": h_prev, "c_prev": c_prev,
            "f": f, "i": i, "g": g, "o": o,
            "c_next": c_next, "h_next": h_next,
        }
        return h_next, c_next

    def backward(self, dh_next: np.ndarray, dc_next: np.ndarray
                 ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Backward pass for one LSTM time step.

        Args:
            dh_next: Gradient w.r.t. h_next, shape (batch, hidden_size).
            dc_next: Gradient w.r.t. c_next, shape (batch, hidden_size).

        Returns:
            Tuple of (dx, dh_prev, dc_prev, dW, db).
        """
        cache = self._cache
        x = cache["x"]
        h_prev = cache["h_prev"]
        c_prev = cache["c_prev"]
        c_next = cache["c_next"]
        f = cache["f"]
        i = cache["i"]
        g = cache["g"]
        o = cache["o"]

        # Gradient through h_next = o * tanh(c_next)
        tanh_c = np.tanh(c_next)
        do = dh_next * tanh_c
        dc = dh_next * o * (1 - tanh_c ** 2) + dc_next

        # Gradient through gates
        dc_prev = dc * f
        df = dc * c_prev
        di = dc * g
        dg = dc * i

        # Sigmoid/tanh gradients
        df = df * f * (1 - f)
        di = di * i * (1 - i)
        dg = dg * (1 - g ** 2)
        do = do * o * (1 - o)

        # Concatenate gate gradients
        d_gates = np.hstack((df, di, dg, do))  # (batch, 4*hidden)

        # Weight and bias gradients
        xh = np.hstack((x, h_prev))
        dW = np.dot(xh.T, d_gates)
        db = np.sum(d_gates, axis=0, keepdims=True)

        # Input and hidden gradient
        dxh = np.dot(d_gates, self.W.T)
        dx = dxh[:, :self.input_size]
        dh_prev = dxh[:, self.input_size:]

        return dx, dh_prev, dc_prev, dW, db


class LSTM:
    """Multi-layer LSTM processing full sequences."""

    def __init__(self, input_size: int, hidden_size: int,
                 num_layers: int = 1, random_seed: Optional[int] = 42):
        """Initialize LSTM.

        Args:
            input_size: Input feature dimension.
            hidden_size: Hidden/cell state dimension.
            num_layers: Number of stacked LSTM layers.
            random_seed: Random seed.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.cells: list[LSTMCell] = []
        for layer in range(num_layers):
            in_size = input_size if layer == 0 else hidden_size
            cell = LSTMCell(in_size, hidden_size,
                            random_seed=random_seed + layer if random_seed else None)
            self.cells.append(cell)

        # Output projection
        rng = np.random.RandomState(random_seed + 100 if random_seed else None)
        self.W_out = rng.randn(hidden_size, input_size) * 0.01
        self.b_out = np.zeros((1, input_size))
        self._cache: dict = {}

    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward pass through sequence.

        Args:
            x: Input of shape (seq_len, batch_size, input_size).

        Returns:
            Output predictions of shape (seq_len, batch_size, input_size).
        """
        seq_len, batch_size, _ = x.shape
        h_states = [[np.zeros((batch_size, self.hidden_size))] for _ in range(self.num_layers)]
        c_states = [[np.zeros((batch_size, self.hidden_size))] for _ in range(self.num_layers)]

        for t in range(seq_len):
            inp = x[t]
            for layer in range(self.num_layers):
                h_prev = h_states[layer][-1]
                c_prev = c_states[layer][-1]
                h_new, c_new = self.cells[layer].forward(inp, h_prev, c_prev)
                h_states[layer].append(h_new)
                c_states[layer].append(c_new)
                inp = h_new

        # Project last layer's outputs for prediction
        outputs = np.array([h_states[-1][i] for i in range(1, seq_len + 1)])  # (seq, batch, hidden)
        predictions = np.dot(outputs, self.W_out) + self.b_out  # (seq, batch, input_size)

        self._cache = {
            "x": x, "h_states": h_states, "c_states": c_states,
            "outputs": outputs, "predictions": predictions,
        }
        return predictions

    def backward(self, dout: np.ndarray) -> dict:
        """Simplified backward pass through LSTM (accumulates per-cell gradients).

        Args:
            dout: Gradient w.r.t. predictions, (seq_len, batch, input_size).

        Returns:
            Dict of accumulated gradients.
        """
        cache = self._cache
        seq_len, batch_size, _ = dout.shape

        grads = {}
        dc_next_layer = [np.zeros((batch_size, self.hidden_size)) for _ in range(self.num_layers)]
        dh_next_layer = [np.zeros((batch_size, self.hidden_size)) for _ in range(self.num_layers)]

        for layer in range(self.num_layers):
            grads[f"dW_{layer}"] = np.zeros_like(self.cells[layer].W)
            grads[f"db_{layer}"] = np.zeros_like(self.cells[layer].b)

        grads["dW_out"] = np.zeros_like(self.W_out)
        grads["db_out"] = np.zeros_like(self.b_out)

        for t in reversed(range(seq_len)):
            # Output projection gradient
            dh = np.dot(dout[t], self.W_out.T)
            grads["dW_out"] += np.dot(cache["h_states"][-1][t + 1].T, dout[t])
            grads["db_out"] += np.sum(dout[t], axis=0, keepdims=True)

            dh = dh + dh_next_layer[-1]

            for layer in reversed(range(self.num_layers)):
                cell = self.cells[layer]
                h_idx = t + 1  # cached state index

                # Restore cache
                cell._cache = {
                    "x": (cache["x"][t] if layer == 0
                          else cache["h_states"][layer - 1][h_idx]),
                    "h_prev": cache["h_states"][layer][h_idx - 1],
                    "c_prev": cache["c_states"][layer][h_idx - 1],
                    "f": None, "i": None, "g": None, "o": None,
                    "c_next": cache["c_states"][layer][h_idx],
                    "h_next": cache["h_states"][layer][h_idx],
                }
                # Recompute gates (needed for backward)
                x_in = cell._cache["x"]
                h_in = cell._cache["h_prev"]
                xh = np.hstack((x_in, h_in))
                gates = np.dot(xh, cell.W) + cell.b
                hs = cell.hidden_size
                cell._cache["f"] = 1.0 / (1.0 + np.exp(-gates[:, 0:hs]))
                cell._cache["i"] = 1.0 / (1.0 + np.exp(-np.clip(gates[:, hs:2*hs], -500, 500)))
                cell._cache["g"] = np.tanh(gates[:, 2*hs:3*hs])
                cell._cache["o"] = 1.0 / (1.0 + np.exp(-np.clip(gates[:, 3*hs:4*hs], -500, 500)))

                dx_cell, dh_cell, dc_cell, dW, db = cell.backward(dh, dc_next_layer[layer])

                grads[f"dW_{layer}"] += dW
                grads[f"db_{layer}"] += db
                dc_next_layer[layer] = dc_cell
                dh = dh_cell

            dh_next_layer[-1] = np.zeros_like(dh_next_layer[-1])

        return grads

    def train_step(self, x: np.ndarray, y: np.ndarray, lr: float) -> float:
        """One training step with MSE loss (predict next value).

        Args:
            x: Input sequence of shape (seq_len, batch_size, input_size).
            y: Target (next values) of same shape.
            lr: Learning rate.

        Returns:
            MSE loss.
        """
        preds = self.forward(x)
        loss = float(np.mean((preds - y) ** 2))
        dout = 2.0 * (preds - y) / (y.size / y.shape[-1])

        grads = self.backward(dout)

        # Update parameters
        for layer in range(self.num_layers):
            self.cells[layer].W -= lr * grads[f"dW_{layer}"]
            self.cells[layer].b -= lr * grads[f"db_{layer}"]
        self.W_out -= lr * grads["dW_out"]
        self.b_out -= lr * grads["db_out"]

        return loss


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing LSTM from scratch...")

    np.random.seed(42)

    # Test 1: LSTMCell forward/backward shapes
    cell = LSTMCell(input_size=4, hidden_size=3, random_seed=42)
    x = np.random.randn(2, 4)
    h_prev = np.zeros((2, 3))
    c_prev = np.zeros((2, 3))
    h_next, c_next = cell.forward(x, h_prev, c_prev)
    assert h_next.shape == (2, 3), f"h_next shape wrong: {h_next.shape}"
    assert c_next.shape == (2, 3), f"c_next shape wrong: {c_next.shape}"

    dx, dh_p, dc_p, dW, db = cell.backward(np.ones_like(h_next), np.zeros_like(c_next))
    assert dx.shape == (2, 4), f"dx shape wrong: {dx.shape}"
    assert dW.shape == (7, 12), f"dW shape wrong: {dW.shape}"  # (4+3, 4*3)
    print("  PASS: LSTMCell forward/backward shapes correct")

    # Test 2: Gradient check for LSTMCell
    cell2 = LSTMCell(input_size=2, hidden_size=2, random_seed=99)
    x2 = np.array([[0.5, -0.3], [0.8, 0.1]])
    h2 = np.zeros((2, 2))
    c2 = np.zeros((2, 2))
    h_out, c_out = cell2.forward(x2, h2, c2)
    dx2, _, _, dW2, _ = cell2.backward(np.ones_like(h_out), np.zeros_like(c_out))

    eps = 1e-5
    num_dx = np.zeros_like(x2)
    for i in range(x2.size):
        idx = np.unravel_index(i, x2.shape)
        orig = x2[idx]
        x2[idx] = orig + eps
        hp, _ = cell2.forward(x2, h2, c2)
        lp = np.sum(hp)
        x2[idx] = orig - eps
        hm, _ = cell2.forward(x2, h2, c2)
        lm = np.sum(hm)
        x2[idx] = orig
        num_dx[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(dx2 - num_dx)) / (np.max(np.abs(num_dx)) + 1e-10)
    assert max_err < 1e-4, f"LSTM gradient check failed: {max_err:.2e}"
    print(f"  PASS: LSTM gradient check, max rel error = {max_err:.2e}")

    # Test 3: LSTM sequence prediction (sine wave)
    seq_len, batch, dim = 20, 1, 1
    t = np.linspace(0, 4 * np.pi, seq_len + batch * 0)  # one batch of length 20
    sine = np.sin(t[:seq_len]).reshape(seq_len, batch, dim) * 0.0  # placeholder

    # Create sine wave data
    x_sine = np.zeros((seq_len, batch, dim))
    y_sine = np.zeros((seq_len, batch, dim))
    for i in range(seq_len - 1):
        x_sine[i] = np.sin(t[i]).reshape(batch, dim)
        y_sine[i] = np.sin(t[i + 1]).reshape(batch, dim)

    lstm = LSTM(input_size=1, hidden_size=8, num_layers=1, random_seed=42)
    initial_loss = lstm.train_step(x_sine, y_sine, lr=0.01)

    losses = []
    for _ in range(500):
        loss = lstm.train_step(x_sine, y_sine, lr=0.05)
        losses.append(loss)

    assert losses[-1] < initial_loss, f"Loss did not decrease: {initial_loss:.4f} → {losses[-1]:.4f}"
    print(f"  PASS: LSTM sine prediction: loss {initial_loss:.4f} → {losses[-1]:.4f}")

    # Test 4: Forward pass produces finite outputs
    x_test = np.random.randn(5, 3, 2)
    lstm2 = LSTM(input_size=2, hidden_size=4, num_layers=1, random_seed=42)
    out = lstm2.forward(x_test)
    assert out.shape == (5, 3, 2), f"LSTM output shape wrong: {out.shape}"
    assert np.all(np.isfinite(out)), "LSTM output contains NaN/Inf"
    print(f"  PASS: LSTM output shape: {out.shape}, all finite")

    print("\nAll LSTM tests passed!")
