from sentence_transformers import SentenceTransformer, util
from transformers_class.emoji_transformer import EmojiTransformer

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
        best_idx = int(scores.argmax())

        if float(scores[best_idx]) < 0.4:
            return "❓"

        best_key = self.phrases[best_idx]
        return self.emoji_dict[best_key]