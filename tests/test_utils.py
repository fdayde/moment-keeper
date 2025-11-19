"""Tests pour les utilitaires."""

from moment_keeper.utils import extract_month_number


def test_extract_month_number_single_digit():
    """Test extraction avec un chiffre."""
    assert extract_month_number("0-1months") == 0
    assert extract_month_number("5-6months") == 5
    assert extract_month_number("9-10months") == 9


def test_extract_month_number_double_digit():
    """Test extraction avec deux chiffres."""
    assert extract_month_number("10-11months") == 10
    assert extract_month_number("12-13months") == 12
    assert extract_month_number("23-24months") == 23


def test_extract_month_number_invalid():
    """Test extraction avec format invalide."""
    assert extract_month_number("invalid") == 999
    assert extract_month_number("") == 999
    assert extract_month_number("months") == 999
    assert extract_month_number("abc-def") == 999
