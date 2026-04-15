from unittest.mock import MagicMock, patch

import pytest

from app.module.user.application.use_cases.create_user_use_case import CreateUserUseCase
from app.module.user.domain.enums import UserRole
from app.module.user.infrastructure.dtos.inputs import UserCreateDto
from app.module.user.infrastructure.dtos.outputs import UserResponseDto


@pytest.fixture
def user_write_adapter():
    return MagicMock()


@pytest.fixture
def use_case(user_write_adapter):
    return CreateUserUseCase(user_write_adapter=user_write_adapter)


@pytest.fixture
def response_dto():
    return UserResponseDto(
        id=1,
        email="new@example.com",
        first_name="Alice",
        last_name="Smith",
        role=UserRole.OPERATOR,
    )


class TestCreateUserUseCase:
    def test_execute_happy_path(self, use_case, user_write_adapter, response_dto):
        # Given
        dto = UserCreateDto(
            email="new@example.com",
            first_name="Alice",
            last_name="Smith",
            password="securepass",
        )
        user_write_adapter.save.return_value = response_dto

        with patch(
            "app.module.user.application.use_cases.create_user_use_case.EncryptService.hash",
            return_value="hashed_securepass",
        ):
            # When
            result = use_case.execute(dto)

        # Then
        assert result.id == 1
        assert result.email == "new@example.com"
        assert dto.password == "hashed_securepass"
        user_write_adapter.save.assert_called_once_with(dto)
