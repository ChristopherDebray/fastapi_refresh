from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from app.module.auth.application.use_cases.refresh_token_use_case import RefreshTokenUseCase
from app.module.auth.infrastructure.dtos.outputs import AuthUserWithPasswordDto
from app.module.user.domain.enums import UserRole


def make_user(**kwargs) -> AuthUserWithPasswordDto:
    defaults = {
        "id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "hashed_password",
        "refresh_token": "valid_refresh_token",
        "role": UserRole.OPERATOR,
    }
    return AuthUserWithPasswordDto(**{**defaults, **kwargs})


class TestRefreshTokenUseCase:
    def test_execute_happy_path(self):
        # Given
        auth_read_repo = MagicMock()
        auth_write_repo = MagicMock()
        use_case = RefreshTokenUseCase(auth_read_repo=auth_read_repo, auth_write_repo=auth_write_repo)

        user = make_user()
        auth_read_repo.find_by_id.return_value = user

        with (
            patch(
                "app.module.auth.application.use_cases.refresh_token_use_case.JwtService.decode_refresh_token",
                return_value=MagicMock(user_id=1, email="user@example.com"),
            ),
            patch(
                "app.module.auth.application.use_cases.refresh_token_use_case.JwtService.create_access_token",
                return_value="new_access_token",
            ),
            patch(
                "app.module.auth.application.use_cases.refresh_token_use_case.JwtService.create_refresh_token",
                return_value="new_refresh_token",
            ),
        ):
            # When
            result = use_case.execute("valid_refresh_token")

        # Then
        assert result.access_token == "new_access_token"
        assert result.refresh_token == "new_refresh_token"
        assert result.user.id == 1
        assert result.user.email == "user@example.com"
        auth_write_repo.save_refresh_token.assert_called_once_with(1, "new_refresh_token")

    def test_execute_invalid_jwt_raises_401(self):
        # Given
        auth_read_repo = MagicMock()
        auth_write_repo = MagicMock()
        use_case = RefreshTokenUseCase(auth_read_repo=auth_read_repo, auth_write_repo=auth_write_repo)

        with patch(
            "app.module.auth.application.use_cases.refresh_token_use_case.JwtService.decode_refresh_token",
            side_effect=Exception("invalid token"),
        ):
            # When / Then
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute("bad_token")

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid or expired refresh token"
        auth_write_repo.save_refresh_token.assert_not_called()

    def test_execute_user_not_found_raises_401(self):
        # Given
        auth_read_repo = MagicMock()
        auth_write_repo = MagicMock()
        use_case = RefreshTokenUseCase(auth_read_repo=auth_read_repo, auth_write_repo=auth_write_repo)

        auth_read_repo.find_by_id.return_value = None

        with patch(
            "app.module.auth.application.use_cases.refresh_token_use_case.JwtService.decode_refresh_token",
            return_value=MagicMock(user_id=99),
        ):
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute("valid_jwt_unknown_user")

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "User not found"

    def test_execute_token_mismatch_raises_401(self):
        # Given
        auth_read_repo = MagicMock()
        auth_write_repo = MagicMock()
        use_case = RefreshTokenUseCase(auth_read_repo=auth_read_repo, auth_write_repo=auth_write_repo)

        user = make_user(refresh_token="stored_token")
        auth_read_repo.find_by_id.return_value = user

        with patch(
            "app.module.auth.application.use_cases.refresh_token_use_case.JwtService.decode_refresh_token",
            return_value=MagicMock(user_id=1),
        ):
            with pytest.raises(HTTPException) as exc_info:
                use_case.execute("different_token")

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Invalid refresh token"
        auth_write_repo.save_refresh_token.assert_not_called()
