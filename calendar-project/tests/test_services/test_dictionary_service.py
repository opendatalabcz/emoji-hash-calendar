import pytest
from unittest.mock import patch, MagicMock

from app.services.dictionary_service import DictionaryService
from app.exceptions import NotFoundError, ForbiddenError, ValidationError


@patch("app.services.dictionary_service.UserRepository")
def test_assert_admin_success(mock_repo):
    mock_repo.get_by_id.return_value = MagicMock(is_admin=True)
    DictionaryService._assert_admin(1)


@patch("app.services.dictionary_service.UserRepository")
def test_assert_admin_user_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        DictionaryService._assert_admin(1)


@patch("app.services.dictionary_service.UserRepository")
def test_assert_admin_forbidden(mock_repo):
    mock_repo.get_by_id.return_value = MagicMock(is_admin=False)

    with pytest.raises(ForbiddenError):
        DictionaryService._assert_admin(1)


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_get_all_dictionaries_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_all.return_value = ["d1", "d2"]

    result = DictionaryService.get_all_dictionaries(1)
    assert result == ["d1", "d2"]


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_get_dictionary_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = "dict"

    result = DictionaryService.get_dictionary(1, 10)
    assert result == "dict"


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_get_dictionary_not_found(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        DictionaryService.get_dictionary(1, 10)


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_create_dictionary_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.create.return_value = "created"

    result = DictionaryService.create_dictionary(1, "MyDict", "en", "desc")
    assert result == "created"


@patch("app.services.dictionary_service.UserRepository")
def test_create_dictionary_missing_fields(mock_user_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)

    with pytest.raises(ValidationError):
        DictionaryService.create_dictionary(1, "", "en")


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_delete_dictionary_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = "dict"

    DictionaryService.delete_dictionary(1, 10)
    mock_dict_repo.delete.assert_called_once_with("dict")


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_delete_dictionary_not_found(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        DictionaryService.delete_dictionary(1, 10)


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_get_entries_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = "dict"
    mock_dict_repo.get_entries.return_value = ["e1"]

    result = DictionaryService.get_entries(1, 10)
    assert result == ["e1"]


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_get_entries_dict_not_found(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        DictionaryService.get_entries(1, 10)


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_add_entry_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = "dict"
    mock_dict_repo.add_entry.return_value = "entry"

    result = DictionaryService.add_entry(1, 10, "hello", "👋")
    assert result == "entry"


@patch("app.services.dictionary_service.UserRepository")
def test_add_entry_missing_fields(mock_user_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)

    with pytest.raises(ValidationError):
        DictionaryService.add_entry(1, 10, "", "👋")


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_add_entry_dict_not_found(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        DictionaryService.add_entry(1, 10, "hello", "👋")


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_delete_entry_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)

    entry = MagicMock(id=5)
    mock_dict_repo.get_by_id.return_value = "dict"
    mock_dict_repo.get_entries.return_value = [entry]

    DictionaryService.delete_entry(1, 10, 5)
    mock_dict_repo.delete_entry.assert_called_once_with(entry)


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_delete_entry_not_found(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = "dict"
    mock_dict_repo.get_entries.return_value = []

    with pytest.raises(NotFoundError):
        DictionaryService.delete_entry(1, 10, 5)


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_bulk_insert_success(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = "dict"
    mock_dict_repo.bulk_insert.return_value = 3

    result = DictionaryService.bulk_insert_entries(1, 10, {"hello": "👋"})
    assert result == 3


@patch("app.services.dictionary_service.UserRepository")
def test_bulk_insert_invalid_type(mock_user_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)

    with pytest.raises(ValidationError):
        DictionaryService.bulk_insert_entries(1, 10, ["not", "a", "dict"])


@patch("app.services.dictionary_service.DictionaryRepository")
@patch("app.services.dictionary_service.UserRepository")
def test_bulk_insert_empty(mock_user_repo, mock_dict_repo):
    mock_user_repo.get_by_id.return_value = MagicMock(is_admin=True)
    mock_dict_repo.get_by_id.return_value = "dict"

    with pytest.raises(ValidationError):
        DictionaryService.bulk_insert_entries(1, 10, {})


@patch("app.services.dictionary_service.DictionaryRepository")
def test_to_dict_success(mock_repo):
    entry1 = MagicMock(word="Hello", emoji="👋")
    entry2 = MagicMock(word="Cat", emoji="🐱")

    mock_repo.get_entries.return_value = [entry1, entry2]

    result = DictionaryService.to_dict(10)

    assert result == {"hello": "👋", "cat": "🐱"}
