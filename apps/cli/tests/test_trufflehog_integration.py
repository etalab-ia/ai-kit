"""Integration test for TruffleHog secret detection.

This test verifies that TruffleHog can detect secrets in files,
including both verified and unverified secrets.
"""

import subprocess
import tempfile
from pathlib import Path


def test_trufflehog_detects_unverified_secrets():
    """Test that TruffleHog detects unverified secrets in a test file."""
    # Create a temporary file with fake secrets
    test_content = '''"""Test file with fake secrets."""

# GitHub Personal Access Token (fake but realistic format)
github_token = "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"

# Slack Webhook URL
slack_webhook = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXX"

# Generic API Key
api_key = "sk-proj-1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOP"
'''

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(test_content)
        test_file = Path(f.name)

    try:
        # Run TruffleHog on the test file (without --results filter to catch all)
        result = subprocess.run(
            ["trufflehog", "filesystem", str(test_file), "--json", "--no-verification"],
            capture_output=True,
            text=True,
        )

        # Check that TruffleHog found at least one secret
        # We expect unverified secrets to be detected
        assert "github" in result.stdout.lower() or "DetectorName" in result.stdout, (
            "TruffleHog should detect the GitHub token in the test file"
        )

        # Verify the output contains secret detection information
        assert result.stdout.strip(), "TruffleHog should produce output for detected secrets"

    finally:
        # Clean up
        test_file.unlink()


def test_trufflehog_available():
    """Test that TruffleHog is installed and accessible."""
    result = subprocess.run(
        ["trufflehog", "--version"],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, "TruffleHog should be installed"
    assert "trufflehog" in result.stdout.lower(), "TruffleHog version should be displayed"


if __name__ == "__main__":
    # Run tests manually
    print("Testing TruffleHog availability...")
    test_trufflehog_available()
    print("✓ TruffleHog is available")

    print("\nTesting TruffleHog secret detection...")
    test_trufflehog_detects_unverified_secrets()
    print("✓ TruffleHog detects secrets correctly")

    print("\n✅ All TruffleHog integration tests passed!")
