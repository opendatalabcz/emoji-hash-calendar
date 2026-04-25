from sentence_transformers import SentenceTransformer, util
from transformers_class.emoji_transformer import EmojiTransformer
from torch.nn.functional import normalize

class EmbeddingTransformer(EmojiTransformer):
    def __init__(self, emoji_dict: dict, model: str):
        self.model = SentenceTransformer(model)

        self.emoji_dict = emoji_dict

        self.phrases = list(self.emoji_dict.keys())
        self.embeddings = self.model.encode(
            self.phrases, convert_to_tensor=True
        )

    def transform(self, text: str) -> str:
        text_embedding = self.model.encode(text, convert_to_tensor=True)

        scores = util.cos_sim(text_embedding, self.embeddings)[0]
        """
        threshold = 0.4
        selected = []

        for idx, score in enumerate(scores):
            if float(score) >= threshold:
                selected.append((idx, float(score)))

        if not selected:
            return "❓"

        selected.sort(key=lambda x: x[1], reverse=True)
        top_k = selected[:5]

        emojis = [self.emoji_dict[self.phrases[idx]] for idx, _ in top_k]
        """

        top_k = 3
        top_indices = scores.topk(k=top_k).indices

        emojis = [
            self.emoji_dict[self.phrases[idx]]
            for idx in top_indices
        ]

        return " ".join(emojis)
