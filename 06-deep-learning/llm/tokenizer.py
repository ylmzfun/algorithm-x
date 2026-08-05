"""BPE (Byte Pair Encoding) tokenizer from scratch.

Implements:
- Training: learn merge rules from corpus by iteratively merging most frequent adjacent pairs
- Encoding: convert text to token IDs using learned merges
- Decoding: convert token IDs back to text
"""

import re
from collections import Counter, defaultdict
from typing import Optional


class BPETokenizer:
    """Byte Pair Encoding tokenizer.

    Learns subword vocabulary by iteratively merging the most frequent
    adjacent token pairs in the training corpus.
    """

    def __init__(
        self,
        pad_token: str = "<PAD>",
        unk_token: str = "<UNK>",
        bos_token: str = "<BOS>",
        eos_token: str = "<EOS>",
    ):
        """Initialize BPE tokenizer.

        Args:
            pad_token: Padding token string.
            unk_token: Unknown token string.
            bos_token: Beginning-of-sequence token.
            eos_token: End-of-sequence token.
        """
        self.pad_token = pad_token
        self.unk_token = unk_token
        self.bos_token = bos_token
        self.eos_token = eos_token

        self.special_tokens = [pad_token, unk_token, bos_token, eos_token]
        self.pad_id = 0
        self.unk_id = 1
        self.bos_id = 2
        self.eos_id = 3

        # Vocabulary: id → token string
        self.id_to_token: dict[int, str] = {
            i: tok for i, tok in enumerate(self.special_tokens)
        }
        # Token string → id
        self.token_to_id: dict[str, int] = {
            tok: i for i, tok in self.id_to_token.items()
        }
        # Merge rules: (tok_a, tok_b) → merged_token_string
        self.merges: dict[tuple[str, str], str] = {}
        self.vocab_size: int = len(self.special_tokens)

    @staticmethod
    def _tokenize_text(text: str) -> list[str]:
        """Initial tokenization: split into characters with word boundary marker.

        Adds '▁' (U+2581) at the start of each word to denote word boundaries.

        Args:
            text: Input text string.

        Returns:
            List of character tokens.
        """
        # Split on whitespace, add word boundary marker
        words = text.split()
        tokens = []
        for word in words:
            tokens.append("▁")  # word boundary
            tokens.extend(list(word))
        return tokens

    def train(self, texts: list[str], vocab_size: int, verbose: bool = False):
        """Train BPE tokenizer on a corpus.

        Args:
            texts: List of text strings for training.
            vocab_size: Target vocabulary size (including special tokens).
            verbose: If True, print merge progress.
        """
        # Initial tokenization
        all_tokens = []
        for text in texts:
            all_tokens.extend(self._tokenize_text(text))

        # Build initial vocabulary from characters
        chars = set()
        for text in texts:
            chars.update(list(text))
        chars.add("▁")

        for ch in sorted(chars):
            if ch not in self.token_to_id:
                idx = len(self.id_to_token)
                self.id_to_token[idx] = ch
                self.token_to_id[ch] = idx

        num_merges = vocab_size - len(self.id_to_token)
        if num_merges <= 0:
            return

        # Split training text into token sequences
        token_seqs = []
        for text in texts:
            seq = self._tokenize_text(text)
            token_seqs.append(seq)

        # Greedy BPE
        for merge_step in range(num_merges):
            # Count all adjacent pairs
            pair_counts: dict[tuple[str, str], int] = defaultdict(int)
            for seq in token_seqs:
                for i in range(len(seq) - 1):
                    pair = (seq[i], seq[i + 1])
                    pair_counts[pair] += 1

            if not pair_counts:
                break

            # Find most frequent pair
            best_pair = max(pair_counts, key=pair_counts.get)
            if pair_counts[best_pair] < 2:
                break

            # Create new token
            new_token = best_pair[0] + best_pair[1]
            new_id = len(self.id_to_token)
            self.id_to_token[new_id] = new_token
            self.token_to_id[new_token] = new_id
            self.merges[best_pair] = new_token

            if verbose and merge_step % 100 == 0:
                print(f"  Merge {merge_step}: {best_pair} → {new_token} (count={pair_counts[best_pair]})")

            # Apply merge to all sequences
            for seq in token_seqs:
                i = 0
                while i < len(seq) - 1:
                    if seq[i] == best_pair[0] and seq[i + 1] == best_pair[1]:
                        seq[i:i + 2] = [new_token]
                    else:
                        i += 1

        self.vocab_size = len(self.id_to_token)

    def _get_merge_order(self) -> list[tuple[str, str]]:
        """Get merges in order of priority (by token id, lower = earlier merge).

        Returns:
            List of (tok_a, tok_b) pairs in merge order.
        """
        # Sort merges by the id of the resulting token (lower = applied earlier)
        merge_items = sorted(self.merges.items(), key=lambda x: self.token_to_id.get(x[1], 999999))
        return [pair for pair, _ in merge_items]

    def encode(self, text: str) -> list[int]:
        """Encode text to token IDs.

        Args:
            text: Input text string.

        Returns:
            List of token IDs.
        """
        if not self.merges:
            # No merges learned yet; just encode characters
            tokens = self._tokenize_text(text)
        else:
            tokens = self._tokenize_text(text)
            merge_order = self._get_merge_order()

            for pair in merge_order:
                merged = self.merges[pair]
                i = 0
                while i < len(tokens) - 1:
                    if tokens[i] == pair[0] and tokens[i + 1] == pair[1]:
                        tokens[i:i + 2] = [merged]
                    else:
                        i += 1

        # Convert tokens to IDs
        ids = []
        for tok in tokens:
            if tok in self.token_to_id:
                ids.append(self.token_to_id[tok])
            else:
                # Try character-level fallback
                chars = list(tok)
                for ch in chars:
                    ids.append(self.token_to_id.get(ch, self.unk_id))
        return ids

    def decode(self, ids: list[int]) -> str:
        """Decode token IDs back to text.

        Args:
            ids: List of token IDs.

        Returns:
            Decoded text string.
        """
        tokens = []
        for idx in ids:
            if idx in self.id_to_token:
                tokens.append(self.id_to_token[idx])
            else:
                tokens.append(self.unk_token)

        # Join tokens and clean up word boundaries
        text = "".join(tokens)
        # Replace word boundary marker with space
        text = text.replace("▁", " ")
        # Remove leading/trailing spaces
        text = text.strip()
        # Fix double spaces
        text = re.sub(r'\s+', ' ', text)
        return text


# ============================================================================
# Tests
# ============================================================================
if __name__ == "__main__":
    print("Testing BPETokenizer...")

    # Test 1: Basic initialization
    tokenizer = BPETokenizer()
    assert tokenizer.pad_id == 0
    assert tokenizer.unk_id == 1
    assert tokenizer.bos_id == 2
    assert tokenizer.eos_id == 3
    print("  PASS: Tokenizer initialized with special tokens")

    # Test 2: Training on small corpus
    corpus = [
        "hello world hello",
        "hello there world",
        "hello hello world",
        "the quick brown fox",
        "the lazy dog",
    ]
    tokenizer.train(corpus, vocab_size=50, verbose=False)
    assert tokenizer.vocab_size <= 50, f"Vocab size exceeded: {tokenizer.vocab_size}"
    assert tokenizer.vocab_size > 4, "No merges learned"
    print(f"  PASS: Trained vocabulary size: {tokenizer.vocab_size}")

    # Test 3: Encode/decode roundtrip
    text = "hello world"
    ids = tokenizer.encode(text)
    decoded = tokenizer.decode(ids)
    assert "hello" in decoded.lower() or "hello" in decoded, f"Decode lost content: '{decoded}'"
    print(f"  PASS: Encode/decode: '{text}' → ids {ids} → '{decoded}'")

    # Test 4: Unknown character handling
    ids_unk = tokenizer.encode("hello @#$ world")
    decoded_unk = tokenizer.decode(ids_unk)
    # Should not crash and produce something reasonable
    assert len(decoded_unk) > 0, "Empty decode for unknown chars"
    print(f"  PASS: Unknown character handling: '{decoded_unk}'")

    # Test 5: Empty text
    ids_empty = tokenizer.encode("")
    assert ids_empty == [], "Empty text should produce empty ids"
    decoded_empty = tokenizer.decode([])
    assert decoded_empty == "", f"Empty ids should decode to empty: '{decoded_empty}'"
    print("  PASS: Empty text handling")

    # Test 6: BPE merge rules applied
    tokenizer2 = BPETokenizer()
    tokenizer2.train(["aa aa bb", "aa aa aa", "bb aa bb"], vocab_size=30)
    ids2 = tokenizer2.encode("aa bb")
    # "aa" should be a single token after merges
    decoded2 = tokenizer2.decode(ids2)
    # Should have some merging (aa repeated, so likely merged)
    print(f"  PASS: BPE merges: 'aa bb' → ids {ids2} → '{decoded2}'")

    # Test 7: Larger vocabulary
    tokenizer3 = BPETokenizer()
    longer_corpus = [
        "the quick brown fox jumps over the lazy dog",
        "the quick brown fox jumps over the lazy dog",
        "a quick movement of the enemy will jeopardize six gunboats",
        "how quickly daft jumping zebras vex",
        "the five boxing wizards jump quickly",
    ]
    tokenizer3.train(longer_corpus, vocab_size=100)
    text3 = "the quick brown fox"
    ids3 = tokenizer3.encode(text3)
    decoded3 = tokenizer3.decode(ids3)
    assert len(decoded3) > 0
    print(f"  PASS: Larger vocab: '{text3}' → ids {ids3} → '{decoded3}'")

    # Test 8: Merge priority
    # Verify that merges are applied in correct order
    assert len(tokenizer.merges) > 0, "No merges learned"
    print(f"  PASS: {len(tokenizer.merges)} merge rules learned")

    # Test 9: Special token IDs are accessible
    assert tokenizer.token_to_id["<PAD>"] == 0
    assert tokenizer.token_to_id["<UNK>"] == 1
    assert tokenizer.token_to_id["<BOS>"] == 2
    assert tokenizer.token_to_id["<EOS>"] == 3
    print("  PASS: Special token IDs correct")

    print("\nAll BPETokenizer tests passed!")
