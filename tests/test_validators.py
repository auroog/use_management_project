import pytest
from app.utils.validators import validate_email_address


# Test for a valid email
def test_valid_email():
    """Test a valid email address."""
    assert validate_email_address("test@example.com") is True


# Test for an invalid email
def test_invalid_email():
    """Test an invalid email address."""
    assert validate_email_address("not@valid") is False


# Test for another invalid email example
def test_empty_email():
    """Test an empty email address."""
    assert validate_email_address("") is False


# Test for edge-case: missing domain
def test_missing_domain():
    """Test email missing a domain."""
    assert validate_email_address("user@.com") is False
