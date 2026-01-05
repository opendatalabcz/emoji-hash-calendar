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

    """def transform_calendar(self, filepath: str, method: str, user_mapping: dict | None = None) -> str:
        # old transform using filepath not streams
        calendar = Calendar()
        for event in self.importer.load_file(filepath):
            calendar.add_event(event)

        # Select transformation strategy
        transformer = self._get_transformer(method, user_mapping)

        # Apply transformations
        for event in calendar.get_events():
            event.emoji = transformer.transform(event.title)

        # Export updated calendar
        output_path = "output.ics"
        self.exporter.export(output_path, calendar.get_events())

        return output_path
    """

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
            event.emoji = transformer.transform(event.title)

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
        return transformer.transform(text)


    def _get_transformer(self, method: str, user_mapping: dict | None = None):
        with open("utils/emoji_dict.json") as f:
            emoji_dict = {k.lower(): v for k, v in json.load(f).items()}

        # Returns the correct transformer
        if method == "dictionary":
            base_transformer = DictionaryTransformer(emoji_dict)

        elif method == "embedding - all-MiniLM-L6-v2":
            base_transformer = EmbeddingTransformer(emoji_dict, "all-MiniLM-L6-v2")

        elif method == "embedding - all-MiniLM-L12-v2":
            base_transformer = EmbeddingTransformer(emoji_dict, "all-MiniLM-L12-v2")

        # TODO: add other transformers_class

        # Error handling
        else:
            raise ValueError(f"Unknown transformation method: {method}")

        # If user mapping added
        if user_mapping:
            return PriorityTransformer(base_transformer, user_mapping)

        return base_transformer