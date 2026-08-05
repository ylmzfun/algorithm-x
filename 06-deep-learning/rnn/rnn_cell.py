"""Simple RNN cell and RNN layer from scratch (NumPy).

Implements:
- RNNCell: single step of RNN with tanh activation
- RNN: full sequence processing with BPTT (backpropagation through time)
"""

import numpy as np
from typing import Optional


class RNNCell:
    """A single RNN cell with tanh activation.

    h_t = tanh(W_xh @ x_t + W_hh @ h_{t-1} + b)
    """

    def __init__(self, input_size: int, hidden_size: int, random_seed: Optional[int] = 42):
        """Initialize RNN cell.

        Args:
            input_size: Dimension of input features.
            hidden_size: Dimension of hidden state.
            random_seed: Seed for weight initialization.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        rng = np.random.RandomState(random_seed)

        # Xavier-like initialization
        scale = np.sqrt(1.0 / hidden_size)
        self.W_xh = rng.randn(input_size, hidden_size) * scale
        self.W_hh = rng.randn(hidden_size, hidden_size) * scale
        self.b = np.zeros((1, hidden_size))
        self._cache: dict = {}

    def forward(self, x: np.ndarray, h_prev: np.ndarray) -> np.ndarray:
        """Forward pass for one time step.

        Args:
            x: Input at current time step, shape (batch_size, input_size).
            h_prev: Previous hidden state, shape (batch_size, hidden_size).

        Returns:
            Next hidden state, shape (batch_size, hidden_size).
        """
        z = np.dot(x, self.W_xh) + np.dot(h_prev, self.W_hh) + self.b
        h_next = np.tanh(z)

        self._cache = {"x": x, "h_prev": h_prev, "z": z, "h_next": h_next}
        return h_next

    def backward(self, dh_next: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Backward pass for one time step.

        Args:
            dh_next: Gradient of loss w.r.t. h_next, shape (batch_size, hidden_size).

        Returns:
            Tuple of (dx, dh_prev, dW_xh, dW_hh, db).
        """
        cache = self._cache
        x = cache["x"]
        h_prev = cache["h_prev"]
        z = cache["z"]
        h_next = cache["h_next"]

        # d(tanh(z))/dz = 1 - tanh^2(z) = 1 - h_next^2
        dz = dh_next * (1 - h_next ** 2)

        dW_xh = np.dot(x.T, dz)
        dW_hh = np.dot(h_prev.T, dz)
        db = np.sum(dz, axis=0, keepdims=True)
        dx = np.dot(dz, self.W_xh.T)
        dh_prev = np.dot(dz, self.W_hh.T)

        return dx, dh_prev, dW_xh, dW_hh, db


class RNN:
    """Multi-layer RNN processing full sequences with BPTT."""

    def __init__(self, input_size: int, hidden_size: int, num_layers: int = 1,
                 random_seed: Optional[int] = 42):
        """Initialize RNN.

        Args:
            input_size: Input feature dimension.
            hidden_size: Hidden state dimension.
            num_layers: Number of stacked RNN layers.
            random_seed: Random seed.
        """
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers

        self.cells: list[RNNCell] = []
        for layer in range(num_layers):
            in_size = input_size if layer == 0 else hidden_size
            cell = RNNCell(in_size, hidden_size, random_seed=random_seed + layer if random_seed else None)
            self.cells.append(cell)

        self._cache: dict = {}

    def forward(self, x: np.ndarray,
                h0: Optional[list[np.ndarray]] = None) -> tuple[np.ndarray, list[np.ndarray]]:
        """Forward pass through the full sequence.

        Args:
            x: Input sequence of shape (seq_len, batch_size, input_size).
            h0: Initial hidden states per layer, list of (batch_size, hidden_size).
                If None, zeros are used.

        Returns:
            Tuple of (outputs, h_final).
            outputs: shape (seq_len, batch_size, hidden_size) from last layer.
            h_final: list of final hidden states per layer.
        """
        seq_len, batch_size, _ = x.shape
        if h0 is None:
            h0 = [np.zeros((batch_size, self.hidden_size)) for _ in range(self.num_layers)]

        outputs = np.zeros((seq_len, batch_size, self.hidden_size))
        h_states = [[h0[layer]] for layer in range(self.num_layers)]

        for t in range(seq_len):
            inp = x[t]
            for layer in range(self.num_layers):
                h_prev = h_states[layer][-1]
                h_new = self.cells[layer].forward(inp, h_prev)
                h_states[layer].append(h_new)
                inp = h_new  # input to next layer
            outputs[t] = h_states[-1][-1]

        h_final = [h_states[l][-1] for l in range(self.num_layers)]
        self._cache = {"x": x, "h_states": h_states, "outputs": outputs}
        return outputs, h_final

    def backward(self, dout: np.ndarray) -> tuple[np.ndarray, list[dict]]:
        """Backward pass through time.

        Args:
            dout: Gradient w.r.t. outputs, shape (seq_len, batch_size, hidden_size).

        Returns:
            Tuple of (dx, grads_per_layer).
            dx: Gradient w.r.t. input, shape (seq_len, batch_size, input_size).
            grads_per_layer: List of dicts with dW_xh, dW_hh, db per layer.
        """
        cache = self._cache
        seq_len, batch_size, _ = dout.shape

        # Initialize gradient accumulators
        dx = np.zeros((seq_len, batch_size, self.input_size))
        grads_per_layer: list[dict] = []

        # Gradient flowing from future timesteps per layer
        dh_future = [np.zeros((batch_size, self.hidden_size)) for _ in range(self.num_layers)]

        for layer in range(self.num_layers):
            grads_per_layer.append({
                "dW_xh": np.zeros_like(self.cells[layer].W_xh),
                "dW_hh": np.zeros_like(self.cells[layer].W_hh),
                "db": np.zeros_like(self.cells[layer].b),
            })

        # Process each timestep in reverse
        for t in reversed(range(seq_len)):
            # Gradient into last layer from loss + future
            dh = dout[t] + dh_future[-1]

            for layer in reversed(range(self.num_layers)):
                cell = self.cells[layer]
                # Restore cell's cache for this timestep
                cell._cache = {
                    "x": (cache["x"][t] if layer == 0
                          else cache["h_states"][layer - 1][t + 1]),
                    "h_prev": cache["h_states"][layer][t],
                    "z": None,  # Need to recompute
                    "h_next": cache["h_states"][layer][t + 1],
                }
                # Recompute z from stored values
                cell._cache["z"] = (
                    np.dot(cell._cache["x"], cell.W_xh) +
                    np.dot(cell._cache["h_prev"], cell.W_hh) +
                    cell.b
                )

                dx_cell, dh_prev, dW_xh, dW_hh, db = cell.backward(dh)

                # Accumulate gradients
                grads_per_layer[layer]["dW_xh"] += dW_xh
                grads_per_layer[layer]["dW_hh"] += dW_hh
                grads_per_layer[layer]["db"] += db

                if layer == 0:
                    dx[t] = dx_cell
                else:
                    dh = dh_future[layer - 1] + dx_cell
                    # Update dh for the previous layer at this timestep
                    pass

                dh_future[layer] = dh_prev

            # Reset dh for last layer (no future for current reverse iteration)
            # dh_future has been updated; for next iteration (t-1), dh starts fresh + future

        return dx, grads_per_layer


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing RNN from scratch...")

    np.random.seed(42)

    # Test 1: RNNCell forward and backward shapes
    cell = RNNCell(input_size=4, hidden_size=3, random_seed=42)
    x = np.random.randn(2, 4)  # batch=2, input=4
    h_prev = np.zeros((2, 3))
    h_next = cell.forward(x, h_prev)
    assert h_next.shape == (2, 3), f"Wrong h_next shape: {h_next.shape}"

    dx, dh_prev, dW_xh, dW_hh, db = cell.backward(np.ones_like(h_next))
    assert dx.shape == (2, 4), f"Wrong dx shape: {dx.shape}"
    assert dh_prev.shape == (2, 3), f"Wrong dh_prev shape: {dh_prev.shape}"
    assert dW_xh.shape == (4, 3), f"Wrong dW_xh shape: {dW_xh.shape}"
    print("  PASS: RNNCell forward/backward shapes correct")

    # Test 2: RNN forward on sequence
    rnn = RNN(input_size=4, hidden_size=5, num_layers=1, random_seed=42)
    x_seq = np.random.randn(3, 2, 4)  # seq=3, batch=2, input=4
    outputs, h_final = rnn.forward(x_seq)
    assert outputs.shape == (3, 2, 5), f"Wrong outputs shape: {outputs.shape}"
    assert h_final[0].shape == (2, 5), f"Wrong h_final shape: {h_final[0].shape}"
    print(f"  PASS: RNN forward shape: {outputs.shape}")

    # Test 3: Gradient check for RNNCell
    cell2 = RNNCell(input_size=3, hidden_size=2, random_seed=99)
    x2 = np.array([[1.0, 0.5, -0.3], [0.2, -0.8, 1.5]])
    h2 = np.array([[0.1, -0.2], [0.3, 0.1]])
    h_out = cell2.forward(x2, h2)

    dout = np.ones_like(h_out)
    dx_c, dh_c, dWxh, dWhh, db_c = cell2.backward(dout)

    # Numerical gradient for W_xh
    eps = 1e-5
    num_dWxh = np.zeros_like(cell2.W_xh)
    for i in range(cell2.W_xh.size):
        idx = np.unravel_index(i, cell2.W_xh.shape)
        orig = cell2.W_xh[idx]
        cell2.W_xh[idx] = orig + eps
        hp = cell2.forward(x2, h2)
        lp = np.sum(hp)
        cell2.W_xh[idx] = orig - eps
        hm = cell2.forward(x2, h2)
        lm = np.sum(hm)
        cell2.W_xh[idx] = orig
        num_dWxh[idx] = (lp - lm) / (2 * eps)

    max_err = np.max(np.abs(dWxh - num_dWxh)) / (np.max(np.abs(num_dWxh)) + 1e-10)
    assert max_err < 1e-4, f"RNN gradient check failed: max rel error = {max_err:.2e}"
    print(f"  PASS: RNNCell gradient check, max rel error = {max_err:.2e}")

    # Test 4: Multi-layer RNN
    rnn2 = RNN(input_size=3, hidden_size=4, num_layers=2, random_seed=42)
    x_seq2 = np.random.randn(5, 2, 3)
    outputs2, h_final2 = rnn2.forward(x_seq2)
    assert outputs2.shape == (5, 2, 4), f"Multi-layer RNN output shape wrong: {outputs2.shape}"
    assert len(h_final2) == 2
    print(f"  PASS: Multi-layer RNN output shape: {outputs2.shape}")

    print("\nAll RNN tests passed!")
