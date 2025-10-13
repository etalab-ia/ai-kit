"""Tests for ai-kit core library."""

from ai_kit_core import hello


def test_hello_default():
    """Test hello with default argument."""
    assert hello() == "Hello, World!"


def test_hello_with_name():
    """Test hello with custom name."""
    assert hello("Alice") == "Hello, Alice!"
