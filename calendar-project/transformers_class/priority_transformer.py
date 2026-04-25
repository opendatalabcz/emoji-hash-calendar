import re
from transformers_class.emoji_transformer import EmojiTransformer


class PriorityTransformer(EmojiTransformer):
    def __init__(self, base_transformer: EmojiTransformer, user_mapping: dict):
        self.base = base_transformer
        self.user_mapping = {k.lower(): v for k, v in user_mapping.items()}

        escaped_words = [re.escape(word) for word in self.user_mapping.keys()]
        pattern = r"\b(" + "|".join(escaped_words) + r")\b"
        self.regex = re.compile(pattern, re.IGNORECASE)

    """def transform(self, text: str) -> str:
        match = self.regex.search(text)
        if match:
            word = match.group(1).lower()
            return self.user_mapping[word]

        # Fallback to base transformer
        return self.base.transform(text)"""

    def transform(self, text: str) -> str:

        user_emojis = []
        for match in self.regex.finditer(text):
            word = match.group(1).lower()
            emoji = self.user_mapping[word]
            if emoji not in user_emojis:
                user_emojis.append(emoji)

        base_emojis_str = self.base.transform(text)
        base_emojis = base_emojis_str.split() if base_emojis_str != "❓" else []

        all_emojis = user_emojis + [e for e in base_emojis if e not in user_emojis]

        if not all_emojis:
            return "❓"

        return " ".join(all_emojis)