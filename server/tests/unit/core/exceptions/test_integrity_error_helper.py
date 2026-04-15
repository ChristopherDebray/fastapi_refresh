from unittest.mock import MagicMock
from sqlalchemy.exc import IntegrityError

from app.core.exceptions.integrity_error_helper import extract_field_from_integrity_error


def _make_error(orig_message: str) -> IntegrityError:
    orig = MagicMock()
    orig.__str__ = lambda self: orig_message
    return IntegrityError(statement=None, params=None, orig=orig)


class TestExtractFieldFromIntegrityError:
    def test_extracts_field_name_from_standard_psycopg2_message(self):
        # Given
        error = _make_error('DETAIL:  Key (email)=(test@example.com) already exists.')

        # When
        result = extract_field_from_integrity_error(error)

        # Then
        assert result == "email"

    def test_extracts_field_name_with_underscore(self):
        # Given
        error = _make_error('DETAIL:  Key (user_name)=(john_doe) already exists.')

        # When
        result = extract_field_from_integrity_error(error)

        # Then
        assert result == "user_name"

    def test_returns_unknown_when_no_key_pattern(self):
        # Given
        error = _make_error('some generic database error without key info')

        # When
        result = extract_field_from_integrity_error(error)

        # Then
        assert result == "unknown"

    def test_returns_unknown_on_empty_message(self):
        # Given
        error = _make_error('')

        # When
        result = extract_field_from_integrity_error(error)

        # Then
        assert result == "unknown"
