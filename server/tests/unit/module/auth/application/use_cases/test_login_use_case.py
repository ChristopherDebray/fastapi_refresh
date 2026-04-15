from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.module.auth.application.use_cases.login_use_case import LoginUseCase
from app.module.auth.infrastructure.dtos.inputs import LoginDto
from app.module.auth.infrastructure.dtos.outputs import AuthUserWithPasswordDto
from app.module.user.domain.enums import UserRole


# Les fixtures sont load une seule fois puis on charge l'élélement déjà load dans les tests sans les ré instancier
@pytest.fixture
def mock_user():
    return AuthUserWithPasswordDto(
        id=1,
        email="user@example.com",
        first_name="John",
        last_name="Doe",
        password="hashed_password",
        role=UserRole.OPERATOR,
    )


@pytest.fixture
def auth_read_repo():
    return MagicMock()


@pytest.fixture
def use_case(auth_read_repo):
    return LoginUseCase(auth_read_repo=auth_read_repo)


class TestLoginUseCase:
    def test_execute_happy_path(self, use_case, auth_read_repo, mock_user):
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
                return_value="jwt_token_abc",
            ),
        ):
            # When
            result = use_case.execute(dto)

        # Then
        assert result.access_token == "jwt_token_abc"
        assert result.user.id == 1
        assert result.user.email == "user@example.com"
        auth_read_repo.find_by_email.assert_called_once_with("user@example.com")

    def test_execute_user_not_found_raises_401(self, use_case, auth_read_repo):
        # Given
        dto = LoginDto(email="ghost@example.com", password="anypassword")
        auth_read_repo.find_by_email.return_value = None

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
            # When / Then
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute(dto)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid credentials"
