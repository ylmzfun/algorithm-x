"""
Information Theory: Entropy and Related Measures for ML/AI Foundations.

Implements:
- Shannon entropy for discrete distributions
- Joint entropy
- Conditional entropy
- Mutual information
- Cross-entropy
- KL divergence (Kullback-Leibler divergence, with numerical stability)

All measures are fundamental to ML: loss functions, decision trees,
variational inference, and information bottleneck methods.
"""

import numpy as np
from numpy.typing import NDArray
from typing import Dict
from math import log2


# ============================================================
# Shannon Entropy
# ============================================================

def entropy(p: NDArray[np.float64], base: float = 2.0) -> float:
    """Compute Shannon entropy H(X) = -Σ p(x) * log_b(p(x)).

    Measures the average uncertainty/information content of a random variable.
    - H = 0: no uncertainty (deterministic, one outcome with p=1).
    - H = log₂(k): maximum uncertainty for k equally likely outcomes (uniform).

    Uses 0 * log(0) = 0 convention by masking zero probabilities.

    Args:
        p: Probability mass function (non-negative, sums to 1).
        base: Logarithm base (2 = bits, e = nats, 10 = dits).

    Returns:
        Entropy in the specified units.

    Raises:
        ValueError: If p does not sum to 1 (within tolerance) or has negatives.

    Complexity: O(n) where n = len(p).

    Example:
        >>> entropy(np.array([0.5, 0.5]))
        1.0  # fair coin: 1 bit of entropy
        >>> entropy(np.array([1.0, 0.0]))
        0.0  # deterministic: 0 bits
    """
    p = np.asarray(p, dtype=np.float64)

    if np.any(p < 0):
        raise ValueError("Probabilities must be non-negative")
    if abs(np.sum(p) - 1.0) > 1e-10:
        raise ValueError(f"Probabilities must sum to 1, got {np.sum(p)}")

    # Mask zero probabilities: 0 * log(0) = 0
    non_zero = p > 0
    if base == 2.0:
        return float(-np.sum(p[non_zero] * np.log2(p[non_zero])))
    elif base == np.e:
        return float(-np.sum(p[non_zero] * np.log(p[non_zero])))
    else:
        return float(-np.sum(p[non_zero] * np.log(p[non_zero]) / np.log(base)))


def binary_entropy(p: float) -> float:
    """Compute entropy of a Bernoulli(p) random variable.

    H(p) = -p log₂(p) - (1-p) log₂(1-p)

    Args:
        p: Success probability in [0, 1].

    Returns:
        Binary entropy in bits.
    """
    if p <= 0 or p >= 1:
        return 0.0
    return float(-p * log2(p) - (1 - p) * log2(1 - p))


# ============================================================
# Joint Entropy
# ============================================================

def joint_entropy(
    joint_pmf: NDArray[np.float64],
    base: float = 2.0
) -> float:
    """Compute joint entropy H(X, Y) = -Σ p(x, y) * log(p(x, y)).

    Measures total uncertainty in the joint distribution of two variables.
    H(X, Y) = H(X) + H(Y|X) = H(Y) + H(X|Y)

    Args:
        joint_pmf: Joint probability matrix of shape (|X|, |Y|).
                   joint_pmf[i, j] = P(X=x_i, Y=y_j).
        base: Logarithm base.

    Returns:
        Joint entropy.

    Complexity: O(|X| * |Y|).

    Example:
        >>> jp = np.array([[0.5, 0.0], [0.0, 0.5]])
        >>> joint_entropy(jp)
        1.0  # X and Y are perfectly correlated, H(X,Y)=H(X)=1
    """
    joint_pmf = np.asarray(joint_pmf, dtype=np.float64)
    non_zero = joint_pmf > 0
    if base == 2.0:
        return float(-np.sum(joint_pmf[non_zero] * np.log2(joint_pmf[non_zero])))
    else:
        return float(-np.sum(joint_pmf[non_zero] * np.log(joint_pmf[non_zero]) / np.log(base)))


# ============================================================
# Conditional Entropy
# ============================================================

def conditional_entropy(
    joint_pmf: NDArray[np.float64],
    base: float = 2.0
) -> float:
    """Compute conditional entropy H(Y|X) = Σ p(x) * H(Y|X=x).

    Measures the remaining uncertainty about Y after knowing X.
    H(Y|X) = H(X, Y) - H(X)

    Args:
        joint_pmf: Joint probability matrix (|X|, |Y|).
        base: Logarithm base.

    Returns:
        Conditional entropy H(Y|X).

    Complexity: O(|X| * |Y|).

    Example:
        >>> # X and Y independent, H(Y|X) = H(Y) = 1
        >>> jp = np.array([[0.25, 0.25], [0.25, 0.25]])
        >>> conditional_entropy(jp)
        1.0
    """
    joint_pmf = np.asarray(joint_pmf, dtype=np.float64)

    # Marginal p(x)
    p_x = np.sum(joint_pmf, axis=1)

    h_y_given_x = 0.0
    for i, px in enumerate(p_x):
        if px > 0:
            p_y_given_x = joint_pmf[i, :] / px
            h_y_given_x += px * entropy(p_y_given_x, base=base)

    return h_y_given_x


# ============================================================
# Mutual Information
# ============================================================

def mutual_information(
    joint_pmf: NDArray[np.float64],
    base: float = 2.0
) -> float:
    """Compute mutual information I(X; Y) = H(X) + H(Y) - H(X, Y).

    Measures how much information X and Y share. Equivalent to the
    reduction in uncertainty about one variable given knowledge of the other.

    I(X; Y) = Σₓ Σ_y p(x, y) * log(p(x, y) / (p(x) * p(y)))

    Properties:
    - I(X; Y) ≥ 0 (always non-negative)
    - I(X; Y) = 0 iff X and Y are independent
    - I(X; Y) = H(X) = H(Y) when X and Y are perfectly correlated

    Args:
        joint_pmf: Joint probability matrix (|X|, |Y|).
        base: Logarithm base.

    Returns:
        Mutual information.

    Complexity: O(|X| * |Y|).
    """
    joint_pmf = np.asarray(joint_pmf, dtype=np.float64)

    p_x = np.sum(joint_pmf, axis=1)
    p_y = np.sum(joint_pmf, axis=0)

    mi = 0.0
    for i in range(joint_pmf.shape[0]):
        for j in range(joint_pmf.shape[1]):
            if joint_pmf[i, j] > 0:
                # p(x,y) / (p(x) * p(y))
                ratio = joint_pmf[i, j] / (p_x[i] * p_y[j])
                if base == 2.0:
                    mi += joint_pmf[i, j] * np.log2(ratio)
                else:
                    mi += joint_pmf[i, j] * np.log(ratio) / np.log(base)

    return float(mi)


# ============================================================
# Cross-Entropy
# ============================================================

def cross_entropy(
    p: NDArray[np.float64],
    q: NDArray[np.float64],
    base: float = 2.0
) -> float:
    """Compute cross-entropy H(p, q) = -Σ p(x) * log(q(x)).

    Measures the average number of bits needed to encode data from
    distribution p using a code optimized for distribution q.

    In ML, cross-entropy is the standard loss function for classification:
        Loss = -Σ y_true * log(y_pred)

    H(p, q) = H(p) + D_KL(p || q) ≥ H(p)

    Args:
        p: True distribution (PMF).
        q: Approximating distribution (PMF). Must have same support and
           q(x) > 0 wherever p(x) > 0 (numerically: uses epsilon clamping).

        base: Logarithm base.

    Returns:
        Cross-entropy H(p, q).

    Complexity: O(n).
    """
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)

    if p.shape != q.shape:
        raise ValueError(f"Shape mismatch: {p.shape} vs {q.shape}")

    # Clamp q to avoid log(0)
    eps = 1e-15
    q_safe = np.clip(q, eps, 1.0)

    if base == 2.0:
        return float(-np.sum(p * np.log2(q_safe)))
    elif base == np.e:
        return float(-np.sum(p * np.log(q_safe)))
    else:
        return float(-np.sum(p * np.log(q_safe) / np.log(base)))


# ============================================================
# KL Divergence
# ============================================================

def kl_divergence(
    p: NDArray[np.float64],
    q: NDArray[np.float64],
    base: float = 2.0
) -> float:
    """Compute Kullback-Leibler divergence D_KL(p || q).

    D_KL(p || q) = Σ p(x) * log(p(x) / q(x))

    Measures how much information is lost when approximating distribution p
    with distribution q. NOT symmetric: D_KL(p||q) ≠ D_KL(q||p).

    Properties:
    - D_KL(p || q) ≥ 0 (Gibbs' inequality)
    - D_KL(p || q) = 0 iff p = q almost everywhere
    - D_KL(p || q) ≠ D_KL(q || p) (asymmetric)

    In ML: KL divergence appears in:
    - Variational inference (ELBO)
    - t-SNE dimensionality reduction
    - Knowledge distillation
    - Regularization (KL penalty on latent variables)

    Numerical stability: uses 0*log(0/q)=0 convention and clamps q.

    Args:
        p: True distribution (PMF).
        q: Approximating distribution (PMF).

        base: Logarithm base.

    Returns:
        KL divergence D_KL(p || q) ≥ 0.

    Complexity: O(n).
    """
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)

    if p.shape != q.shape:
        raise ValueError(f"Shape mismatch: {p.shape} vs {q.shape}")

    eps = 1e-15
    q_safe = np.clip(q, eps, 1.0)

    kl = 0.0
    for i in range(len(p)):
        if p[i] > 0:
            ratio = p[i] / q_safe[i]
            if base == 2.0:
                kl += p[i] * np.log2(ratio)
            elif base == np.e:
                kl += p[i] * np.log(ratio)
            else:
                kl += p[i] * np.log(ratio) / np.log(base)

    return float(kl)


def js_divergence(
    p: NDArray[np.float64],
    q: NDArray[np.float64],
    base: float = 2.0
) -> float:
    """Compute Jensen-Shannon divergence (symmetric version of KL).

    JS(p || q) = (1/2) * D_KL(p || m) + (1/2) * D_KL(q || m)
    where m = (p + q) / 2

    Properties:
    - 0 ≤ JS(p || q) ≤ 1 (when base=2)
    - Symmetric: JS(p||q) = JS(q||p)
    - Square root is a metric

    Args:
        p, q: Probability distributions.
        base: Logarithm base.

    Returns:
        JS divergence.
    """
    p = np.asarray(p, dtype=np.float64)
    q = np.asarray(q, dtype=np.float64)
    m = 0.5 * (p + q)
    return 0.5 * kl_divergence(p, m, base) + 0.5 * kl_divergence(q, m, base)


# ============================================================
# Tests
# ============================================================

def _test_entropy() -> None:
    # Fair coin: H = 1 bit
    assert abs(entropy(np.array([0.5, 0.5])) - 1.0) < 1e-10
    # Deterministic: H = 0
    assert abs(entropy(np.array([1.0, 0.0])) - 0.0) < 1e-10
    # Uniform over 4: H = -4 * (0.25 * log₂(0.25)) = 2 bits
    assert abs(entropy(np.array([0.25] * 4)) - 2.0) < 1e-10
    # Binary entropy
    assert abs(binary_entropy(0.5) - 1.0) < 1e-10
    assert abs(binary_entropy(0.0) - 0.0) < 1e-10
    # Non-uniform
    h = entropy(np.array([0.7, 0.2, 0.1]))
    assert 0 < h < np.log2(3), f"Entropy out of range: {h}"
    print("  PASS: entropy")


def _test_joint_conditional_entropy() -> None:
    # Perfect correlation: P(X=0,Y=0)=0.5, P(X=1,Y=1)=0.5
    jp = np.array([[0.5, 0.0], [0.0, 0.5]])
    h_xy = joint_entropy(jp)
    hy_given_x = conditional_entropy(jp)
    # H(Y|X) = 0 (Y is fully determined by X)
    assert abs(hy_given_x) < 1e-10, f"FAIL H(Y|X): {hy_given_x}"
    # H(X,Y) = H(X) = 1 bit
    assert abs(h_xy - 1.0) < 1e-10, f"FAIL H(X,Y): {h_xy}"

    # Independence: uniform 2×2
    jp_ind = np.ones((3, 3)) / 9.0
    hy_given_x_ind = conditional_entropy(jp_ind)
    # H(Y|X) = H(Y) = log₂(3) ≈ 1.585
    assert abs(hy_given_x_ind - np.log2(3.0)) < 1e-10, \
        f"FAIL H(Y|X) indep: {hy_given_x_ind}"
    print("  PASS: joint and conditional entropy")


def _test_mutual_information() -> None:
    # Independent: I(X;Y) = 0
    jp_ind = np.ones((2, 2)) / 4.0
    mi_ind = mutual_information(jp_ind)
    assert abs(mi_ind) < 1e-10, f"FAIL MI indep: {mi_ind}"

    # Perfect correlation: I(X;Y) = H(X) = 1
    jp_corr = np.array([[0.5, 0.0], [0.0, 0.5]])
    mi_corr = mutual_information(jp_corr)
    assert abs(mi_corr - 1.0) < 1e-10, f"FAIL MI corr: {mi_corr}"

    # Some information
    jp_some = np.array([[0.4, 0.1], [0.1, 0.4]])
    mi_some = mutual_information(jp_some)
    assert 0 < mi_some < 1.0, f"MI should be between 0 and 1: {mi_some}"
    print("  PASS: mutual_information")


def _test_cross_entropy_kl() -> None:
    p = np.array([1.0, 0.0])  # deterministic: class 0
    q_good = np.array([0.9, 0.1])
    q_bad = np.array([0.1, 0.9])

    # Cross-entropy: good model should have lower CE
    ce_good = cross_entropy(p, q_good, base=2.0)
    ce_bad = cross_entropy(p, q_bad, base=2.0)
    assert ce_good < ce_bad, f"CE should be smaller for good model: {ce_good} vs {ce_bad}"
    # H(p) = 0, so CE = KL
    assert abs(ce_good - kl_divergence(p, q_good, base=2.0)) < 1e-10

    # KL divergence properties
    # D_KL(p || p) = 0
    p_test = np.array([0.6, 0.4])
    assert abs(kl_divergence(p_test, p_test)) < 1e-10
    # D_KL ≥ 0
    assert kl_divergence(p_test, np.array([0.5, 0.5])) > 0

    # JS divergence: symmetric
    p1 = np.array([0.9, 0.1])
    p2 = np.array([0.1, 0.9])
    js_12 = js_divergence(p1, p2)
    js_21 = js_divergence(p2, p1)
    assert abs(js_12 - js_21) < 1e-10, "JS not symmetric"
    assert 0 < js_12 <= 1.0, f"JS out of range: {js_12}"

    print("  PASS: cross_entropy and KL/JS divergence")


if __name__ == "__main__":
    print("Testing entropy.py ...")
    _test_entropy()
    _test_joint_conditional_entropy()
    _test_mutual_information()
    _test_cross_entropy_kl()
    print("All entropy tests PASSED!")
