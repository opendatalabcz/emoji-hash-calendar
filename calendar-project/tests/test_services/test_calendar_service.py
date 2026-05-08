import pytest
from unittest.mock import patch, MagicMock
from io import BytesIO

from app.services.calendar_service import CalendarService
from app.exceptions import ValidationError, AppException


def test_generate_subscription_link():
    link = CalendarService.generate_subscription_link(
        base_url="https://example.com",
        ics_url="https://ics.com/a.ics",
        method="dictionary",
        dictionary_id=5,
        user_mapping={"meeting": "📅"}
    )

    assert link.startswith("https://example.com/feed?")
    assert "ics_url=https%3A%2F%2Fics.com%2Fa.ics" in link
    assert "method=dictionary" in link
    assert "dictionary_id=5" in link
    assert "user_mapping=" in link


@patch("app.services.calendar_service.requests.get")
def test_download_ics_success(mock_get):
    mock_resp = MagicMock(status_code=200, content=b"ICS DATA", headers={"Content-Type": "text/calendar"})
    mock_get.return_value = mock_resp

    stream = CalendarService._download_ics("https://example.com/test.ics")
    assert isinstance(stream, BytesIO)
    assert stream.read() == b"ICS DATA"


@patch("app.services.calendar_service.requests.get")
def test_download_ics_invalid_status(mock_get):
    mock_resp = MagicMock(status_code=404)
    mock_get.return_value = mock_resp

    with pytest.raises(ValidationError):
        CalendarService._download_ics("https://example.com/test.ics")


@patch("app.services.calendar_service.requests.get")
def test_download_ics_invalid_content_type(mock_get):
    mock_resp = MagicMock(
        status_code=200,
        content=b"DATA",
        headers={"Content-Type": "text/html"}
    )
    mock_get.return_value = mock_resp

    with pytest.raises(ValidationError):
        CalendarService._download_ics("https://example.com/test.ics", validate_content_type=True)


@patch("app.services.calendar_service.DictionaryService")
def test_build_mapping_merge(mock_dict_service):
    mock_dict_service.to_dict.return_value = {"meeting": "📅"}

    result = CalendarService._build_mapping(
        dictionary_id=1,
        user_mapping={"party": "🎉"}
    )

    assert result == {"meeting": "📅", "party": "🎉"}


@patch("app.services.calendar_service.DictionaryTransformer")
def test_transform_text_to_emoji_dictionary(mock_transformer):
    mock_transformer.return_value.transform.return_value = ["📅"]

    service = CalendarService()
    result = service.transform_text_to_emoji("meeting", "dictionary", {"meeting": "📅"})

    assert result == "📅"


def test_transform_text_to_emoji_empty():
    service = CalendarService()

    with pytest.raises(ValidationError):
        service.transform_text_to_emoji("", "dictionary", {})


@patch("app.services.calendar_service.DictionaryTransformer")
def test_get_transformer_dictionary(mock_transformer):
    result = CalendarService._get_transformer("dictionary", {"a": "b"})
    assert result == mock_transformer.return_value


@patch("sentence_transformers.SentenceTransformer")
def test_get_transformer_embedding_success(mock_model):
    mock_model.return_value = MagicMock()

    result = CalendarService._get_transformer("embedding - balanced", {})
    assert result is not None  # EmbeddingTransformer instance


def test_get_transformer_unknown_method():
    with pytest.raises(ValidationError):
        CalendarService._get_transformer("invalid", {})


@patch("sentence_transformers.SentenceTransformer", side_effect=Exception("fail"))
def test_get_transformer_embedding_failure(mock_model):
    CalendarService._model_cache.clear()

    with pytest.raises(AppException):
        CalendarService._get_transformer("embedding - balanced", {})


@patch("app.services.calendar_service.DictionaryTransformer")
def test_transform_calendar_stream_success(mock_transformer):
    mock_transformer.return_value.transform.return_value = ["📅"]

    mock_importer = MagicMock()
    mock_exporter = MagicMock()

    event = MagicMock(title="Meeting")
    mock_importer.load_stream.return_value = [event]

    service = CalendarService(importer=mock_importer, exporter=mock_exporter)

    output_stream, preview = service.transform_calendar_stream(
        input_stream=BytesIO(b"ICS"),
        method="dictionary",
        emoji_dict={"meeting": "📅"}
    )

    assert isinstance(output_stream, BytesIO)
    assert preview[0]["title_original"] == "Meeting"
    assert preview[0]["title_transformed"] == "📅"


def test_transform_calendar_stream_empty_stream():
    service = CalendarService()

    with pytest.raises(ValidationError):
        service.transform_calendar_stream(None, "dictionary", {})


def test_transform_calendar_stream_no_events():
    mock_importer = MagicMock()
    mock_importer.load_stream.return_value = []

    service = CalendarService(importer=mock_importer)

    with pytest.raises(ValidationError):
        service.transform_calendar_stream(BytesIO(b"ICS"), "dictionary", {})


@patch("app.services.calendar_service.CalendarService._download_ics")
@patch("app.services.calendar_service.CalendarService.transform_calendar_stream")
@patch("app.services.calendar_service.DictionaryService")
def test_transform_calendar_success(mock_dict_service, mock_transform, mock_download):
    mock_download.return_value = BytesIO(b"ICS")
    mock_dict_service.to_dict.return_value = {}
    mock_transform.return_value = (BytesIO(b"ICS_OUT"), [{"a": 1}])

    service = CalendarService()
    result = service.transform_calendar("url", "dictionary", None, None)

    assert result["message"] == "Transformation complete"
    assert "ics_base64" in result
    assert result["preview"] == [{"a": 1}]


@patch("app.services.calendar_service.CalendarService._download_ics")
@patch("app.services.calendar_service.CalendarService.transform_calendar_stream")
@patch("app.services.calendar_service.DictionaryService")
def test_generate_feed_success(mock_dict_service, mock_transform, mock_download):
    mock_download.return_value = BytesIO(b"ICS")
    mock_dict_service.to_dict.return_value = {}
    mock_transform.return_value = (BytesIO(b"ICS_OUT"), [])

    service = CalendarService()
    result = service.generate_feed("url", "dictionary", None, None)

    assert result == b"ICS_OUT"
