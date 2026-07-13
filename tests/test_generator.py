import sys
import os
import string

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from generator import generate_password


def test_default_length():
    password = generate_password()
    assert len(password) == 16


def test_custom_length():
    password = generate_password(length=24)
    assert len(password) == 24


def test_contains_all_character_types_by_default():
    password = generate_password(length=20)
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in string.digits for c in password)
    assert any(c not in string.ascii_letters + string.digits for c in password)


def test_only_digits():
    password = generate_password(
        length=10, use_upper=False, use_lower=False, use_special=False
    )
    assert all(c in string.digits for c in password)


def test_too_short_raises_error():
    with pytest.raises(ValueError):
        generate_password(length=2)


def test_no_character_types_raises_error():
    with pytest.raises(ValueError):
        generate_password(
            use_upper=False, use_lower=False, use_digits=False, use_special=False
        )


def test_passwords_are_random():
    passwords = {generate_password() for _ in range(20)}
    assert len(passwords) == 20