from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.module.user.application.use_cases.delete_user_use_case import DeleteUserUseCase
from app.module.user.domain.enums import UserRole
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


@pytest.fixture
def user_read_adapter():
    return MagicMock()


@pytest.fixture
def user_write_adapter():
    return MagicMock()


@pytest.fixture
def use_case(user_read_adapter, user_write_adapter):
    return DeleteUserUseCase(
        user_read_adapter=user_read_adapter,
        user_write_adapter=user_write_adapter,
    )


@pytest.fixture
def existing_user():
    return UserResponseDto(
        id=5,
        email="todelete@example.com",
        first_name="To",
        last_name="Delete",
        role=UserRole.DRIVER,
    )


class TestDeleteUserUseCase:
    def test_execute_happy_path(self, use_case, user_read_adapter, user_write_adapter, existing_user):
        # Given
        user_read_adapter.find_by_id.return_value = existing_user

        # When
        result = use_case.execute(5)

        # Then
        assert result is None
        user_read_adapter.find_by_id.assert_called_once_with(5)
        user_write_adapter.delete.assert_called_once_with(5)

    def test_execute_user_not_found_raises_404(self, use_case, user_read_adapter, user_write_adapter):
        # Given
        user_read_adapter.find_by_id.return_value = None

        # When / Then
        with pytest.raises(HTTPException) as exc_info:
            use_case.execute(999)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"
        user_write_adapter.delete.assert_not_called()
