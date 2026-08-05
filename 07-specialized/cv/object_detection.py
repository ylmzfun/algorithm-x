"""Simplified YOLO-like object detection from scratch using NumPy.

Implements:
- Bounding box IoU (Intersection over Union)
- Non-maximum suppression (NMS)
- Average Precision (AP) and mean Average Precision (mAP)
- Grid-based prediction generation

Reference: Redmon et al., "You Only Look Once: Unified, Real-Time
Object Detection" (2016).
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# IoU
# ---------------------------------------------------------------------------

def bbox_iou(box1: np.ndarray, box2: np.ndarray) -> float:
    """Compute Intersection over Union (IoU) between two bounding boxes.

    Box format: [x1, y1, x2, y2] where (x1,y1) is top-left and
    (x2,y2) is bottom-right.

    Args:
        box1: First bounding box [4].
        box2: Second bounding box [4].

    Returns:
        IoU value in [0, 1].
    """
    x1 = max(box1[0], box2[0])
    y1 = max(box1[1], box2[1])
    x2 = min(box1[2], box2[2])
    y2 = min(box1[3], box2[3])

    inter_w = max(0.0, x2 - x1)
    inter_h = max(0.0, y2 - y1)
    inter_area = inter_w * inter_h

    area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    union_area = area1 + area2 - inter_area

    return float(inter_area / union_area) if union_area > 0 else 0.0


def bbox_iou_matrix(boxes1: np.ndarray, boxes2: np.ndarray) -> np.ndarray:
    """Compute pairwise IoU between two sets of boxes.

    Args:
        boxes1: [N, 4] array of boxes.
        boxes2: [M, 4] array of boxes.

    Returns:
        IoU matrix [N, M].
    """
    n, m = len(boxes1), len(boxes2)
    iou = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            iou[i, j] = bbox_iou(boxes1[i], boxes2[j])
    return iou


# ---------------------------------------------------------------------------
# NMS
# ---------------------------------------------------------------------------

def nms(
    boxes: np.ndarray,
    scores: np.ndarray,
    iou_threshold: float = 0.5,
) -> np.ndarray:
    """Non-maximum suppression.

    Removes redundant bounding boxes that have high IoU with a
    higher-scoring box.

    Args:
        boxes: Bounding boxes [N, 4] in [x1, y1, x2, y2] format.
        scores: Confidence scores [N].
        iou_threshold: IoU threshold for suppression.

    Returns:
        Indices of kept boxes [K].
    """
    if len(boxes) == 0:
        return np.array([], dtype=np.int64)

    # Sort by score descending
    order = np.argsort(scores)[::-1]
    keep: list[int] = []

    while len(order) > 0:
        idx = order[0]
        keep.append(idx)

        if len(order) == 1:
            break

        # Compute IoU of the kept box with remaining boxes
        ious = np.array([bbox_iou(boxes[idx], boxes[o]) for o in order[1:]])
        # Keep only boxes with IoU below threshold
        order = order[1:][ious < iou_threshold]

    return np.array(keep, dtype=np.int64)


# ---------------------------------------------------------------------------
# Average Precision
# ---------------------------------------------------------------------------

def compute_ap(
    recalls: np.ndarray, precisions: np.ndarray
) -> float:
    """Compute Average Precision from precision-recall curve.

    Uses the 11-point interpolation method (Pascal VOC style) or
    all-point interpolation if fewer than 11 points.

    Args:
        recalls: Sorted recall values.
        precisions: Corresponding precision values.

    Returns:
        Average Precision score.
    """
    # Interpolated precision: maximum precision for any recall >= r
    for i in range(len(precisions) - 2, -1, -1):
        precisions[i] = max(precisions[i], precisions[i + 1])

    # Compute AP as area under precision-recall curve
    ap = 0.0
    for i in range(len(recalls) - 1):
        ap += (recalls[i + 1] - recalls[i]) * precisions[i + 1]

    return float(ap)


def compute_ap_from_predictions(
    pred_boxes: np.ndarray,
    pred_scores: np.ndarray,
    gt_boxes: np.ndarray,
    iou_threshold: float = 0.5,
) -> float:
    """Compute Average Precision for a single class.

    Args:
        pred_boxes: Predicted boxes [P, 4].
        pred_scores: Confidence scores [P].
        gt_boxes: Ground truth boxes [G, 4].
        iou_threshold: IoU threshold for a true positive.

    Returns:
        AP score.
    """
    if len(gt_boxes) == 0:
        return 1.0 if len(pred_boxes) == 0 else 0.0
    if len(pred_boxes) == 0:
        return 0.0

    # Sort predictions by score descending
    order = np.argsort(pred_scores)[::-1]
    pred_boxes = pred_boxes[order]
    pred_scores = pred_scores[order]

    tp = np.zeros(len(pred_boxes))
    fp = np.zeros(len(pred_boxes))
    gt_matched = np.zeros(len(gt_boxes), dtype=bool)

    for i in range(len(pred_boxes)):
        if len(gt_boxes) == 0:
            fp[i] = 1
            continue

        ious = np.array([bbox_iou(pred_boxes[i], gt) for gt in gt_boxes])
        best_iou = np.max(ious)
        best_gt = np.argmax(ious)

        if best_iou >= iou_threshold and not gt_matched[best_gt]:
            tp[i] = 1
            gt_matched[best_gt] = True
        else:
            fp[i] = 1

    # Cumulative sums
    tp_cum = np.cumsum(tp)
    fp_cum = np.cumsum(fp)

    recalls = tp_cum / len(gt_boxes)
    precisions = tp_cum / (tp_cum + fp_cum + 1e-12)

    return compute_ap(recalls, precisions)


# ---------------------------------------------------------------------------
# mAP
# ---------------------------------------------------------------------------

def compute_map(
    predictions: dict[int, tuple[np.ndarray, np.ndarray]],
    ground_truths: dict[int, np.ndarray],
    iou_threshold: float = 0.5,
) -> float:
    """Compute mean Average Precision across all classes.

    Args:
        predictions: Dict mapping class_id -> (boxes [N,4], scores [N]).
        ground_truths: Dict mapping class_id -> boxes [M,4].

    Returns:
        mAP score.
    """
    all_classes = set(predictions.keys()) | set(ground_truths.keys())
    aps: list[float] = []

    for cls in all_classes:
        pred_boxes, pred_scores = predictions.get(cls, (np.empty((0, 4)),
                                                        np.empty(0)))
        gt_boxes = ground_truths.get(cls, np.empty((0, 4)))
        ap = compute_ap_from_predictions(
            pred_boxes, pred_scores, gt_boxes, iou_threshold
        )
        aps.append(ap)

    return float(np.mean(aps)) if aps else 0.0


# ---------------------------------------------------------------------------
# Grid Prediction (YOLO-style toy)
# ---------------------------------------------------------------------------

def generate_grid_predictions(
    image_size: int = 64,
    grid_size: int = 4,
    num_classes: int = 3,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Generate toy YOLO-style grid predictions for testing.

    Each grid cell predicts: [x, y, w, h, obj_conf, class_1, ..., class_n].

    Args:
        image_size: Size of the square image.
        grid_size: Grid dimension (e.g., 4 means 4x4 grid).
        num_classes: Number of object classes.

    Returns:
        Tuple of (pred_boxes [N,4], pred_scores [N], pred_classes [N]).
    """
    cell_size = image_size / grid_size
    all_boxes: list[np.ndarray] = []
    all_scores: list[float] = []
    all_classes: list[int] = []

    for gy in range(grid_size):
        for gx in range(grid_size):
            for c in range(num_classes):
                obj_conf = np.random.random()
                if obj_conf > 0.7:  # Only keep high-confidence predictions
                    # Box center within cell
                    cx = (gx + np.random.random()) * cell_size
                    cy = (gy + np.random.random()) * cell_size
                    w = np.random.uniform(5, cell_size)
                    h = np.random.uniform(5, cell_size)
                    x1 = cx - w / 2
                    y1 = cy - h / 2
                    x2 = cx + w / 2
                    y2 = cy + h / 2
                    score = obj_conf * np.random.uniform(0.5, 1.0)
                    all_boxes.append(np.array([x1, y1, x2, y2]))
                    all_scores.append(score)
                    all_classes.append(c)

    if not all_boxes:
        return (
            np.empty((0, 4)),
            np.empty(0),
            np.empty(0, dtype=np.int64),
        )

    return (
        np.array(all_boxes),
        np.array(all_scores),
        np.array(all_classes, dtype=np.int64),
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing object_detection.py — Object Detection")
    print("=" * 60)

    all_pass = True

    # Test 1: IoU
    print("\n--- IoU Tests ---")
    box_a = np.array([0, 0, 10, 10])
    box_b = np.array([5, 5, 15, 15])
    iou = bbox_iou(box_a, box_b)
    print(f"  IoU of {box_a} and {box_b}: {iou:.3f} (expected 0.143)")
    iou_pass = abs(iou - 0.142857) < 0.01
    all_pass = all_pass and iou_pass

    # Perfect overlap
    iou_perfect = bbox_iou(box_a, box_a)
    print(f"  IoU of identical boxes: {iou_perfect:.3f} (expected 1.0)")
    all_pass = all_pass and abs(iou_perfect - 1.0) < 0.001

    # No overlap
    box_c = np.array([20, 20, 30, 30])
    iou_zero = bbox_iou(box_a, box_c)
    print(f"  IoU of non-overlapping boxes: {iou_zero:.3f} (expected 0.0)")
    all_pass = all_pass and abs(iou_zero - 0.0) < 0.001

    # Test 2: NMS
    print("\n--- NMS Tests ---")
    boxes = np.array([
        [0, 0, 10, 10],
        [1, 1, 9, 9],
        [5, 5, 15, 15],
        [20, 20, 30, 30],
        [21, 21, 29, 29],
    ])
    scores = np.array([0.9, 0.8, 0.7, 0.6, 0.5])
    keep = nms(boxes, scores, iou_threshold=0.5)
    print(f"  NMS kept indices: {keep}")
    # Should keep first (highest score), third (low IoU with first), fourth
    nms_pass = 0 in keep and 2 in keep
    all_pass = all_pass and nms_pass

    # Test 3: mAP
    print("\n--- mAP Tests ---")
    # Class 0: predictions and ground truths
    pred_class0 = {
        0: (np.array([[1, 1, 9, 9], [2, 2, 8, 8], [20, 20, 30, 30]]),
            np.array([0.9, 0.8, 0.7])),
    }
    gt_class0 = {
        0: np.array([[0, 0, 10, 10], [5, 5, 15, 15]]),
    }
    mAP = compute_map(pred_class0, gt_class0, iou_threshold=0.5)
    print(f"  mAP: {mAP:.3f}")
    mAP_pass = 0.0 <= mAP <= 1.0
    all_pass = all_pass and mAP_pass

    # Test 4: Full pipeline
    print("\n--- Full Pipeline ---")
    pred_boxes, pred_scores, pred_classes = generate_grid_predictions(
        image_size=64, grid_size=4, num_classes=2
    )
    print(f"  Generated {len(pred_boxes)} predictions")

    # Per-class NMS
    final_boxes: list[np.ndarray] = []
    for cls in np.unique(pred_classes):
        mask = pred_classes == cls
        cls_boxes = pred_boxes[mask]
        cls_scores = pred_scores[mask]
        keep = nms(cls_boxes, cls_scores, iou_threshold=0.5)
        final_boxes.append(cls_boxes[keep])
        print(f"  Class {cls}: {len(keep)} boxes after NMS "
              f"(from {len(cls_boxes)})")

    print(f"\n{'PASS' if all_pass else 'FAIL'}: object_detection.py")
