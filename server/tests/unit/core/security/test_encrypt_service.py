from app.core.security.encrypt_service import EncryptService


class TestEncryptServiceHash:
    def test_returns_hashed_string(self):
        # Given / When
        result = EncryptService.hash("my_password")

        # Then
        assert isinstance(result, str)
        assert result != "my_password"

    def test_hash_starts_with_bcrypt_prefix(self):
        # Given / When
        result = EncryptService.hash("my_password")

        # Then
        assert result.startswith("$2b$")

    def test_two_hashes_of_same_password_differ(self):
        # Given / When
        hash1 = EncryptService.hash("my_password")
        hash2 = EncryptService.hash("my_password")

        # Then
        assert hash1 != hash2


class TestEncryptServiceVerify:
    def test_returns_true_for_correct_password(self):
        # Given
        plain = "my_password"
        hashed = EncryptService.hash(plain)

        # When
        result = EncryptService.verify(plain, hashed)

        # Then
        assert result is True

    def test_returns_false_for_wrong_password(self):
        # Given
        hashed = EncryptService.hash("correct_password")

        # When
        result = EncryptService.verify("wrong_password", hashed)

        # Then
        assert result is False

    def test_returns_false_for_empty_plain_against_real_hash(self):
        # Given
        hashed = EncryptService.hash("some_password")

        # When
        result = EncryptService.verify("", hashed)

        # Then
        assert result is False
