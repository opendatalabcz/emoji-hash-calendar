from abc import ABC, abstractmethod

class EmojiTransformer(ABC):
    @abstractmethod
    def transform(self, text: str) -> list[str]:
        pass