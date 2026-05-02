import re
from nltk.stem import PorterStemmer
from transformers_class.emoji_transformer import EmojiTransformer

class DictionaryTransformer(EmojiTransformer):
    def __init__(self, dictionary: dict):
        self.stemmer = PorterStemmer()

        self.dictionary = {}
        for k, v in dictionary.items():
            k_lower = k.lower()
            k_stem = " ".join(self.stemmer.stem(w) for w in k_lower.split())

            self.dictionary[k_lower] = v
            self.dictionary[k_stem] = v

    def transform(self, text: str) -> list[str]:
        text = text.lower().replace("'", "")
        words = re.findall(r"[^\W\d_]+", text.lower(), flags=re.UNICODE)

        def generate_ngrams(words, n):
            return [" ".join(words[i:i+n]) for i in range(len(words)-n+1)]

        emojis = []
        used_indices = set()

        for n in [3, 2, 1]:
            ngrams = generate_ngrams(words, n)

            for i, phrase in enumerate(ngrams):
                if any(idx in used_indices for idx in range(i, i+n)):
                    continue

                stemmed_phrase = " ".join(self.stemmer.stem(w) for w in phrase.split())

                if phrase in self.dictionary:
                    emoji = self.dictionary[phrase]
                elif stemmed_phrase in self.dictionary:
                    emoji = self.dictionary[stemmed_phrase]
                else:
                    continue

                if emoji not in emojis:
                    emojis.append(emoji)

                used_indices.update(range(i, i+n))

        return emojis