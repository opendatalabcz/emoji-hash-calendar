import re
from nltk.stem import PorterStemmer
from app.utilities.emoji_transformers.emoji_transformer import EmojiTransformer

class DictionaryTransformer(EmojiTransformer):
    def __init__(self, dictionary: dict):
        self.stemmer = PorterStemmer()

        self.dictionary = {}
        for k, v in dictionary.items():
            k_lower = k.lower()
            k_stem = " ".join(self.stemmer.stem(w) for w in k_lower.split())
            self.dictionary[k_lower] = v
            if k_stem != k_lower:
                self.dictionary[k_stem] = v

    @staticmethod
    def _generate_ngrams(words: list[str], n: int) -> list[str]:
        return [" ".join(words[i:i + n]) for i in range(len(words) - n + 1)]

    def transform(self, text: str) -> list[str]:
        text = text.lower().replace("'", "")
        words = re.findall(r"[^\W\d_]+", text, flags=re.UNICODE)

        emojis = []
        used_indices = set()

        for n in [3, 2, 1]:
            for i, phrase in enumerate(self._generate_ngrams(words, n)):
                if any(idx in used_indices for idx in range(i, i + n)):
                    continue
                stemmed_phrase = " ".join(self.stemmer.stem(w) for w in phrase.split())
                emoji = self.dictionary.get(phrase) or self.dictionary.get(stemmed_phrase)
                if not emoji:
                    continue
                if emoji not in emojis:
                    emojis.append(emoji)
                used_indices.update(range(i, i + n))
        return emojis

