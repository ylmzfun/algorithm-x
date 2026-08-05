"""Classification and regression metrics implemented from scratch.

All functions use numpy and provide sklearn-compatible outputs
for easy comparison during testing.
"""

from __future__ import annotations

import numpy as np
from typing import Optional, Tuple


# ======================================================================
# Classification Metrics
# ======================================================================


def accuracy_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute accuracy classification score.

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
        Ground truth labels.
    y_pred : np.ndarray of shape (n_samples,)
        Predicted labels.

    Returns
    -------
    accuracy : float
    """
    return float(np.mean(y_true == y_pred))


def confusion_matrix(
    y_true: np.ndarray, y_pred: np.ndarray, labels: np.ndarray | None = None
) -> np.ndarray:
    """Compute confusion matrix to evaluate classification accuracy.

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
    y_pred : np.ndarray of shape (n_samples,)
    labels : np.ndarray or None
        List of labels to index the matrix.

    Returns
    -------
    cm : np.ndarray of shape (n_classes, n_classes)
        Rows are true labels, columns are predicted labels.
    """
    if labels is None:
        labels = np.unique(np.concatenate([y_true, y_pred]))
    n_labels = len(labels)
    label_to_idx = {l: i for i, l in enumerate(labels)}
    cm = np.zeros((n_labels, n_labels), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[label_to_idx[t], label_to_idx[p]] += 1
    return cm


def precision_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    average: str = "binary",
    labels: np.ndarray | None = None,
) -> float:
    """Compute precision score.

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
    y_pred : np.ndarray of shape (n_samples,)
    average : str, {'binary', 'macro', 'micro', 'weighted'}
    labels : np.ndarray or None (for macro/micro/weighted)

    Returns
    -------
    precision : float
    """
    cm = confusion_matrix(y_true, y_pred, labels)
    n_classes = cm.shape[0]

    if average == "binary":
        if n_classes != 2:
            raise ValueError("binary average requires exactly 2 classes.")
        tp = cm[1, 1] if n_classes == 2 else cm[0, 0]
        fp = np.sum(cm[:, 1]) - tp if n_classes == 2 else np.sum(cm[:, 0]) - tp
        return float(tp / (tp + fp)) if (tp + fp) > 0 else 0.0

    precisions = np.zeros(n_classes)
    for i in range(n_classes):
        tp = cm[i, i]
        fp = np.sum(cm[:, i]) - tp
        precisions[i] = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    if average == "macro":
        return float(np.mean(precisions))
    elif average == "micro":
        tp_sum = np.sum(np.diag(cm))
        fp_sum = np.sum(cm) - tp_sum  # total predictions - tp = fp
        return float(tp_sum / (tp_sum + fp_sum)) if (tp_sum + fp_sum) > 0 else 0.0
    elif average == "weighted":
        support = np.sum(cm, axis=1)
        return float(np.average(precisions, weights=support)) if np.sum(support) > 0 else 0.0
    else:
        raise ValueError(f"Unknown average: {average}")


def recall_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    average: str = "binary",
    labels: np.ndarray | None = None,
) -> float:
    """Compute recall score.

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
    y_pred : np.ndarray of shape (n_samples,)
    average : str, {'binary', 'macro', 'micro', 'weighted'}
    labels : np.ndarray or None

    Returns
    -------
    recall : float
    """
    cm = confusion_matrix(y_true, y_pred, labels)
    n_classes = cm.shape[0]

    if average == "binary":
        if n_classes != 2:
            raise ValueError("binary average requires exactly 2 classes.")
        tp = cm[1, 1] if n_classes == 2 else cm[0, 0]
        fn = np.sum(cm[1, :]) - tp if n_classes == 2 else np.sum(cm[0, :]) - tp
        return float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0

    recalls = np.zeros(n_classes)
    for i in range(n_classes):
        tp = cm[i, i]
        fn = np.sum(cm[i, :]) - tp
        recalls[i] = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    if average == "macro":
        return float(np.mean(recalls))
    elif average == "micro":
        tp_sum = np.sum(np.diag(cm))
        fn_sum = 0.0  # micro: tp / (tp + 0) = 1 if no FN
        # Actually micro recall = micro precision for multi-class
        tp_sum_m = np.sum(np.diag(cm))
        fn_sum_m = np.sum(cm) - tp_sum_m  # total true - tp = fn (equivalent)
        # For micro, recall = tp / (tp + fn) where all are summed across classes
        return float(tp_sum_m / np.sum(cm)) if np.sum(cm) > 0 else 0.0
    elif average == "weighted":
        support = np.sum(cm, axis=1)
        return float(np.average(recalls, weights=support)) if np.sum(support) > 0 else 0.0
    else:
        raise ValueError(f"Unknown average: {average}")


def f1_score(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    average: str = "binary",
    labels: np.ndarray | None = None,
) -> float:
    """Compute F1 score.

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
    y_pred : np.ndarray of shape (n_samples,)
    average : str, {'binary', 'macro', 'micro', 'weighted'}
    labels : np.ndarray or None

    Returns
    -------
    f1 : float
    """
    if average == "binary":
        p = precision_score(y_true, y_pred, average="binary", labels=labels)
        r = recall_score(y_true, y_pred, average="binary", labels=labels)
    else:
        p = precision_score(y_true, y_pred, average=average, labels=labels)
        r = recall_score(y_true, y_pred, average=average, labels=labels)
    return float(2 * p * r / (p + r)) if (p + r) > 0 else 0.0


def roc_curve(
    y_true: np.ndarray, y_score: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Compute Receiver Operating Characteristic (ROC) curve.

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
        Binary labels (0 or 1).
    y_score : np.ndarray of shape (n_samples,)
        Predicted probabilities for the positive class.

    Returns
    -------
    fpr : np.ndarray
        False positive rate.
    tpr : np.ndarray
        True positive rate.
    thresholds : np.ndarray
        Threshold values.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_score = np.asarray(y_score)

    # Sort by descending score
    desc_indices = np.argsort(y_score)[::-1]
    y_score = y_score[desc_indices]
    y_true = y_true[desc_indices]

    # Unique thresholds (add inf at both ends)
    distinct_indices = np.where(np.diff(y_score))[0]
    threshold_indices = np.r_[distinct_indices, len(y_true) - 1]

    tpr = np.zeros(len(threshold_indices) + 2)
    fpr = np.zeros(len(threshold_indices) + 2)
    thresholds = np.zeros(len(threshold_indices) + 2)

    # Start: threshold > max score -> predict all 0
    tpr[0], fpr[0] = 0.0, 0.0
    thresholds[0] = y_score[0] + 1.0 if len(y_score) > 0 else 1.0

    n_pos = np.sum(y_true)
    n_neg = len(y_true) - n_pos

    tp, fp = 0, 0
    j = 0
    for i in range(len(y_true)):
        if y_true[i] == 1:
            tp += 1
        else:
            fp += 1

        if i == threshold_indices[j]:
            j += 1
            tpr[j] = tp / n_pos if n_pos > 0 else 0
            fpr[j] = fp / n_neg if n_neg > 0 else 0
            thresholds[j] = y_score[i]

    # End: threshold <= min score -> predict all 1
    tpr[-1] = 1.0
    fpr[-1] = 1.0
    thresholds[-1] = y_score[-1] - 1.0 if len(y_score) > 0 else 0.0

    return fpr, tpr, thresholds


def roc_auc_score(y_true: np.ndarray, y_score: np.ndarray) -> float:
    """Compute Area Under the ROC Curve (AUC).

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
        Binary labels (0 or 1).
    y_score : np.ndarray of shape (n_samples,)
        Predicted probabilities for the positive class.

    Returns
    -------
    auc : float
    """
    fpr, tpr, _ = roc_curve(y_true, y_score)
    # Trapezoidal rule
    return float(np.trapz(tpr, fpr))


def log_loss(y_true: np.ndarray, y_pred: np.ndarray, eps: float = 1e-15) -> float:
    """Compute log loss (cross-entropy loss).

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,) or (n_samples, n_classes)
        Ground truth labels (binary) or one-hot encoded.
    y_pred : np.ndarray of shape (n_samples,) or (n_samples, n_classes)
        Predicted probabilities.

    Returns
    -------
    loss : float
    """
    y_pred = np.clip(np.asarray(y_pred, dtype=np.float64), eps, 1 - eps)

    if y_pred.ndim == 1:
        y_true = np.asarray(y_true, dtype=np.float64)
        return float(-np.mean(y_true * np.log(y_pred) + (1 - y_true) * np.log(1 - y_pred)))
    else:
        y_true = np.asarray(y_true, dtype=np.float64)
        return float(-np.sum(y_true * np.log(y_pred)) / y_true.shape[0])


# ======================================================================
# Regression Metrics
# ======================================================================


def mean_squared_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute mean squared error (MSE).

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
    y_pred : np.ndarray of shape (n_samples,)

    Returns
    -------
    mse : float
    """
    return float(np.mean((y_true - y_pred) ** 2))


def mean_absolute_error(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute mean absolute error (MAE).

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
    y_pred : np.ndarray of shape (n_samples,)

    Returns
    -------
    mae : float
    """
    return float(np.mean(np.abs(y_true - y_pred)))


def r2_score(y_true: np.ndarray, y_pred: np.ndarray) -> float:
    """Compute R² (coefficient of determination).

    Parameters
    ----------
    y_true : np.ndarray of shape (n_samples,)
    y_pred : np.ndarray of shape (n_samples,)

    Returns
    -------
    r2 : float
    """
    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return float(1 - ss_res / ss_tot) if ss_tot > 0 else 0.0


# ======================================================================
# Tests
# ======================================================================

if __name__ == "__main__":
    print("=== Testing Metrics ===")

    np.random.seed(42)
    n = 200

    # --- Classification metrics ---
    y_true_bin = np.array([0, 0, 1, 1, 0, 0, 1, 1], dtype=int)
    y_pred_bin = np.array([0, 1, 0, 1, 0, 1, 0, 1], dtype=int)

    # Accuracy
    acc = accuracy_score(y_true_bin, y_pred_bin)
    assert 0 <= acc <= 1, "Accuracy out of range"
    assert acc == 0.5, f"Expected 0.5, got {acc}"

    # Confusion matrix
    cm = confusion_matrix(y_true_bin, y_pred_bin)
    assert cm.shape == (2, 2), f"CM shape: {cm.shape}"
    assert cm[0, 0] == 2 and cm[1, 1] == 2, f"CM diag: {cm}"

    # Precision, Recall, F1 (binary)
    p = precision_score(y_true_bin, y_pred_bin, average="binary")
    r = recall_score(y_true_bin, y_pred_bin, average="binary")
    f1 = f1_score(y_true_bin, y_pred_bin, average="binary")
    assert np.isclose(p, 0.5), f"Precision: {p}"
    assert np.isclose(r, 0.5), f"Recall: {r}"
    assert np.isclose(f1, 0.5), f"F1: {f1}"
    print("  Classification (binary): PASS")

    # Multi-class metrics
    y_true_mc = np.array([0, 0, 1, 1, 2, 2, 0, 1, 2], dtype=int)
    y_pred_mc = np.array([0, 0, 1, 1, 2, 1, 0, 1, 2], dtype=int)
    p_macro = precision_score(y_true_mc, y_pred_mc, average="macro")
    assert 0 <= p_macro <= 1
    print("  Classification (multi-class): PASS")

    # ROC / AUC
    y_score = np.array([0.1, 0.4, 0.35, 0.8, 0.2, 0.3, 0.45, 0.9])
    fpr, tpr, thresh = roc_curve(y_true_bin, y_score)
    assert len(fpr) == len(tpr), "ROC curve length mismatch"
    auc = roc_auc_score(y_true_bin, y_score)
    assert 0 <= auc <= 1, f"AUC out of range: {auc}"
    print("  ROC / AUC: PASS")

    # Log loss
    y_prob = np.array([0.9, 0.1, 0.8, 0.2, 0.7, 0.3, 0.6, 0.4])
    ll = log_loss(y_true_bin, y_prob)
    assert ll >= 0, f"Log loss negative: {ll}"
    print("  Log loss: PASS")

    # --- Regression metrics ---
    y_true_reg = np.array([3.0, -0.5, 2.0, 7.0])
    y_pred_reg = np.array([2.5, 0.0, 2.0, 8.0])

    mse = mean_squared_error(y_true_reg, y_pred_reg)
    assert np.isclose(mse, 0.375), f"MSE: {mse}"

    mae = mean_absolute_error(y_true_reg, y_pred_reg)
    assert np.isclose(mae, 0.5), f"MAE: {mae}"

    r2 = r2_score(y_true_reg, y_pred_reg)
    # Perfect prediction test
    r2_perf = r2_score(y_true_reg, y_true_reg)
    assert np.isclose(r2_perf, 1.0), f"R² perfect: {r2_perf}"
    print("  Regression: PASS")

    print("All metrics tests PASSED!\n")
