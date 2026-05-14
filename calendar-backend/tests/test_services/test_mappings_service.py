import pytest
from unittest.mock import patch, MagicMock

from app.services.mappings_service import MappingService
from app.exceptions import NotFoundError, ForbiddenError, ValidationError


@patch("app.services.mappings_service.UserRepository")
def test_assert_user_exists_success(mock_repo):
    mock_repo.get_by_id.return_value = MagicMock()
    MappingService._assert_user_exists(1)


@patch("app.services.mappings_service.UserRepository")
def test_assert_user_exists_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(NotFoundError):
        MappingService._assert_user_exists(1)


@patch("app.services.mappings_service.MappingRepository")
def test_get_user_set_success(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set

    result = MappingService._get_user_set(10, 1)
    assert result == mock_set


@patch("app.services.mappings_service.MappingRepository")
def test_get_user_set_not_found(mock_repo):
    mock_repo.get_set_by_id.return_value = None

    with pytest.raises(NotFoundError):
        MappingService._get_user_set(10, 1)


@patch("app.services.mappings_service.MappingRepository")
def test_get_user_set_forbidden(mock_repo):
    mock_set = MagicMock(user_id=2)
    mock_repo.get_set_by_id.return_value = mock_set

    with pytest.raises(ForbiddenError):
        MappingService._get_user_set(10, 1)


@patch("app.services.mappings_service.MappingRepository")
@patch("app.services.mappings_service.UserRepository")
def test_get_user_sets_success(mock_user_repo, mock_map_repo):
    mock_user_repo.get_by_id.return_value = MagicMock()
    mock_map_repo.get_all_sets_by_user.return_value = ["set1"]

    result = MappingService.get_user_sets(1)
    assert result == ["set1"]


@patch("app.services.mappings_service.UserRepository")
def test_get_user_sets_user_not_found(mock_user_repo):
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        MappingService.get_user_sets(1)


@patch("app.services.mappings_service.MappingRepository")
@patch("app.services.mappings_service.UserRepository")
def test_create_set_success(mock_user_repo, mock_map_repo):
    mock_user_repo.get_by_id.return_value = MagicMock()
    mock_map_repo.create_set.return_value = "created"

    result = MappingService.create_set(1, "My Set")
    assert result == "created"


@patch("app.services.mappings_service.UserRepository")
def test_create_set_user_not_found(mock_user_repo):
    mock_user_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        MappingService.create_set(1, "My Set")


@patch("app.services.mappings_service.UserRepository")
def test_create_set_missing_name(mock_user_repo):
    mock_user_repo.get_by_id.return_value = MagicMock()

    with pytest.raises(ValidationError):
        MappingService.create_set(1, "")


@patch("app.services.mappings_service.MappingRepository")
def test_delete_set_success(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set

    MappingService.delete_set(10, 1)
    mock_repo.delete_set.assert_called_once_with(mock_set)


@patch("app.services.mappings_service.MappingRepository")
def test_delete_set_forbidden(mock_repo):
    mock_set = MagicMock(user_id=2)
    mock_repo.get_set_by_id.return_value = mock_set

    with pytest.raises(ForbiddenError):
        MappingService.delete_set(10, 1)


@patch("app.services.mappings_service.MappingRepository")
def test_get_mappings_success(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set
    mock_repo.get_mappings_by_set.return_value = ["m1"]

    result = MappingService.get_mappings(10, 1)
    assert result == ["m1"]


@patch("app.services.mappings_service.MappingRepository")
def test_create_mapping_success(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set
    mock_repo.create_mapping.return_value = "created"

    result = MappingService.create_mapping(10, 1, "hello", "👋")
    assert result == "created"


@patch("app.services.mappings_service.MappingRepository")
def test_create_mapping_missing_word(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set

    with pytest.raises(ValidationError):
        MappingService.create_mapping(10, 1, "", "👋")


@patch("app.services.mappings_service.MappingRepository")
def test_create_mapping_missing_emoji(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set

    with pytest.raises(ValidationError):
        MappingService.create_mapping(10, 1, "hello", None)


@patch("app.services.mappings_service.MappingRepository")
def test_delete_mapping_success(mock_repo):
    mock_mapping = MagicMock()
    mock_mapping.mapping_set.user_id = 1
    mock_repo.get_mapping_by_id.return_value = mock_mapping

    MappingService.delete_mapping(5, 1)
    mock_repo.delete_mapping.assert_called_once_with(mock_mapping)


@patch("app.services.mappings_service.MappingRepository")
def test_delete_mapping_not_found(mock_repo):
    mock_repo.get_mapping_by_id.return_value = None

    with pytest.raises(NotFoundError):
        MappingService.delete_mapping(5, 1)


@patch("app.services.mappings_service.MappingRepository")
def test_delete_mapping_forbidden(mock_repo):
    mock_mapping = MagicMock()
    mock_mapping.mapping_set.user_id = 2
    mock_repo.get_mapping_by_id.return_value = mock_mapping

    with pytest.raises(ForbiddenError):
        MappingService.delete_mapping(5, 1)


@patch("app.services.mappings_service.MappingRepository")
def test_update_set_success(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set

    result = MappingService.update_set(
        set_id=10,
        user_id=1,
        name="Updated",
        mappings=[{"word": "hello", "emoji": "👋"}]
    )

    assert result == mock_set
    mock_repo.delete_mappings_by_set.assert_called_once_with(10)
    mock_repo.create_mapping.assert_called_once()
    mock_repo.save.assert_called_once_with(mock_set)


@patch("app.services.mappings_service.MappingRepository")
def test_update_set_invalid_mapping(mock_repo):
    mock_set = MagicMock(user_id=1)
    mock_repo.get_set_by_id.return_value = mock_set

    with pytest.raises(ValidationError):
        MappingService.update_set(
            10, 1, "Updated",
            mappings=[{"word": "", "emoji": "👋"}]
        )
