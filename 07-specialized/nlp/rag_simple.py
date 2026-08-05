"""Simple RAG (Retrieval-Augmented Generation) demo from scratch.

Implements:
- TF-IDF document retriever
- Query-based document retrieval
- Prompt construction with retrieved context
- Mock LLM response generation

Reference: Lewis et al., "Retrieval-Augmented Generation for
Knowledge-Intensive NLP Tasks" (2020).
"""

from __future__ import annotations

import numpy as np
from collections import Counter
from typing import Optional


# ---------------------------------------------------------------------------
# TF-IDF Retriever
# ---------------------------------------------------------------------------

class TFIDFRetriever:
    """TF-IDF based document retriever.

    Computes TF-IDF vectors for a corpus of documents and retrieves
    the top-k most relevant documents for a given query.

    Attributes:
        documents: List of document strings.
        vocab: Set of unique terms in the corpus.
        word2idx: Mapping from term to index.
        idf: Inverse document frequency for each term.
        doc_vectors: TF-IDF vectors for each document [num_docs, vocab_size].
    """

    def __init__(self) -> None:
        """Initialize an empty TF-IDF retriever."""
        self.documents: list[str] = []
        self.vocab: set[str] = set()
        self.word2idx: dict[str, int] = {}
        self.idf: np.ndarray = np.array([])
        self.doc_vectors: np.ndarray = np.array([])

    def _tokenize(self, text: str) -> list[str]:
        """Simple whitespace lowercased tokenization.

        Args:
            text: Input text string.

        Returns:
            List of lowercased tokens.
        """
        return text.lower().split()

    def fit(self, documents: list[str]) -> None:
        """Build the TF-IDF index from a document corpus.

        Args:
            documents: List of document strings to index.
        """
        self.documents = documents
        num_docs = len(documents)

        # Build vocabulary
        all_tokens: list[list[str]] = []
        for doc in documents:
            tokens = self._tokenize(doc)
            all_tokens.append(tokens)
            self.vocab.update(tokens)

        self.word2idx = {w: i for i, w in enumerate(sorted(self.vocab))}
        vocab_size = len(self.vocab)

        # Compute IDF
        df = np.zeros(vocab_size)
        for tokens in all_tokens:
            unique_tokens = set(tokens)
            for tok in unique_tokens:
                if tok in self.word2idx:
                    df[self.word2idx[tok]] += 1

        self.idf = np.log((num_docs + 1) / (df + 1)) + 1.0  # smooth IDF

        # Compute TF-IDF vectors
        self.doc_vectors = np.zeros((num_docs, vocab_size))
        for i, tokens in enumerate(all_tokens):
            tf = Counter(tokens)
            for tok, count in tf.items():
                if tok in self.word2idx:
                    j = self.word2idx[tok]
                    self.doc_vectors[i, j] = count * self.idf[j]

            # L2 normalize
            norm = np.linalg.norm(self.doc_vectors[i]) + 1e-12
            self.doc_vectors[i] /= norm

    def _query_vector(self, query: str) -> np.ndarray:
        """Convert a query string to a TF-IDF vector.

        Args:
            query: Query string.

        Returns:
            TF-IDF query vector [vocab_size], L2 normalized.
        """
        tokens = self._tokenize(query)
        vec = np.zeros(len(self.vocab))
        tf = Counter(tokens)
        for tok, count in tf.items():
            if tok in self.word2idx:
                j = self.word2idx[tok]
                # For query, use IDF from corpus and raw TF
                vec[j] = count * self.idf[j]
        norm = np.linalg.norm(vec) + 1e-12
        return vec / norm

    def retrieve(
        self, query: str, top_k: int = 3
    ) -> list[tuple[int, str, float]]:
        """Retrieve the top-k most relevant documents for a query.

        Args:
            query: Query string.
            top_k: Number of documents to retrieve.

        Returns:
            List of (doc_index, document_text, cosine_similarity) tuples,
            sorted by similarity descending.
        """
        q_vec = self._query_vector(query)
        sims = self.doc_vectors @ q_vec  # [num_docs]
        top_indices = np.argsort(sims)[::-1][:top_k]
        return [
            (int(i), self.documents[i], float(sims[i]))
            for i in top_indices
        ]


# ---------------------------------------------------------------------------
# Simple RAG
# ---------------------------------------------------------------------------

class SimpleRAG:
    """Simple Retrieval-Augmented Generation system.

    Combines a TF-IDF retriever with a mock LLM. The retriever finds
    relevant documents for a query, and the mock LLM generates a response
    using the retrieved context.

    Attributes:
        retriever: The TF-IDF document retriever.
        top_k: Number of documents to retrieve per query.
    """

    def __init__(self, retriever: TFIDFRetriever, top_k: int = 3) -> None:
        """Initialize the RAG system.

        Args:
            retriever: A fitted TFIDFRetriever.
            top_k: Default number of documents to retrieve.
        """
        self.retriever = retriever
        self.top_k = top_k

    def build_prompt(
        self, query: str, retrieved_docs: list[tuple[int, str, float]]
    ) -> str:
        """Construct a prompt with retrieved context.

        Args:
            query: User query.
            retrieved_docs: Retrieved (idx, text, score) tuples.

        Returns:
            Formatted prompt string with context and query.
        """
        context = "\n".join(
            f"  [{i+1}] {doc}" for i, (_, doc, _) in enumerate(retrieved_docs)
        )
        prompt = (
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            f"Answer (based on the context above):"
        )
        return prompt

    def generate(self, query: str, top_k: Optional[int] = None) -> dict:
        """Run the full RAG pipeline: retrieve → build prompt → generate.

        Args:
            query: User query.
            top_k: Override the default number of retrieved documents.

        Returns:
            Dictionary with keys: 'query', 'retrieved_docs', 'prompt',
            'response'.
        """
        k = top_k if top_k is not None else self.top_k
        retrieved = self.retriever.retrieve(query, top_k=k)
        prompt = self.build_prompt(query, retrieved)
        response = self._mock_llm(query, retrieved)
        return {
            "query": query,
            "retrieved_docs": retrieved,
            "prompt": prompt,
            "response": response,
        }

    def _mock_llm(
        self,
        query: str,
        retrieved_docs: list[tuple[int, str, float]],
    ) -> str:
        """Mock LLM that constructs a response from retrieved context.

        In a real system, this would call an actual LLM. Here we simulate
        by extracting key phrases from the retrieved documents.

        Args:
            query: User query.
            retrieved_docs: Retrieved documents with scores.

        Returns:
            Generated response string.
        """
        if not retrieved_docs:
            return "I don't have enough information to answer that question."

        # Extract key terms from the query
        query_terms = set(query.lower().split())

        # Build response from retrieved context
        facts: list[str] = []
        for _, doc, score in retrieved_docs:
            if score > 0.0:
                # Extract the sentence most relevant to the query
                doc_terms = set(doc.lower().split())
                overlap = query_terms & doc_terms
                if overlap:
                    facts.append(doc)

        if facts:
            response = "Based on the retrieved information: " + "; ".join(facts)
        else:
            response = (
                f"Based on the context, I found relevant information "
                f"but cannot form a precise answer."
            )

        return response


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Testing rag_simple.py — Simple RAG Demo")
    print("=" * 60)

    # Build a small knowledge base
    documents = [
        "The cat is a small domesticated carnivorous mammal.",
        "Dogs are domesticated mammals and are known as man's best friend.",
        "Paris is the capital and most populous city of France.",
        "Tokyo is the capital of Japan and one of the most populous cities.",
        "The Earth orbits the Sun at an average distance of 93 million miles.",
        "The Moon is Earth's only natural satellite and orbits our planet.",
        "Water freezes at 0 degrees Celsius and boils at 100 degrees Celsius.",
        "The Amazon rainforest is the largest tropical rainforest on Earth.",
        "Python is a high-level programming language known for its readability.",
        "Machine learning is a subset of artificial intelligence.",
        "The Great Wall of China is one of the most famous landmarks.",
        "Shakespeare wrote many famous plays including Hamlet and Romeo and Juliet.",
        "Photosynthesis converts sunlight into chemical energy in plants.",
        "The human body has 206 bones and over 600 muscles.",
        "Albert Einstein developed the theory of relativity.",
    ]

    print(f"\nKnowledge base: {len(documents)} documents")

    # Build retriever
    retriever = TFIDFRetriever()
    retriever.fit(documents)
    print(f"Vocabulary size: {len(retriever.vocab)}")

    # Create RAG system
    rag = SimpleRAG(retriever, top_k=3)

    # Test queries
    test_queries = [
        ("What is the capital of France?", "Paris"),
        ("Tell me about dogs", "man's best friend"),
        ("What temperature does water boil at?", "100 degrees"),
        ("Who developed relativity?", "Einstein"),
        ("Tell me about programming languages", "Python"),
    ]

    all_pass = True
    for query, expected_term in test_queries:
        result = rag.generate(query)
        retrieved = result["retrieved_docs"]
        response = result["response"]
        has_expected = expected_term.lower() in response.lower()
        has_context = len(retrieved) > 0

        print(f"\n  Query: '{query}'")
        print(f"  Retrieved: {len(retrieved)} docs")
        if retrieved:
            print(f"  Top doc: '{retrieved[0][1][:60]}...' "
                  f"(score={retrieved[0][2]:.3f})")
        print(f"  Response contains '{expected_term}': {has_expected}")

        if not has_expected or not has_context:
            all_pass = False

    # Test retrieval quality
    query = "famous landmarks in China"
    results = retriever.retrieve(query, top_k=3)
    great_wall_in_results = any(
        "Great Wall" in doc for _, doc, _ in results
    )
    print(f"\n  Query: '{query}'")
    print(f"  Great Wall in top-3 results: {great_wall_in_results}")
    if not great_wall_in_results:
        all_pass = False

    # Test prompt construction
    result = rag.generate("What is the Moon?")
    prompt = result["prompt"]
    prompt_ok = "Context:" in prompt and "Question:" in prompt
    print(f"\n  Prompt contains expected sections: {prompt_ok}")
    all_pass = all_pass and prompt_ok

    print(f"\n{'PASS' if all_pass else 'FAIL'}: rag_simple.py")
