"""
Information Theory Applications for ML/AI Foundations.

Demonstrates practical uses of information-theoretic concepts:
- Decision tree split criterion (entropy vs Gini impurity)
- KL divergence as a loss function in ML
- Entropy as a measure of prediction uncertainty
"""

import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple, Dict
from entropy import entropy, cross_entropy, kl_divergence, binary_entropy


# ============================================================
# Decision Tree Split Criteria
# ============================================================

def gini_impurity(labels: NDArray[np.int64]) -> float:
    """Compute Gini impurity of a set of labels.

    Gini = 1 - Σ p_k²

    where p_k is the proportion of class k in the node.

    Gini impurity measures the probability of misclassifying a randomly
    chosen element if it were randomly labeled according to the class
    distribution. Used in CART decision trees.

    Args:
        labels: Array of class labels (0, 1, ..., K-1).

    Returns:
        Gini impurity ∈ [0, 1 - 1/K].
        0 = perfectly pure (all same class).
        1 - 1/K = maximally impure (uniform distribution).

    Complexity: O(n).
    """
    n = len(labels)
    if n == 0:
        return 0.0
    _, counts = np.unique(labels, return_counts=True)
    proportions = counts / n
    return float(1.0 - np.sum(proportions ** 2))


def information_gain(
    parent_labels: NDArray[np.int64],
    left_labels: NDArray[np.int64],
    right_labels: NDArray[np.int64],
    criterion: str = "entropy"
) -> float:
    """Compute information gain from a binary split.

    IG = Impurity(parent) - weighted_impurity(children)

    where weighted_impurity = (n_left/n) * imp(left) + (n_right/n) * imp(right)

    Args:
        parent_labels: Labels before split.
        left_labels: Labels in left child.
        right_labels: Labels in right child.
        criterion: "entropy" for information gain (ID3/C4.5) or
                   "gini" for Gini gain (CART).

    Returns:
        Information gain (higher = better split).

    Complexity: O(n).
    """
    n = len(parent_labels)
    n_left, n_right = len(left_labels), len(right_labels)

    if criterion == "entropy":
        # Compute class probabilities for entropy calculation
        def impurity(labels: NDArray[np.int64]) -> float:
            if len(labels) == 0:
                return 0.0
            _, counts = np.unique(labels, return_counts=True)
            probs = counts / len(labels)
            return entropy(probs, base=2.0)
    elif criterion == "gini":
        impurity = gini_impurity
    else:
        raise ValueError(f"Unknown criterion: {criterion}")

    parent_imp = impurity(parent_labels)
    left_imp = impurity(left_labels)
    right_imp = impurity(right_labels)

    weighted_child_imp = (n_left / n) * left_imp + (n_right / n) * right_imp
    return parent_imp - weighted_child_imp


def best_split_decision_tree_demo() -> None:
    """Demonstrate entropy vs Gini for a decision tree split.

    Example: binary classification with a candidate split.
    """
    print("\n--- Decision Tree Split Demo ---")

    # Parent node: 50 positive, 50 negative
    parent = np.hstack([np.ones(50), np.zeros(50)]).astype(np.int64)

    # Candidate split 1: good split
    left_1 = np.hstack([np.ones(45), np.zeros(5)]).astype(np.int64)
    right_1 = np.hstack([np.ones(5), np.zeros(45)]).astype(np.int64)

    # Candidate split 2: poor split
    left_2 = np.hstack([np.ones(30), np.zeros(20)]).astype(np.int64)
    right_2 = np.hstack([np.ones(20), np.zeros(30)]).astype(np.int64)

    # Candidate split 3: useless split (same distribution as parent)
    left_3 = np.hstack([np.ones(25), np.zeros(25)]).astype(np.int64)
    right_3 = np.hstack([np.ones(25), np.zeros(25)]).astype(np.int64)

    for criterion in ["entropy", "gini"]:
        print(f"\n  Criterion: {criterion}")
        for name, l, r in [("Good", left_1, right_1),
                           ("Poor", left_2, right_2),
                           ("Useless", left_3, right_3)]:
            ig = information_gain(parent, l, r, criterion)
            print(f"    {name:8s} split: IG = {ig:.4f}")
    print()


# ============================================================
# KL Divergence as a Loss Function in ML
# ============================================================

def kl_divergence_loss_demo() -> None:
    """Demonstrate KL divergence as a loss function.

    In variational inference and knowledge distillation, we minimize
    D_KL(target || prediction) to make the prediction match the target.

    Also shows how cross-entropy (standard classification loss) relates
    to KL divergence: CE(p, q) = H(p) + D_KL(p || q).
    """
    print("--- KL Divergence as Loss ---")

    # True distribution (one-hot encoded)
    y_true = np.array([1.0, 0.0, 0.0])  # class 0

    # Model predictions (softmax outputs)
    predictions = {
        "Good (confident)": np.array([0.85, 0.10, 0.05]),
        "Okay (uncertain)": np.array([0.60, 0.25, 0.15]),
        "Bad (wrong)": np.array([0.10, 0.80, 0.10]),
        "Terrible": np.array([0.01, 0.01, 0.98]),
    }

    print(f"  True distribution: {y_true}")
    h_true = entropy(y_true, base=np.e)
    print(f"  H(true) = {h_true:.4f} nats (entropy of true distribution)")

    for name, pred in predictions.items():
        ce = cross_entropy(y_true, pred, base=np.e)
        kl = kl_divergence(y_true, pred, base=np.e)
        # CE = H(p) + KL(p||q)
        print(f"  {name:20s}: CE={ce:.4f}, KL={kl:.4f}, "
              f"CE = H + KL? {abs(ce - (h_true + kl)) < 1e-10}")
    print()


# ============================================================
# Entropy as Uncertainty Measure
# ============================================================

def prediction_uncertainty_demo() -> None:
    """Show how entropy quantifies prediction uncertainty.

    In ML, a model's output probabilities can be summarized by their
    entropy: higher entropy = more uncertain prediction.

    This is used in:
    - Active learning (query most uncertain samples)
    - Confidence calibration
    - Out-of-distribution detection
    """
    print("--- Entropy as Uncertainty Measure ---")

    # Various softmax outputs
    predictions = [
        ("Very confident", np.array([0.99, 0.005, 0.005])),
        ("Confident", np.array([0.80, 0.15, 0.05])),
        ("Somewhat uncertain", np.array([0.50, 0.30, 0.20])),
        ("Very uncertain", np.array([0.34, 0.33, 0.33])),
        ("Pure guess", np.array([0.333, 0.333, 0.334])),
    ]

    max_entropy = np.log2(3)  # maximum for 3 classes = log₂(3) ≈ 1.585

    for label, probs in predictions:
        h = entropy(probs, base=2.0)
        normalized = h / max_entropy  # 0 = confident, 1 = maximally uncertain
        bar = "#" * int(normalized * 20)
        print(f"  {label:20s}: H={h:.4f} bits ({normalized:.2%}) |{bar}")

    print()


# ============================================================
# Tests
# ============================================================

def _test_gini_impurity() -> None:
    # Pure node: Gini = 0
    g = gini_impurity(np.array([1, 1, 1], dtype=np.int64))
    assert abs(g) < 1e-10, f"FAIL pure: {g}"

    # 50-50: Gini = 1 - (0.5² + 0.5²) = 0.5
    g = gini_impurity(np.array([0, 0, 1, 1], dtype=np.int64))
    assert abs(g - 0.5) < 1e-10, f"FAIL 50-50: {g}"

    # 3 classes uniform: Gini = 1 - 3*(1/3)² = 2/3
    g = gini_impurity(np.array([0, 1, 2], dtype=np.int64))
    assert abs(g - 2.0/3.0) < 1e-10, f"FAIL 3-class: {g}"
    print("  PASS: gini_impurity")


def _test_information_gain() -> None:
    parent = np.array([1, 1, 1, 0, 0, 0], dtype=np.int64)
    # Perfect split: left=[1,1,1], right=[0,0,0] → IG = H(parent) = 1
    left = np.array([1, 1, 1], dtype=np.int64)
    right = np.array([0, 0, 0], dtype=np.int64)
    ig_ent = information_gain(parent, left, right, "entropy")
    assert abs(ig_ent - 1.0) < 1e-10, f"FAIL perfect IG entropy: {ig_ent}"
    ig_gini = information_gain(parent, left, right, "gini")
    assert abs(ig_gini - 0.5) < 1e-10, f"FAIL perfect IG gini: {ig_gini}"

    # Useless split (same distribution as parent)
    left2 = np.array([1, 1, 0, 0], dtype=np.int64)
    right2 = np.array([1, 0], dtype=np.int64)
    ig_useless = information_gain(parent, left2, right2, "entropy")
    assert abs(ig_useless) < 1e-10, f"FAIL useless IG: {ig_useless}"
    print("  PASS: information_gain")


def _test_kl_as_loss() -> None:
    y = np.array([1.0, 0.0])
    q1 = np.array([0.9, 0.1])
    q2 = np.array([0.5, 0.5])

    # Better model (q1) should have lower KL
    kl1 = kl_divergence(y, q1)
    kl2 = kl_divergence(y, q2)
    assert kl1 < kl2, f"KL should be smaller for better model: {kl1} vs {kl2}"
    print("  PASS: KL as loss")


if __name__ == "__main__":
    print("Testing information_theory/applications.py ...")
    _test_gini_impurity()
    _test_information_gain()
    _test_kl_as_loss()

    # Demonstration prints
    best_split_decision_tree_demo()
    kl_divergence_loss_demo()
    prediction_uncertainty_demo()

    print("All information_theory applications tests PASSED!")
