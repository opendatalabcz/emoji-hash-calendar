import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash

from app.services.user_service import UserService
from app.exceptions import (
    NotFoundError,
    ForbiddenError,
    ValidationError,
    AuthenticationError,
)


def test_assert_user_owns_resource_success():
    UserService.assert_user_owns_resource(1, 1)


def test_assert_user_owns_resource_forbidden():
    with pytest.raises(ForbiddenError):
        UserService.assert_user_owns_resource(1, 2)


def test_assert_admin_success():
    user = MagicMock(is_admin=True)
    UserService.assert_admin(user)


def test_assert_admin_forbidden():
    user = MagicMock(is_admin=False)
    with pytest.raises(ForbiddenError):
        UserService.assert_admin(user)


@patch("app.services.user_service.UserRepository")
def test_get_user_success(mock_repo):
    mock_user = MagicMock()
    mock_repo.get_by_id.return_value = mock_user

    result = UserService.get_user(1)

    assert result == mock_user
    mock_repo.get_by_id.assert_called_once_with(1)


@patch("app.services.user_service.UserRepository")
def test_get_user_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        UserService.get_user(1)


@patch("app.services.user_service.UserRepository")
def test_create_user_success_first_user_becomes_admin(mock_repo):
    mock_repo.get_by_username.return_value = None
    mock_repo.count.return_value = 0
    mock_repo.create.return_value = MagicMock()

    result = UserService.create_user("duy", "Password1", "Password1")

    assert result is not None
    mock_repo.create.assert_called_once()
    args, kwargs = mock_repo.create.call_args
    assert kwargs["is_admin"] is True


@patch("app.services.user_service.UserRepository")
def test_create_user_username_taken(mock_repo):
    mock_repo.get_by_username.return_value = MagicMock()

    with pytest.raises(ValidationError):
        UserService.create_user("duy", "Password1", "Password1")


@patch("app.services.user_service.UserRepository")
def test_create_user_password_mismatch(mock_repo):
    mock_repo.get_by_username.return_value = None

    with pytest.raises(ValidationError):
        UserService.create_user("duy", "Password1", "Different")


@patch("app.services.user_service.UserRepository")
def test_update_user_password_success(mock_repo):
    user = MagicMock(password=generate_password_hash("OldPass1"))
    mock_repo.get_by_id.return_value = user

    result = UserService.update_user_password(
        user_id=1,
        current_user_id=1,
        current_password="OldPass1",
        new_password="NewPass1",
        confirm_new_password="NewPass1",
    )

    assert result is not None
    mock_repo.update_password.assert_called_once()


@patch("app.services.user_service.UserRepository")
def test_update_user_password_user_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        UserService.update_user_password(1, 1, "a", "b", "b")


@patch("app.services.user_service.UserRepository")
def test_update_user_password_wrong_owner(mock_repo):
    user = MagicMock(password=generate_password_hash("OldPass1"))
    mock_repo.get_by_id.return_value = user

    with pytest.raises(ForbiddenError):
        UserService.update_user_password(1, 2, "OldPass1", "NewPass1", "NewPass1")


@patch("app.services.user_service.UserRepository")
def test_update_user_password_incorrect_current(mock_repo):
    user = MagicMock(password=generate_password_hash("OldPass1"))
    mock_repo.get_by_id.return_value = user

    with pytest.raises(ValidationError):
        UserService.update_user_password(1, 1, "WrongPass", "NewPass1", "NewPass1")


@patch("app.services.user_service.UserRepository")
def test_update_user_password_mismatch(mock_repo):
    user = MagicMock(password=generate_password_hash("OldPass1"))
    mock_repo.get_by_id.return_value = user

    with pytest.raises(ValidationError):
        UserService.update_user_password(1, 1, "OldPass1", "NewPass1", "Different")


@patch("app.services.user_service.UserRepository")
def test_make_admin_success(mock_repo):
    current_user = MagicMock(is_admin=True)
    target_user = MagicMock(is_admin=False)

    mock_repo.get_by_id.side_effect = [current_user, target_user]
    mock_repo.update_admin.return_value = target_user

    result = UserService.make_admin(2, 1)

    assert result == target_user
    mock_repo.update_admin.assert_called_once()


@patch("app.services.user_service.UserRepository")
def test_make_admin_not_admin(mock_repo):
    current_user = MagicMock(is_admin=False)
    mock_repo.get_by_id.return_value = current_user

    with pytest.raises(ForbiddenError):
        UserService.make_admin(2, 1)


@patch("app.services.user_service.UserRepository")
def test_make_admin_user_not_found(mock_repo):
    current_user = MagicMock(is_admin=True)
    mock_repo.get_by_id.side_effect = [current_user, None]

    with pytest.raises(NotFoundError):
        UserService.make_admin(2, 1)


@patch("app.services.user_service.UserRepository")
def test_delete_user_success(mock_repo):
    user = MagicMock()
    mock_repo.get_by_id.return_value = user

    UserService.delete_user(1, 1)

    mock_repo.delete.assert_called_once_with(user)


@patch("app.services.user_service.UserRepository")
def test_delete_user_not_found(mock_repo):
    mock_repo.get_by_id.return_value = None

    with pytest.raises(NotFoundError):
        UserService.delete_user(1, 1)


@patch("app.services.user_service.UserRepository")
def test_delete_user_wrong_owner(mock_repo):
    user = MagicMock()
    mock_repo.get_by_id.return_value = user

    with pytest.raises(ForbiddenError):
        UserService.delete_user(1, 2)


@patch("app.services.user_service.UserRepository")
def test_authenticate_success(mock_repo):
    user = MagicMock(password=generate_password_hash("Password1"))
    mock_repo.get_by_username.return_value = user

    result = UserService.authenticate("duy", "Password1")

    assert result == user


@patch("app.services.user_service.UserRepository")
def test_authenticate_missing_credentials(mock_repo):
    with pytest.raises(AuthenticationError):
        UserService.authenticate("", "Password1")


@patch("app.services.user_service.UserRepository")
def test_authenticate_user_not_found(mock_repo):
    mock_repo.get_by_username.return_value = None

    with pytest.raises(AuthenticationError):
        UserService.authenticate("duy", "Password1")


@patch("app.services.user_service.UserRepository")
def test_authenticate_wrong_password(mock_repo):
    user = MagicMock(password=generate_password_hash("Correct1"))
    mock_repo.get_by_username.return_value = user

    with pytest.raises(AuthenticationError):
        UserService.authenticate("duy", "WrongPass")
