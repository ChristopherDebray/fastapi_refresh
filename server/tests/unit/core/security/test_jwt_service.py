import pytest
from jose import JWTError

from app.core.security.jwt_service import JwtService
from app.core.security.token_payload import TokenPayloadDto
from app.module.user.domain.enums import UserRole


class TestJwtServiceCreateAccessToken:
    def test_returns_non_empty_string(self):
        # Given / When
        token = JwtService.create_access_token(user_id=1, email="user@example.com", role=UserRole.ADMIN)

        # Then
        assert isinstance(token, str)
        assert len(token) > 0

    def test_token_has_three_jwt_segments(self):
        # Given / When
        token = JwtService.create_access_token(user_id=1, email="user@example.com", role=UserRole.ADMIN)

        # Then
        assert token.count(".") == 2


class TestJwtServiceDecodeAccessToken:
    def test_decode_returns_correct_payload(self):
        # Given
        token = JwtService.create_access_token(user_id=42, email="user@example.com", role=UserRole.DRIVER)

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
            email = "u@example.com"
            id = 1
            token = JwtService.create_access_token(user_id=id, email=email, role=role)

            # When
            payload = JwtService.decode_access_token(token)

            # Then
            assert payload.role == role
            assert payload.email == email
            assert payload.sub == id

    def test_raises_on_invalid_token(self):
        # Given
        invalid_token = "not.a.token"

        # When / Then
        with pytest.raises(JWTError):
            JwtService.decode_access_token(invalid_token)

    def test_raises_on_tampered_token(self):
        # Given
        token = JwtService.create_access_token(user_id=1, email="u@example.com", role=UserRole.ADMIN)
        tampered = token[:-5] + "XXXXX"

        # When / Then
        with pytest.raises(JWTError):
            JwtService.decode_access_token(tampered)
