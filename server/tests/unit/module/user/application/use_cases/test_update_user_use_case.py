from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.module.user.application.use_cases.update_user_use_case import UpdateUserUseCase
from app.module.user.domain.enums import UserRole
from app.module.user.infrastructure.dtos.inputs import UserUpdateDto
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


@pytest.fixture
def user_read_adapter():
    return MagicMock()


@pytest.fixture
def user_write_adapter():
    return MagicMock()


@pytest.fixture
def use_case(user_write_adapter, user_read_adapter):
    return UpdateUserUseCase(
        user_write_adapter=user_write_adapter,
        user_read_adapter=user_read_adapter,
    )


@pytest.fixture
def existing_user():
    return UserResponseDto(
        id=1,
        email="old@example.com",
        first_name="Old",
        last_name="Name",
        role=UserRole.OPERATOR,
    )


@pytest.fixture
def updated_user():
    return UserResponseDto(
        id=1,
        email="new@example.com",
        first_name="New",
        last_name="Name",
        role=UserRole.OPERATOR,
    )


class TestUpdateUserUseCase:
    def test_execute_happy_path(self, use_case, user_read_adapter, user_write_adapter, existing_user, updated_user):
        # Given
        dto = UserUpdateDto(email="new@example.com", first_name="New", last_name="Name")
        user_read_adapter.find_by_id.return_value = existing_user
        user_write_adapter.update.return_value = updated_user

        # When
        result = use_case.execute(1, dto)

        # Then
        assert result.email == "new@example.com"
        assert result.first_name == "New"
        user_read_adapter.find_by_id.assert_called_once_with(1)
        user_write_adapter.update.assert_called_once()
        called_dto = user_write_adapter.update.call_args[0][0]
        assert called_dto.id == 1
        assert called_dto.email == "new@example.com"

    def test_execute_user_not_found_raises_404(self, use_case, user_read_adapter):
        # Given
        dto = UserUpdateDto(email="new@example.com")
        user_read_adapter.find_by_id.return_value = None

        # When / Then
        with pytest.raises(HTTPException) as exc_info:
            use_case.execute(999, dto)

        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "User not found"
