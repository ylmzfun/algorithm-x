"""
Bayes Theorem and Applications for ML/AI Foundations.

Implements:
- Bayes theorem computation
- Medical test problem (classic Bayesian inference)
- Naive Bayes spam filter simulation
- Monty Hall problem simulation
"""

import numpy as np
from numpy.typing import NDArray
from typing import Tuple, List, Dict


# ============================================================
# Bayes Theorem
# ============================================================

def bayes_theorem(
    p_a_given_b: float, p_b: float, p_a: float
) -> float:
    """Compute P(B | A) using Bayes theorem.

    P(B | A) = P(A | B) * P(B) / P(A)

    Terms:
    - P(A | B): likelihood
    - P(B): prior probability
    - P(A): marginal probability (evidence / normalizing constant)
    - P(B | A): posterior probability

    Args:
        p_a_given_b: Likelihood P(A | B).
        p_b: Prior P(B).
        p_a: Marginal probability P(A).

    Returns:
        Posterior probability P(B | A).

    Raises:
        ValueError: If any probability is not in [0, 1] or P(A) = 0.

    Complexity: O(1).
    """
    if not (0 <= p_a_given_b <= 1 and 0 <= p_b <= 1 and 0 <= p_a <= 1):
        raise ValueError("Probabilities must be in [0, 1]")
    if p_a == 0:
        raise ValueError("P(A) cannot be zero (division by zero)")
    return p_a_given_b * p_b / p_a


def bayes_theorem_with_law_of_total_prob(
    p_a_given_b: float,
    p_b: float,
    p_a_given_not_b: float
) -> float:
    """Compute P(B | A) when only P(A | B) and P(A | ¬B) are known.

    Uses the law of total probability:
        P(A) = P(A|B) * P(B) + P(A|¬B) * P(¬B)

    Then applies Bayes theorem:
        P(B | A) = P(A | B) * P(B) / P(A)

    Args:
        p_a_given_b: P(A | B), the likelihood.
        p_b: Prior P(B).
        p_a_given_not_b: P(A | ¬B), the false positive / alternate likelihood.

    Returns:
        Posterior P(B | A).

    Complexity: O(1).
    """
    p_not_b = 1.0 - p_b
    p_a = p_a_given_b * p_b + p_a_given_not_b * p_not_b
    return bayes_theorem(p_a_given_b, p_b, p_a)


# ============================================================
# Medical Test Problem
# ============================================================

def medical_test_problem(
    prevalence: float = 0.01,
    sensitivity: float = 0.99,
    specificity: float = 0.99
) -> Dict[str, float]:
    """Solve the classic medical test Bayesian inference problem.

    Given:
    - Prevalence: P(D) — probability of having the disease.
    - Sensitivity: P(+ | D) — probability of testing positive given disease.
    - Specificity: P(- | ¬D) — probability of testing negative given no disease.

    Question: What is P(D | +), the probability of having the disease
              given a positive test result?

    Intuition: When the disease is rare (low prevalence), even a highly
    accurate test can yield mostly false positives, because the number
    of healthy people greatly exceeds the number of sick people.

    Args:
        prevalence: P(D), default 1% (0.01).
        sensitivity: P(+|D), default 99% (0.99).
        specificity: P(-|¬D), default 99% (0.99).

    Returns:
        Dictionary with keys:
            - 'prevalence': P(D)
            - 'sensitivity': P(+|D)
            - 'specificity': P(-|¬D)
            - 'false_positive_rate': P(+|¬D) = 1 - specificity
            - 'p_positive': P(+), probability of any positive test
            - 'posterior': P(D | +), probability of disease given positive test
            - 'explanation': human-readable explanation
    """
    false_positive_rate = 1.0 - specificity
    p_not_d = 1.0 - prevalence

    # P(+) = P(+|D)*P(D) + P(+|¬D)*P(¬D)
    p_positive = sensitivity * prevalence + false_positive_rate * p_not_d

    # P(D | +) = P(+|D) * P(D) / P(+)
    posterior = sensitivity * prevalence / p_positive

    # Explanation
    n = 10000  # hypothetical population
    n_sick = int(n * prevalence)
    n_healthy = n - n_sick
    true_positives = int(n_sick * sensitivity)
    false_positives = int(n_healthy * false_positive_rate)

    return {
        'prevalence': prevalence,
        'sensitivity': sensitivity,
        'specificity': specificity,
        'false_positive_rate': false_positive_rate,
        'p_positive': p_positive,
        'posterior': posterior,
        'explanation': (
            f"In a population of {n}: {n_sick} have the disease, {n_healthy} do not.\n"
            f"True positives (sick + test positive): {true_positives}\n"
            f"False positives (healthy + test positive): {false_positives}\n"
            f"Total positive tests: {true_positives + false_positives}\n"
            f"P(disease | positive test) = {posterior:.4f} = {posterior*100:.2f}%\n"
            f"This shows how low prevalence makes even a 99% accurate test "
            f"give mostly false positives."
        )
    }


# ============================================================
# Naive Bayes Spam Filter
# ============================================================

class NaiveBayesSpamFilter:
    """Simple Naive Bayes classifier for spam detection.

    Uses Bayes theorem with the "naive" assumption of conditional
    independence between features (words).

    P(spam | words) ∝ P(spam) * Πᵢ P(word_i | spam)

    Works with binary word features (word present/absent).
    Uses Laplace (add-1) smoothing to handle unseen words.
    """

    def __init__(self, alpha: float = 1.0):
        """
        Args:
            alpha: Laplace smoothing parameter (default 1.0 = add-1).
        """
        self.alpha = alpha
        self.p_spam: float = 0.5
        self.p_ham: float = 0.5
        self.word_probs_spam: Dict[str, float] = {}
        self.word_probs_ham: Dict[str, float] = {}
        self.vocabulary: set = set()
        self._trained = False

    def _extract_words(self, text: str) -> set:
        """Extract unique words from text (simple tokenization)."""
        return set(text.lower().split())

    def fit(self, texts: List[str], labels: List[int]) -> None:
        """Train the Naive Bayes classifier.

        Args:
            texts: List of text messages.
            labels: List of labels (1 = spam, 0 = ham/not-spam).
        """
        n = len(texts)
        if n == 0:
            raise ValueError("Empty training data")

        n_spam = sum(labels)
        n_ham = n - n_spam

        self.p_spam = n_spam / n
        self.p_ham = n_ham / n

        # Collect vocabulary and word counts
        spam_word_counts: Dict[str, int] = {}
        ham_word_counts: Dict[str, int] = {}

        for text, label in zip(texts, labels):
            words = self._extract_words(text)
            self.vocabulary.update(words)
            for w in words:
                if label == 1:
                    spam_word_counts[w] = spam_word_counts.get(w, 0) + 1
                else:
                    ham_word_counts[w] = ham_word_counts.get(w, 0) + 1

        vocab_size = len(self.vocabulary)

        # Compute P(word | spam) and P(word | ham) with Laplace smoothing
        for w in self.vocabulary:
            self.word_probs_spam[w] = (
                (spam_word_counts.get(w, 0) + self.alpha) /
                (n_spam + self.alpha * 2)  # binary features, so 2 classes of word presence
            )
            self.word_probs_ham[w] = (
                (ham_word_counts.get(w, 0) + self.alpha) /
                (n_ham + self.alpha * 2)
            )

        self._trained = True

    def predict_proba(self, text: str) -> Tuple[float, float]:
        """Compute P(spam | text) and P(ham | text).

        Uses log probabilities for numerical stability.

        Args:
            text: Input text message.

        Returns:
            Tuple (p_spam_given_text, p_ham_given_text).
        """
        if not self._trained:
            raise RuntimeError("Model not trained; call fit() first")

        words = self._extract_words(text)

        # Log probabilities to avoid underflow
        log_p_spam = np.log(self.p_spam) if self.p_spam > 0 else -np.inf
        log_p_ham = np.log(self.p_ham) if self.p_ham > 0 else -np.inf

        for w in words:
            if w in self.vocabulary:
                log_p_spam += np.log(self.word_probs_spam[w])
                log_p_ham += np.log(self.word_probs_ham[w])
            # Words not in vocabulary: ignore (contribute factor ~1)
            # Could use a prior for OOV words

        # Convert from log space
        # p(spam|words) = exp(log_p_spam) / (exp(log_p_spam) + exp(log_p_ham))
        max_log = max(log_p_spam, log_p_ham)
        p_spam = np.exp(log_p_spam - max_log)
        p_ham = np.exp(log_p_ham - max_log)
        total = p_spam + p_ham

        return p_spam / total, p_ham / total

    def predict(self, text: str) -> int:
        """Classify text as spam (1) or ham (0).

        Args:
            text: Input text message.

        Returns:
            1 for spam, 0 for ham.
        """
        p_spam, p_ham = self.predict_proba(text)
        return 1 if p_spam > p_ham else 0


# ============================================================
# Monty Hall Problem
# ============================================================

def monty_hall_simulation(n_trials: int = 10000) -> Dict[str, float]:
    """Simulate the Monty Hall problem to demonstrate conditional probability.

    Problem setup:
    - 3 doors: behind one is a car (prize), behind the other two are goats.
    - Player picks a door.
    - Host (Monty) opens a different door, always revealing a goat.
    - Player can either stay with original choice or switch to the other
      unopened door.

    The counterintuitive result: switching wins with probability 2/3,
    while staying wins with probability 1/3.

    Args:
        n_trials: Number of simulation trials.

    Returns:
        Dictionary with keys:
            - 'stay_wins': Proportion of wins when staying.
            - 'switch_wins': Proportion of wins when switching.
            - 'explanation': Why switching is better.
    """
    np.random.seed(42)

    stay_wins = 0
    switch_wins = 0

    for _ in range(n_trials):
        # Randomly place the car (0, 1, or 2)
        car_door = np.random.randint(0, 3)
        # Player's initial choice
        player_choice = np.random.randint(0, 3)

        # Host opens a door that:
        # 1. Is not the player's choice
        # 2. Does NOT have the car
        remaining = [d for d in range(3)
                     if d != player_choice and d != car_door]
        host_opens = remaining[np.random.randint(0, len(remaining))]

        # The door the player would switch to (the other unopened door)
        switch_choice = [d for d in range(3)
                         if d != player_choice and d != host_opens][0]

        # Record results
        if player_choice == car_door:
            stay_wins += 1
        if switch_choice == car_door:
            switch_wins += 1

    return {
        'stay_wins': stay_wins / n_trials,
        'switch_wins': switch_wins / n_trials,
        'explanation': (
            "Initial probability of picking the car: 1/3.\n"
            "Probability the car is behind one of the other two doors: 2/3.\n"
            "When Monty opens a goat door, he effectively transfers the 2/3 "
            "probability to the remaining unopened door.\n"
            "Thus: P(win | switch) = 2/3, P(win | stay) = 1/3."
        )
    }


# ============================================================
# Tests
# ============================================================

def _test_bayes_theorem() -> None:
    # Classic example: P(A) = 0.3 (raining), P(B) = 0.5 (cloudy),
    # P(cloudy | raining) = 0.8
    # Bayes: P(raining | cloudy) = 0.8 * 0.3 / 0.5 = 0.48
    result = bayes_theorem(p_a_given_b=0.8, p_b=0.3, p_a=0.5)
    assert abs(result - 0.48) < 1e-10, f"FAIL: {result}"

    # With law of total probability
    result2 = bayes_theorem_with_law_of_total_prob(
        p_a_given_b=0.8, p_b=0.3, p_a_given_not_b=0.3714
    )
    assert abs(result2 - 0.48) < 0.01, f"FAIL: {result2}"
    print("  PASS: bayes_theorem")


def _test_medical_test() -> None:
    result = medical_test_problem(prevalence=0.01, sensitivity=0.99, specificity=0.99)
    posterior = result['posterior']
    # P(D|+) should be ≈ 0.5 (with these numbers)
    assert 0.45 < posterior < 0.55, f"FAIL: posterior={posterior}"
    print(f"  PASS: medical_test (P(D|+)={posterior:.4f})")


def _test_naive_bayes() -> None:
    # Simple training data
    texts = [
        "buy now limited offer",       # spam
        "click here win prize",        # spam
        "hello how are you",           # ham
        "meeting at noon tomorrow",    # ham
        "free money guaranteed",       # spam
        "project deadline updated",    # ham
    ]
    labels = [1, 1, 0, 0, 1, 0]

    nb = NaiveBayesSpamFilter(alpha=1.0)
    nb.fit(texts, labels)

    # Test on seen-like data
    test_spam = "free offer now"
    p_spam, p_ham = nb.predict_proba(test_spam)
    assert p_spam > p_ham, f"FAIL: spam classified as ham ({p_spam:.3f} > {p_ham:.3f})"
    assert nb.predict(test_spam) == 1

    test_ham = "hello meeting tomorrow"
    p_spam2, p_ham2 = nb.predict_proba(test_ham)
    assert p_ham2 > p_spam2, f"FAIL: ham classified as spam ({p_ham2:.3f} > {p_spam2:.3f})"
    assert nb.predict(test_ham) == 0

    print("  PASS: naive_bayes_spam_filter")


def _test_monty_hall() -> None:
    result = monty_hall_simulation(n_trials=50000)
    stay = result['stay_wins']
    switch = result['switch_wins']
    # Stay should be ~1/3, switch ~2/3
    assert 0.30 < stay < 0.36, f"FAIL stay: {stay}"
    assert 0.64 < switch < 0.70, f"FAIL switch: {switch}"
    print(f"  PASS: monty_hall (stay={stay:.4f}, switch={switch:.4f})")


if __name__ == "__main__":
    print("Testing bayes_theorem.py ...")
    _test_bayes_theorem()
    _test_medical_test()
    _test_naive_bayes()
    _test_monty_hall()
    print("All Bayes theorem tests PASSED!")
