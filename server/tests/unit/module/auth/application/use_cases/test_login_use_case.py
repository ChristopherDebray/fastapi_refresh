from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.module.auth.application.use_cases.login_use_case import LoginUseCase
from app.module.auth.infrastructure.dtos.inputs import LoginDto
from app.module.auth.infrastructure.dtos.outputs import AuthUserWithPasswordDto
from app.module.user.domain.enums import UserRole


@pytest.fixture
def mock_user():
    return AuthUserWithPasswordDto(
        id=1,
        email="user@example.com",
        first_name="John",
        last_name="Doe",
        password="hashed_password",
        refresh_token="hashed_token",
        role=UserRole.OPERATOR,
    )


@pytest.fixture
def auth_read_repo():
    return MagicMock()


@pytest.fixture
def auth_write_repo():
    return MagicMock()


@pytest.fixture
def use_case(auth_read_repo, auth_write_repo):
    return LoginUseCase(auth_read_repo=auth_read_repo, auth_write_repo=auth_write_repo)


class TestLoginUseCase:
    def test_execute_happy_path(self, use_case, auth_read_repo, auth_write_repo, mock_user):
        # Given
        dto = LoginDto(email="user@example.com", password="plainpassword")
        auth_read_repo.find_by_email.return_value = mock_user

        with (
            patch(
                "app.module.auth.application.use_cases.login_use_case.EncryptService.verify",
                return_value=True,
            ),
            patch(
                "app.module.auth.application.use_cases.login_use_case.JwtService.create_access_token",
                return_value="access_token_abc",
            ),
            patch(
                "app.module.auth.application.use_cases.login_use_case.JwtService.create_refresh_token",
                return_value="refresh_token_abc",
            ),
        ):
            # When
            result = use_case.execute(dto)

        # Then
        assert result.access_token == "access_token_abc"
        assert result.refresh_token == "refresh_token_abc"
        assert result.user.id == 1
        assert result.user.email == "user@example.com"
        auth_read_repo.find_by_email.assert_called_once_with("user@example.com")
        auth_write_repo.save_refresh_token.assert_called_once_with(1, "refresh_token_abc")

    def test_execute_user_not_found_raises_401(self, use_case, auth_read_repo):
        # Given
        dto = LoginDto(email="ghost@example.com", password="anypassword")
        auth_read_repo.find_by_email.return_value = None

        # Ici pareil c'est pour que ton use case il lance un raise
        # pour tester les erreurs. as exc_info ça
        # je comprend pas le but, en théorie je dirais comme pr
        # result en haut ? Mais la tu peux mettre le retour
        # qui se stock dans exc_info automatiquement ?

        # When / Then
        with pytest.raises(HTTPException) as exc_info:
            use_case.execute(dto)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid credentials"

    def test_execute_wrong_password_raises_401(self, use_case, auth_read_repo, mock_user):
        # Given
        dto = LoginDto(email="user@example.com", password="wrongpassword")
        auth_read_repo.find_by_email.return_value = mock_user

        with patch(
            "app.module.auth.application.use_cases.login_use_case.EncryptService.verify",
            return_value=False,
        ):
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dto)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid credentials"

    def test_execute_does_not_save_refresh_token_on_invalid_credentials(self, use_case, auth_read_repo, auth_write_repo, mock_user):
        # Given
        dto = LoginDto(email="user@example.com", password="wrongpassword")
        auth_read_repo.find_by_email.return_value = mock_user

        with patch(
            "app.module.auth.application.use_cases.login_use_case.EncryptService.verify",
            return_value=False,
        ):
            with pytest.raises(HTTPException):
                use_case.execute(dto)

        auth_write_repo.save_refresh_token.assert_not_called()
