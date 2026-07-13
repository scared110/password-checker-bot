import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from checker import analyze_password


def test_common_password_is_weak():
    result = analyze_password("123456")
    assert result["is_common"] is True
    assert result["score"] == 0


def test_short_password_is_weak():
    result = analyze_password("ab1")
    assert result["score"] <= 1


def test_strong_password():
    result = analyze_password("Kx9#mP2$vL8@qR5!")
    assert result["has_upper"] is True
    assert result["has_lower"] is True
    assert result["has_digit"] is True
    assert result["has_special"] is True
    assert result["score"] >= 3


def test_entropy_increases_with_length():
    short = analyze_password("Abc123!")
    long = analyze_password("Abc123!Abc123!Abc")
    assert long["entropy"] > short["entropy"]


def test_tips_are_generated_for_weak_password():
    result = analyze_password("abc")
    assert len(result["tips"]) > 0