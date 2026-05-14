import requests
import base64
from io import BytesIO

from app.models.domain_models.calendar import Calendar
from app.utilities.exporters.ics_exporter import ICSExporter
from app.utilities.importers.ics_importer import ICSImporter

from app.utilities.emoji_transformers.dictionary_transformer import DictionaryTransformer
from app.utilities.emoji_transformers.embedding_transformer import EmbeddingTransformer

from app.exceptions import ValidationError, AppException
from app.constants import EMBEDDING_MODELS
from app.services.dictionary_service import DictionaryService


class CalendarService:
    _model_cache: dict = {}

    def __init__(self, importer=None, exporter=None):
        self.importer = importer or ICSImporter()
        self.exporter = exporter or ICSExporter()

    @staticmethod
    def _build_mapping(dictionary_id, user_mapping):
        """
        Method builds final dictionary from a combination of chosen dictionary and user mapping.
        User mappings extend or replace entries in dictionary
        """
        if user_mapping is not None and not isinstance(user_mapping, dict):
            raise ValidationError("user_mapping must be a valid JSON object")

        db_dict = DictionaryService.to_dict(dictionary_id) if dictionary_id else {}
        final_mapping = db_dict.copy()
        if user_mapping:
            final_mapping.update(user_mapping)

        return final_mapping

    @staticmethod
    def _download_ics(url, validate_content_type=False):
        resp = requests.get(url, timeout=10)
        if resp.status_code != 200:
            raise ValidationError("Failed to download ICS file")

        if validate_content_type:
            content_type = resp.headers.get("Content-Type", "").lower()
            if "calendar" not in content_type and "octet-stream" not in content_type:
                raise ValidationError("URL did not return a calendar file")

        return BytesIO(resp.content)


    @staticmethod
    def generate_subscription_link(base_url, ics_url, method, dictionary_id, user_mapping):
        from urllib.parse import urlencode
        import json

        params = {"ics_url": ics_url, "method": method}

        if dictionary_id is not None:
            params["dictionary_id"] = dictionary_id

        if user_mapping:
            params["user_mapping"] = json.dumps(user_mapping)

        return f"{base_url.rstrip('/')}/feed?{urlencode(params)}"

    def generate_feed(self, ics_url, method, dictionary_id, user_mapping):
        input_stream = self._download_ics(ics_url)
        mapping = self._build_mapping(dictionary_id, user_mapping)

        output_stream, _ = self.transform_calendar_stream(input_stream, method, mapping)
        output_stream.seek(0)
        return output_stream.read()

    def transform_calendar(self, ics_url, method, dictionary_id, user_mapping):
        input_stream = self._download_ics(ics_url, validate_content_type=True)
        mapping = self._build_mapping(dictionary_id, user_mapping)

        output_stream, preview = self.transform_calendar_stream(input_stream, method, mapping)
        output_stream.seek(0)

        return {
            "message": "Transformation complete",
            "ics_base64": base64.b64encode(output_stream.read()).decode("utf-8"),
            "preview": preview[:10]
        }

    def transform_calendar_from_bytes(self, file_bytes: bytes, method: str, dictionary_id, user_mapping):
        if not file_bytes:
            raise ValidationError("Uploaded ICS file is empty")

        input_stream = BytesIO(file_bytes)
        mapping = self._build_mapping(dictionary_id, user_mapping)

        output_stream, preview = self.transform_calendar_stream(input_stream, method, mapping)
        output_stream.seek(0)

        return {
            "message": "Transformation complete",
            "ics_base64": base64.b64encode(output_stream.read()).decode("utf-8"),
            "preview": preview[:10]
        }

    def transform_text(self, text, method, dictionary_id, user_mapping):
        mapping = self._build_mapping(dictionary_id, user_mapping)
        return self.transform_text_to_emoji(text, method, mapping)


    def transform_calendar_stream(self, input_stream: BytesIO, method: str, emoji_dict: dict | None = None):
        if not input_stream:
            raise ValidationError("Input ICS stream is empty")

        events = self.importer.load_stream(input_stream)
        if not events:
            raise ValidationError("ICS file contains no events")

        calendar = Calendar()
        for event in events:
            calendar.add_event(event)

        transformer = self._get_transformer(method, emoji_dict)

        preview = []
        for event in calendar.get_events():
            emojis = transformer.transform(event.title)
            event.emoji = " ".join(emojis) if emojis else "❓"
            preview.append({"title_original": event.title, "title_transformed": event.emoji})

        output_stream = BytesIO()
        self.exporter.export_stream(output_stream, calendar.get_events())
        output_stream.seek(0)

        return output_stream, preview

    def transform_text_to_emoji(self, text: str, method: str, emoji_dict: dict | None = None) -> str:
        if not text or not text.strip():
            raise ValidationError("Text cannot be empty")

        transformer = self._get_transformer(method, emoji_dict)
        emojis = transformer.transform(text)
        return " ".join(emojis) if emojis else "❓"

    @classmethod
    def _get_transformer(cls, method: str, emoji_dict: dict | None = None):
        if not method:
            raise ValidationError("Transformation method is required")

        emoji_dict = {k.lower(): v for k, v in (emoji_dict or {}).items()}

        if method == "dictionary":
            return DictionaryTransformer(emoji_dict)

        model_name = EMBEDDING_MODELS.get(method)
        if not model_name:
            raise ValidationError(f"Unknown transformation method: {method}")

        try:
            if model_name not in cls._model_cache:
                from sentence_transformers import SentenceTransformer
                cls._model_cache[model_name] = SentenceTransformer(model_name)
        except Exception as e:
            raise AppException(f"Failed to load embedding model '{model_name}': {str(e)}")

        return EmbeddingTransformer(emoji_dict, cls._model_cache[model_name], threshold=0.6)