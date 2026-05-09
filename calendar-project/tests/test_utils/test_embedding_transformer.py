import torch
from app.emoji_transformers.embedding_transformer import EmbeddingTransformer


class DummyModel:
    """
    Fake SentenceTransformer model that returns deterministic embeddings.
    Each phrase gets a unique vector so we can control similarity.
    """
    def __init__(self, vectors):
        self.vectors = vectors

    def encode(self, items, convert_to_tensor=True, normalize_embeddings=True):
        if isinstance(items, str):
            return self.vectors[items]
        return torch.stack([self.vectors[i] for i in items])


def test_embedding_transformer_basic_ranking():
    vectors = {
        "cat": torch.tensor([1.0, 0.0]),
        "dog": torch.tensor([0.9, 0.1]),
        "pet": torch.tensor([0.8, 0.2]),
        "text": torch.tensor([1.0, 0.0]),  # identical to "cat"
    }

    model = DummyModel(vectors)

    transformer = EmbeddingTransformer(
        emoji_dict={"cat": "🐱", "dog": "🐶", "pet": "🐾"},
        model=model,
        threshold=0.5
    )

    result = transformer.transform("text")
    assert result == ["🐱", "🐶", "🐾"]


def test_embedding_transformer_threshold_cutoff():
    vectors = {
        "pizza": torch.tensor([1.0, 0.0]),   # highest similarity
        "food": torch.tensor([0.9, 0.1]),    # second highest
        "salad": torch.tensor([0.1, 0.9]),   # low similarity → should be filtered
        "text": torch.tensor([1.0, 0.0]),
    }

    model = DummyModel(vectors)

    transformer = EmbeddingTransformer(
        emoji_dict={
            "pizza": "🍕",
            "food": "🍽️",
            "salad": "🥗"
        },
        model=model,
        threshold=0.8
    )

    result = transformer.transform("text")
    assert result == ["🍕", "🍽️"]


def test_embedding_transformer_max_three_results():
    vectors = {
        "a": torch.tensor([1.0, 0.0]),
        "b": torch.tensor([0.9, 0.1]),
        "c": torch.tensor([0.8, 0.2]),
        "d": torch.tensor([0.7, 0.3]),
        "text": torch.tensor([1.0, 0.0]),
    }

    model = DummyModel(vectors)

    transformer = EmbeddingTransformer(
        emoji_dict={"a": "🅰️", "b": "🅱️", "c": "🇨", "d": "🇩"},
        model=model
    )

    result = transformer.transform("text")

    # Only top 3 allowed
    assert result == ["🅰️", "🅱️", "🇨"]


def test_embedding_transformer_deduplicates_emojis():
    vectors = {
        "hello": torch.tensor([1.0, 0.0]),
        "hi": torch.tensor([1.0, 0.0]),
        "text": torch.tensor([1.0, 0.0]),
    }

    model = DummyModel(vectors)

    transformer = EmbeddingTransformer(
        emoji_dict={"hello": "👋", "hi": "👋"},
        model=model
    )

    result = transformer.transform("text")
    assert result == ["👋"]
