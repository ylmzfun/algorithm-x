"""Simulated multi-stage ranking pipeline from scratch.

Implements the typical recommendation ranking pipeline:
1. Recall stage: multiple strategies to generate candidate set
2. Coarse ranking: lightweight model to filter candidates
3. Fine ranking: more complex model for precise scoring
4. Reranking: diversity/business rules for final ordering

This is a simulated implementation for educational purposes.
"""

from __future__ import annotations

import numpy as np
from typing import Optional


# ---------------------------------------------------------------------------
# Item and User representations
# ---------------------------------------------------------------------------

def _generate_items(n_items: int, n_features: int, seed: int = 42) -> np.ndarray:
    """Generate synthetic item feature vectors.

    Args:
        n_items: Number of items.
        n_features: Feature dimension per item.
        seed: Random seed.

    Returns:
        Item features [n_items, n_features].
    """
    rng = np.random.default_rng(seed)
    return rng.normal(0, 1, (n_items, n_features))


def _generate_user(n_features: int, seed: int = 42) -> np.ndarray:
    """Generate a synthetic user profile vector.

    Args:
        n_features: Feature dimension.
        seed: Random seed.

    Returns:
        User vector [n_features].
    """
    rng = np.random.default_rng(seed)
    return rng.normal(0, 1, n_features)


# ---------------------------------------------------------------------------
# Recall Stage
# ---------------------------------------------------------------------------

class RecallStage:
    """Multi-strategy recall stage.

    Retrieves a candidate set of items from the full item pool using
    multiple recall strategies:
    - Random: uniformly sample items
    - Popularity: items with highest average feature norm
    - Embedding-based: cosine similarity in feature space
    """

    def __init__(self, strategies: Optional[list[str]] = None,
                 candidates_per_strategy: int = 20) -> None:
        """Initialize the recall stage.

        Args:
            strategies: List of strategy names ['random', 'popularity', 'embedding'].
            candidates_per_strategy: Number of candidates per strategy.
        """
        self.strategies = strategies or ["random", "popularity", "embedding"]
        self.candidates_per_strategy = candidates_per_strategy

    def recall(
        self, user: np.ndarray, items: np.ndarray
    ) -> np.ndarray:
        """Recall candidates from the item pool.

        Args:
            user: User profile vector [n_features].
            items: All item features [n_items, n_features].

        Returns:
            Candidate item indices [K].
        """
        candidates: set[int] = set()
        n_items = len(items)

        for strategy in self.strategies:
            if strategy == "random":
                # Random sampling
                n_pick = min(self.candidates_per_strategy, n_items)
                picked = np.random.choice(n_items, size=n_pick, replace=False)
                candidates.update(picked.tolist())

            elif strategy == "popularity":
                # Items with highest feature norm (pseudo-popularity)
                popularity = np.linalg.norm(items, axis=1)
                top_n = min(self.candidates_per_strategy, n_items)
                picked = np.argsort(popularity)[::-1][:top_n]
                candidates.update(picked.tolist())

            elif strategy == "embedding":
                # Cosine similarity between user and items
                user_norm = user / (np.linalg.norm(user) + 1e-12)
                item_norms = np.linalg.norm(items, axis=1) + 1e-12
                sims = (items @ user_norm) / item_norms
                top_n = min(self.candidates_per_strategy, n_items)
                picked = np.argsort(sims)[::-1][:top_n]
                candidates.update(picked.tolist())

        return np.array(sorted(candidates), dtype=np.int64)


# ---------------------------------------------------------------------------
# Coarse Ranking Stage
# ---------------------------------------------------------------------------

class CoarseRankingStage:
    """Lightweight coarse ranking model.

    Uses a simple linear model (dot product with learned weights) to
    quickly score and filter candidates.
    """

    def __init__(self, n_features: int, top_k: int = 20, seed: int = 42) -> None:
        """Initialize coarse ranking.

        Args:
            n_features: Feature dimension.
            top_k: Number of candidates to keep.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.top_k = top_k
        # Simulated "learned" weights (in practice, trained on CTR data)
        self.weights: np.ndarray = rng.normal(0, 1, n_features)

    def rank(
        self, user: np.ndarray, item_indices: np.ndarray, items: np.ndarray
    ) -> np.ndarray:
        """Score and filter candidates.

        Score = user · (item ⊙ weights)  (element-wise product)

        Args:
            user: User profile [n_features].
            item_indices: Candidate indices [K].
            items: All items [n_items, n_features].

        Returns:
            Top-k item indices [top_k].
        """
        candidate_items = items[item_indices]  # [K, n_features]
        # Simple linear scoring
        scores = candidate_items @ self.weights  # [K]
        # Bias with user affinity
        user_scores = candidate_items @ user  # [K]
        combined = scores + 0.5 * user_scores

        top_local = np.argsort(combined)[::-1][:self.top_k]
        return item_indices[top_local]


# ---------------------------------------------------------------------------
# Fine Ranking Stage
# ---------------------------------------------------------------------------

class FineRankingStage:
    """More complex fine ranking model.

    Simulates a deeper model with non-linear interactions for precise scoring.
    """

    def __init__(self, n_features: int, hidden_dim: int = 16,
                 top_k: int = 10, seed: int = 42) -> None:
        """Initialize fine ranking.

        Args:
            n_features: Feature dimension.
            hidden_dim: Hidden layer size.
            top_k: Number of candidates to keep.
            seed: Random seed.
        """
        rng = np.random.default_rng(seed)
        self.top_k = top_k
        self.hidden_dim = hidden_dim
        # Simulated 2-layer network weights
        self.W1: np.ndarray = rng.normal(0, 0.5, (n_features, hidden_dim))
        self.W2: np.ndarray = rng.normal(0, 0.5, (hidden_dim, 1))

    def rank(
        self, user: np.ndarray, item_indices: np.ndarray, items: np.ndarray
    ) -> np.ndarray:
        """Score and filter candidates with non-linear model.

        Score = ReLU(item @ W1 + user @ W1) @ W2

        Args:
            user: User profile [n_features].
            item_indices: Candidate indices [K].
            items: All items [n_items, n_features].

        Returns:
            Top-k item indices [top_k].
        """
        candidate_items = items[item_indices]  # [K, n_features]
        # Simulate user-item interaction
        combined = candidate_items + user[np.newaxis, :]  # [K, n_features]
        hidden = np.maximum(0, combined @ self.W1)  # ReLU [K, hidden_dim]
        scores = (hidden @ self.W2).squeeze(-1)  # [K]

        top_local = np.argsort(scores)[::-1][:self.top_k]
        return item_indices[top_local]


# ---------------------------------------------------------------------------
# Reranking Stage
# ---------------------------------------------------------------------------

class RerankingStage:
    """Reranking stage: apply diversity and business rules.

    Reorders the final list to improve diversity (e.g., avoid showing
    too many items of the same category) and apply business rules.
    """

    def __init__(self, diversity_factor: float = 0.3) -> None:
        """Initialize reranking.

        Args:
            diversity_factor: Controls diversity-vs-relevance trade-off.
        """
        self.diversity_factor = diversity_factor

    def rerank(
        self,
        item_indices: np.ndarray,
        items: np.ndarray,
        scores: Optional[np.ndarray] = None,
    ) -> np.ndarray:
        """Rerank items with a simple diversity heuristic.

        Maximizes marginal relevance: alternately picks the highest-scoring
        item and the most diverse item (furthest in feature space from
        already-selected items).

        Args:
            item_indices: Item indices [K].
            items: All items [n_items, n_features].
            scores: Optional relevance scores [K].

        Returns:
            Reranked item indices [K].
        """
        if len(item_indices) <= 2:
            return item_indices

        if scores is None:
            scores = np.ones(len(item_indices))

        candidate_feats = items[item_indices]  # [K, n_features]
        selected: list[int] = []
        remaining = list(range(len(item_indices)))

        # Pick first by score
        first = int(np.argmax(scores))
        selected.append(first)
        remaining.remove(first)

        while remaining:
            # Compute diversity: min cosine distance to already-selected
            sel_feats = candidate_feats[selected]  # [S, n_features]
            rem_feats = candidate_feats[remaining]  # [R, n_features]

            # Normalize
            sel_norm = sel_feats / (np.linalg.norm(sel_feats, axis=1, keepdims=True) + 1e-12)
            rem_norm = rem_feats / (np.linalg.norm(rem_feats, axis=1, keepdims=True) + 1e-12)

            # Max similarity to any selected item
            sims = rem_norm @ sel_norm.T  # [R, S]
            max_sim = np.max(sims, axis=1)  # [R] — higher = more similar = less diverse
            diversity = 1.0 - max_sim  # [R] — higher = more diverse

            # Combined score: relevance + diversity
            rem_scores = scores[remaining]
            combined = rem_scores + self.diversity_factor * diversity * np.max(scores)

            best = remaining[int(np.argmax(combined))]
            selected.append(best)
            remaining.remove(best)

        return item_indices[np.array(selected)]


# ---------------------------------------------------------------------------
# Ranking Pipeline
# ---------------------------------------------------------------------------

class RankingPipeline:
    """Multi-stage ranking pipeline orchestrator.

    Stages: Recall → Coarse Ranking → Fine Ranking → Reranking

    Attributes:
        recall_stage: Recall strategy manager.
        coarse_ranker: Lightweight coarse ranker.
        fine_ranker: Complex fine ranker.
        reranker: Diversity/business rules reranker.
    """

    def __init__(
        self,
        n_features: int,
        recall_strategies: Optional[list[str]] = None,
    ) -> None:
        """Initialize the ranking pipeline.

        Args:
            n_features: Feature dimension.
            recall_strategies: Recall strategies to use.
        """
        self.recall_stage = RecallStage(strategies=recall_strategies)
        self.coarse_ranker = CoarseRankingStage(n_features, top_k=20)
        self.fine_ranker = FineRankingStage(n_features, top_k=10)
        self.reranker = RerankingStage()

    def run(
        self,
        user: np.ndarray,
        items: np.ndarray,
        verbose: bool = False,
    ) -> dict:
        """Run the full ranking pipeline.

        Args:
            user: User profile vector [n_features].
            items: All item features [n_items, n_features].
            verbose: Whether to print stage statistics.

        Returns:
            Dictionary with keys: 'recalled', 'coarse_ranked',
            'fine_ranked', 'reranked', 'stats'.
        """
        n_items = len(items)
        stats: dict[str, int] = {}

        # Stage 1: Recall
        recalled = self.recall_stage.recall(user, items)
        stats["recall_candidates"] = len(recalled)
        stats["recall_ratio"] = f"{len(recalled)}/{n_items}"

        if verbose:
            print(f"  Recall: {len(recalled)} candidates from {n_items} items")

        # Stage 2: Coarse ranking
        coarse_ranked = self.coarse_ranker.rank(user, recalled, items)
        stats["coarse_candidates"] = len(coarse_ranked)

        if verbose:
            print(f"  Coarse: {len(recalled)} → {len(coarse_ranked)} candidates")

        # Stage 3: Fine ranking
        fine_ranked = self.fine_ranker.rank(user, coarse_ranked, items)
        stats["fine_candidates"] = len(fine_ranked)

        if verbose:
            print(f"  Fine:   {len(coarse_ranked)} → {len(fine_ranked)} candidates")

        # Stage 4: Reranking
        reranked = self.reranker.rerank(fine_ranked, items)
        stats["final_candidates"] = len(reranked)

        if verbose:
            print(f"  Rerank: {len(fine_ranked)} → {len(reranked)} final items")

        return {
            "recalled": recalled,
            "coarse_ranked": coarse_ranked,
            "fine_ranked": fine_ranked,
            "reranked": reranked,
            "stats": stats,
        }


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing ranking_pipeline.py — Multi-stage Ranking")
    print("=" * 60)

    np.random.seed(42)

    # Create synthetic item pool
    n_items = 100
    n_features = 8
    items = _generate_items(n_items, n_features, seed=42)

    # Create a user profile
    user = _generate_user(n_features, seed=123)

    print(f"\nItem pool: {n_items} items, {n_features} features")

    all_pass = True

    # Test 1: Recall stage
    print("\n--- Recall Stage ---")
    recall = RecallStage(
        strategies=["random", "popularity", "embedding"],
        candidates_per_strategy=10,
    )
    recalled = recall.recall(user, items)
    print(f"  Recalled: {len(recalled)} items (≤ 30 expected)")
    recall_ok = 10 < len(recalled) <= 30
    all_pass = all_pass and recall_ok

    # Test 2: Coarse ranking
    print("\n--- Coarse Ranking ---")
    coarse = CoarseRankingStage(n_features, top_k=15)
    coarse_ranked = coarse.rank(user, recalled, items)
    print(f"  Coarse output: {len(coarse_ranked)} items (expected 15)")
    coarse_ok = len(coarse_ranked) == 15
    all_pass = all_pass and coarse_ok

    # Verify coarse is subset of recalled
    subset_ok = set(coarse_ranked).issubset(set(recalled))
    print(f"  Coarse ⊆ Recalled: {subset_ok}")
    all_pass = all_pass and subset_ok

    # Test 3: Fine ranking
    print("\n--- Fine Ranking ---")
    fine = FineRankingStage(n_features, hidden_dim=16, top_k=8)
    fine_ranked = fine.rank(user, coarse_ranked, items)
    print(f"  Fine output: {len(fine_ranked)} items (expected 8)")
    fine_ok = len(fine_ranked) == 8
    all_pass = all_pass and fine_ok

    # Test 4: Reranking
    print("\n--- Reranking ---")
    reranker = RerankingStage(diversity_factor=0.5)
    reranked = reranker.rerank(fine_ranked, items)
    print(f"  Reranked: {len(reranked)} items (same count, reordered)")
    rerank_ok = len(reranked) == len(fine_ranked) and set(reranked) == set(fine_ranked)
    all_pass = all_pass and rerank_ok

    # Test 5: Full pipeline
    print("\n--- Full Pipeline ---")
    pipeline = RankingPipeline(
        n_features=n_features,
        recall_strategies=["random", "popularity", "embedding"],
    )
    result = pipeline.run(user, items, verbose=True)
    stats = result["stats"]
    print(f"  Pipeline stats: {stats}")

    # Verify decreasing candidate counts
    final_len = len(result["reranked"])
    fine_len = len(result["fine_ranked"])
    coarse_len = len(result["coarse_ranked"])
    recall_len = len(result["recalled"])

    decreasing = recall_len >= coarse_len >= fine_len >= final_len
    print(f"  Decreasing candidate counts: {decreasing}")
    print(f"  ({recall_len} → {coarse_len} → {fine_len} → {final_len})")
    all_pass = all_pass and decreasing

    # Test with different users
    user2 = _generate_user(n_features, seed=999)
    result2 = pipeline.run(user2, items)
    different_ranking = not np.array_equal(result["reranked"], result2["reranked"])
    print(f"  Different users get different rankings: {different_ranking}")
    # Not strictly required, but good sanity check

    print(f"\n{'PASS' if all_pass else 'FAIL'}: ranking_pipeline.py")
