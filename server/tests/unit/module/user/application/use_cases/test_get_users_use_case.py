from unittest.mock import MagicMock

import pytest

from app.module.user.application.use_cases.get_users_use_case import GetUsersUseCase
from app.module.user.domain.enums import UserRole
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


@pytest.fixture
def user_read_adapter():
    return MagicMock()


@pytest.fixture
def use_case(user_read_adapter):
    return GetUsersUseCase(user_read_adapter=user_read_adapter)


class TestGetUsersUseCase:
    def test_execute_returns_list(self, use_case, user_read_adapter):
        # Given
        users = [
            UserResponseDto(id=1, email="a@example.com", first_name="A", last_name="A", role=UserRole.OPERATOR),
            UserResponseDto(id=2, email="b@example.com", first_name="B", last_name="B", role=UserRole.ADMIN),
        ]
        user_read_adapter.find_all.return_value = users

        # When
        result = use_case.execute()

        # Then
        assert len(result) == 2
        assert result[0].id == 1
        assert result[1].id == 2
        user_read_adapter.find_all.assert_called_once()

    def test_execute_returns_empty_list(self, use_case, user_read_adapter):
        # Given
        user_read_adapter.find_all.return_value = []

        # When
        result = use_case.execute()

        # Then
        assert result == []
        user_read_adapter.find_all.assert_called_once()
