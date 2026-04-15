from unittest.mock import MagicMock

import pytest

from app.module.user.application.use_cases.get_user_use_case import GetUserUseCase
from app.module.user.domain.enums import UserRole
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


@pytest.fixture
def user_read_adapter():
    return MagicMock()


@pytest.fixture
def use_case(user_read_adapter):
    return GetUserUseCase(user_read_adapter=user_read_adapter)


@pytest.fixture
def response_dto():
    return UserResponseDto(
        id=42,
        email="john@example.com",
        first_name="John",
        last_name="Doe",
        role=UserRole.ADMIN,
    )


class TestGetUserUseCase:
    def test_execute_happy_path(self, use_case, user_read_adapter, response_dto):
        # Given
        user_read_adapter.find_by_id.return_value = response_dto

        # When
        result = use_case.execute(42)

        # Then
        assert result.id == 42
        assert result.email == "john@example.com"
        user_read_adapter.find_by_id.assert_called_once_with(42)

    def test_execute_not_found_returns_none(self, use_case, user_read_adapter):
        # Given
        user_read_adapter.find_by_id.return_value = None

        # When
        result = use_case.execute(999)

        # Then
        assert result is None
        user_read_adapter.find_by_id.assert_called_once_with(999)
