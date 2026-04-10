import re
from transformers_class.emoji_transformer import EmojiTransformer

class DictionaryTransformer(EmojiTransformer):
    def __init__(self, dictionary: dict):
        self.dictionary = dictionary
        escaped_words = [re.escape(word) for word in dictionary.keys()]
        pattern = r"\b(" + "|".join(escaped_words) + r")\b"
        self.regex = re.compile(pattern, re.IGNORECASE)

    #def transform(self, text: str) -> str:
    #    match = self.regex.search(text)
    #    if match:
    #        word = match.group(1).lower()
    #        return self.dictionary.get(word, "❓")
    #    return "❓"

    def transform(self, text: str) -> str:
        # Find all matches
        matches = self.regex.findall(text)
        if not matches:
            return "❓"

        # Map each word to an emoji
        emojis = [self.dictionary.get(word.lower(), "❓") for word in matches]

        # Remove duplicates if you want
        emojis = list(dict.fromkeys(emojis))

        # Join into a string
        return " ".join(emojis)