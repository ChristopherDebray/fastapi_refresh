from unittest.mock import MagicMock

from app.core.security.token_payload import TokenPayloadDto
from app.module.auth.application.use_cases.logout_use_case import LogoutUseCase
from app.module.user.domain.enums import UserRole


def make_token_payload(**kwargs) -> TokenPayloadDto:
    defaults = {
        "id": 1,
        "sub": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": UserRole.OPERATOR,
    }
    return TokenPayloadDto(**{**defaults, **kwargs})


class TestLogoutUseCase:
    def test_execute_clears_refresh_token(self):
        # Given
        write_repo = MagicMock()
        use_case = LogoutUseCase(write_repo=write_repo)
        current_user = make_token_payload(id=42)

        # When
        result = use_case.execute(current_user)

        # Then
        write_repo.save_refresh_token.assert_called_once_with(42, None)
        assert result is None

    def test_execute_uses_user_id_from_token(self):
        # Given
        write_repo = MagicMock()
        use_case = LogoutUseCase(write_repo=write_repo)

        for user_id in [1, 99, 1000]:
            write_repo.reset_mock()
            current_user = make_token_payload(id=user_id, sub=user_id)

            # When
            use_case.execute(current_user)

            # Then
            write_repo.save_refresh_token.assert_called_once_with(user_id, None)
