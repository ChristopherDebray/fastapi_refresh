import pytest
from jose import JWTError

from app.core.security.jwt_service import JwtService
from app.core.security.token_payload import CreateAccessTokenDto, CreateRefreshTokenDto, RefreshTokenPayloadDto, TokenPayloadDto
from app.module.user.domain.enums import UserRole


def make_token_dto(**kwargs) -> CreateAccessTokenDto:
    defaults = {
        "user_id": 1,
        "email": "user@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": UserRole.ADMIN,
    }
    return CreateAccessTokenDto(**{**defaults, **kwargs})


class TestJwtServiceCreateAccessToken:
    def test_returns_non_empty_string(self):
        # Given / When
        token = JwtService.create_access_token(make_token_dto())

        # Then
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_has_three_jwt_segments(self):
        # Given / When
        token = JwtService.create_access_token(make_token_dto())

        # Then
        assert token.count(".") == 2


class TestJwtServiceDecodeAccessToken:
    def test_decode_returns_correct_payload(self):
        # Given
        token = JwtService.create_access_token(make_token_dto(user_id=42, role=UserRole.DRIVER))

        # When
        payload = JwtService.decode_access_token(token)

        # Then
        assert isinstance(payload, TokenPayloadDto)
        assert payload.sub == 42
        assert payload.email == "user@example.com"
        assert payload.role == UserRole.DRIVER

    def test_decode_preserves_all_roles(self):
        for role in UserRole:
            # Given
            token = JwtService.create_access_token(make_token_dto(user_id=1, role=role))

            # When
            payload = JwtService.decode_access_token(token)

            # Then
            assert payload.role == role
            assert payload.email == "user@example.com"
            assert payload.sub == 1

    def test_raises_on_invalid_token(self):
        # Given
        invalid_token = "not.a.token"

        # When / Then
        with pytest.raises(JWTError):
            JwtService.decode_access_token(invalid_token)

    def test_raises_on_tampered_token(self):
        # Given
        token = JwtService.create_access_token(make_token_dto())
        tampered = token[:-5] + "XXXXX"

        # When / Then
        with pytest.raises(JWTError):
            JwtService.decode_access_token(tampered)


def make_refresh_token_dto(**kwargs) -> CreateRefreshTokenDto:
    defaults = {
        "user_id": 1,
        "email": "user@example.com",
    }
    return CreateRefreshTokenDto(**{**defaults, **kwargs})


class TestJwtServiceCreateRefreshToken:
    def test_returns_non_empty_string(self):
        # Given / When
        token = JwtService.create_refresh_token(make_refresh_token_dto())

        # Then
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_has_three_jwt_segments(self):
        # Given / When
        token = JwtService.create_refresh_token(make_refresh_token_dto())

        # Then
        assert token.count(".") == 2


class TestJwtServiceDecodeRefreshToken:
    def test_decode_returns_correct_payload(self):
        # Given
        token = JwtService.create_refresh_token(make_refresh_token_dto(user_id=99))

        # When
        payload = JwtService.decode_refresh_token(token)

        # Then
        assert isinstance(payload, RefreshTokenPayloadDto)
        assert payload.user_id == 99
        assert payload.email == "user@example.com"

    def test_raises_on_invalid_token(self):
        # Given
        invalid_token = "not.a.token"

        # When / Then
        with pytest.raises(JWTError):
            JwtService.decode_refresh_token(invalid_token)

    def test_raises_on_tampered_token(self):
        # Given
        token = JwtService.create_refresh_token(make_refresh_token_dto())
        tampered = token[:-5] + "XXXXX"

        # When / Then
        with pytest.raises(JWTError):
            JwtService.decode_refresh_token(tampered)
