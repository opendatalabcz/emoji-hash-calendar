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

    #def transform(self, text: str) -> str:
    #    text_embedding = self.model.encode(text, convert_to_tensor=True)

    #    scores = util.cos_sim(text_embedding, self.embeddings)[0]
    #    best_idx = int(scores.argmax())

    #    if float(scores[best_idx]) < 0.4:
    #        return "❓"

    #    best_key = self.phrases[best_idx]
    #    return self.emoji_dict[best_key]

    def transform(self, text: str) -> str:
        text_embedding = self.model.encode(text, convert_to_tensor=True)

        scores = util.cos_sim(text_embedding, self.embeddings)[0]

        threshold = 0.4
        selected = []

        for idx, score in enumerate(scores):
            if float(score) >= threshold:
                selected.append((idx, float(score)))

        if not selected:
            return "❓"

        # Seřadit podle relevance (nejvyšší score první)
        selected.sort(key=lambda x: x[1], reverse=True)

        # vezmi max třeba 3 emoji (aby to nebyl chaos)
        top_k = selected[:3]

        emojis = [self.emoji_dict[self.phrases[idx]] for idx, _ in top_k]

        return " ".join(emojis)