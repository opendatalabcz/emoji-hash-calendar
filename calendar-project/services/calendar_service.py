import json
from io import BytesIO
from models.calendar import Calendar
from transformers_class.dictionary_transformer import DictionaryTransformer
from exporters.exporter import CalendarExporter
from importers.importer import CalendarImporter
from transformers_class.embedding_transformer import EmbeddingTransformer
from transformers_class.priority_transformer import PriorityTransformer


class CalendarService:
    def __init__(self, importer=None, exporter=None):
        self.importer = importer or CalendarImporter()
        self.exporter = exporter or CalendarExporter()

        with open("utils/emoji_dict.json") as f:
            self.emoji_dict = {k.lower(): v for k, v in json.load(f).items()}

    def transform_calendar_stream(self, input_stream: BytesIO, method: str,user_mapping: dict | None = None) -> tuple[BytesIO, list]:
        # Load calendar from stream
        calendar = Calendar()
        for event in self.importer.load_stream(input_stream):
            calendar.add_event(event)

        # Select transformer
        transformer = self._get_transformer(method, user_mapping)

        preview = []

        # Apply transformation
        for event in calendar.get_events():
            emojis: list[str] = transformer.transform(event.title)
            event.emoji = " ".join(emojis) if emojis else "?"

            preview.append({
                "title_original": event.title,
                "title_transformed": event.emoji
            })

        # Export to in-memory stream
        output_stream = BytesIO()
        self.exporter.export_stream(output_stream, calendar.get_events())
        output_stream.seek(0)
        return output_stream, preview

    def transform_text_to_emoji(self, text: str, method: str, user_mapping: dict | None = None) -> str:
        """
        Convert input text into emoji(s) using the selected method.
        - method: "dictionary" or "embedding"
        - user_mapping: optional keyword → emoji dict
        """
        transformer = self._get_transformer(method, user_mapping)
        emojis = transformer.transform(text)
        return " ".join(emojis) if emojis else "?"


    def _get_transformer(self, method: str, user_mapping: dict | None = None):
        emoji_dict = self.emoji_dict.copy()

        if user_mapping:
            emoji_dict.update({k.lower(): v for k, v in user_mapping.items()})

        # Returns the correct transformer
        if method == "dictionary":
            base_transformer = DictionaryTransformer(emoji_dict)

        elif method == "embedding - all-MiniLM-L6-v2":
            base_transformer = EmbeddingTransformer(emoji_dict, "all-MiniLM-L6-v2")

        elif method == "embedding - all-MiniLM-L12-v2":
            base_transformer = EmbeddingTransformer(emoji_dict, "all-MiniLM-L12-v2")

        elif method == "embedding - balanced":
            base_transformer = EmbeddingTransformer(emoji_dict, "all-mpnet-base-v2")

        elif method == "embedding - multilingual":
            base_transformer = EmbeddingTransformer(emoji_dict, "paraphrase-multilingual-MiniLM-L12-v2")

        elif method == "embedding - bge":
            base_transformer = EmbeddingTransformer(emoji_dict, "BAAI/bge-small-en-v1.5")

        # TODO: add other transformers_class

        # Error handling
        else:
            raise ValueError(f"Unknown transformation method: {method}")

        # If user mapping added
        #if user_mapping:
        #    return PriorityTransformer(base_transformer, user_mapping)

        return base_transformer