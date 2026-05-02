from abc import ABC, abstractmethod

class Transformer(ABC):
    @abstractmethod
    def transform(self, text: str) -> list[str]:
        pass