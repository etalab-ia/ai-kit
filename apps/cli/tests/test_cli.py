"""Tests for ai-kit CLI."""

from ai_kit_cli.main import main


def test_main_returns_zero():
    """Test that main returns 0 (success)."""
    assert main() == 0
