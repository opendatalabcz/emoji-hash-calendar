from sentence_transformers import SentenceTransformer, util
from app.emoji_transformers.emoji_transformer import EmojiTransformer

class EmbeddingTransformer(EmojiTransformer):
    def __init__(self, emoji_dict: dict, model: SentenceTransformer, threshold: float = 0.6):
        self.model = model
        self.threshold = threshold
        self.emoji_dict = emoji_dict
        self.phrases = list(self.emoji_dict.keys())
        self.embeddings = self.model.encode(
            self.phrases,
            convert_to_tensor=True,
            normalize_embeddings=True
        )

    def transform(self, text: str) -> list[str]:
        text_embedding = self.model.encode(
            text,
            convert_to_tensor=True,
            normalize_embeddings=True
        )
        scores = util.cos_sim(text_embedding, self.embeddings)[0]
        ranked_indices = scores.argsort(descending=True)

        emojis = []
        seen = set()
        for idx in ranked_indices:
            score = scores[int(idx)].item()
            emoji = self.emoji_dict[self.phrases[int(idx)]]
            if emoji in seen:
                continue
            # always take the first one regardless of score
            if len(emojis) >= 2 and score < self.threshold:
                break
            emojis.append(emoji)
            seen.add(emoji)
            if len(emojis) == 3:
                break
        return emojis