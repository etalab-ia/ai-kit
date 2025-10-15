"""Tests for git utilities."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from ai_kit.cli.utils.git import (
    create_git_tag,
    get_current_commit_sha,
    get_file_last_commit_sha,
    get_git_user_name,
    list_git_tags,
)


class TestGetGitUserName:
    """Test getting git user name."""

    @patch("subprocess.run")
    def test_get_user_name_success(self, mock_run):
        """Test successfully getting git user name."""
        mock_run.return_value = MagicMock(returncode=0, stdout="John Doe\n")

        result = get_git_user_name()

        assert result == "John Doe"
        mock_run.assert_called_once_with(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=False,
        )

    @patch("subprocess.run")
    def test_get_user_name_not_configured(self, mock_run):
        """Test when git user name is not configured."""
        mock_run.return_value = MagicMock(returncode=1, stdout="")

        result = get_git_user_name()

        assert result is None

    @patch("subprocess.run")
    def test_get_user_name_git_not_found(self, mock_run):
        """Test when git is not installed."""
        mock_run.side_effect = FileNotFoundError()

        result = get_git_user_name()

        assert result is None


class TestCreateGitTag:
    """Test creating git tags."""

    @patch("subprocess.run")
    def test_create_tag_success(self, mock_run):
        """Test successfully creating a git tag."""
        mock_run.return_value = MagicMock(returncode=0)

        result = create_git_tag("v1.0.0", "Release version 1.0.0")

        assert result is True
        mock_run.assert_called_once_with(
            ["git", "tag", "-a", "v1.0.0", "-m", "Release version 1.0.0"],
            cwd=None,
            check=True,
            capture_output=True,
        )

    @patch("subprocess.run")
    def test_create_tag_with_cwd(self, mock_run):
        """Test creating tag with custom working directory."""
        mock_run.return_value = MagicMock(returncode=0)
        cwd = Path("/path/to/repo")

        result = create_git_tag("v1.0.0", "Release", cwd=cwd)

        assert result is True
        assert mock_run.call_args[1]["cwd"] == cwd

    @patch("subprocess.run")
    def test_create_tag_failure(self, mock_run):
        """Test failure when creating git tag."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git tag")

        result = create_git_tag("v1.0.0", "Release")

        assert result is False


class TestListGitTags:
    """Test listing git tags."""

    @patch("subprocess.run")
    def test_list_all_tags(self, mock_run):
        """Test listing all git tags."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="v1.0.0\nv1.1.0\nv2.0.0\n",
        )

        result = list_git_tags()

        assert result == ["v1.0.0", "v1.1.0", "v2.0.0"]
        mock_run.assert_called_once_with(
            ["git", "tag", "--list"],
            cwd=None,
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_list_tags_with_pattern(self, mock_run):
        """Test listing tags with pattern filter."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="compliance/model-v1.0-2024-10-15\ncompliance/model-v1.1-2024-10-20\n",
        )

        result = list_git_tags("compliance/*")

        assert len(result) == 2
        assert "compliance/model-v1.0-2024-10-15" in result
        mock_run.assert_called_once()
        assert "compliance/*" in mock_run.call_args[0][0]

    @patch("subprocess.run")
    def test_list_tags_empty(self, mock_run):
        """Test listing tags when none exist."""
        mock_run.return_value = MagicMock(returncode=0, stdout="")

        result = list_git_tags()

        assert result == []

    @patch("subprocess.run")
    def test_list_tags_failure(self, mock_run):
        """Test failure when listing tags."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git tag")

        result = list_git_tags()

        assert result == []


class TestGetCurrentCommitSha:
    """Test getting current commit SHA."""

    @patch("subprocess.run")
    def test_get_commit_sha_success(self, mock_run):
        """Test successfully getting commit SHA."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="abc123def456\n",
        )

        result = get_current_commit_sha()

        assert result == "abc123def456"
        mock_run.assert_called_once_with(
            ["git", "rev-parse", "HEAD"],
            cwd=None,
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_get_commit_sha_with_cwd(self, mock_run):
        """Test getting commit SHA with custom working directory."""
        mock_run.return_value = MagicMock(returncode=0, stdout="abc123\n")
        cwd = Path("/path/to/repo")

        result = get_current_commit_sha(cwd=cwd)

        assert result == "abc123"
        assert mock_run.call_args[1]["cwd"] == cwd

    @patch("subprocess.run")
    def test_get_commit_sha_failure(self, mock_run):
        """Test failure when getting commit SHA."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git rev-parse")

        with pytest.raises(RuntimeError, match="Failed to get current commit SHA"):
            get_current_commit_sha()


class TestGetFileLastCommitSha:
    """Test getting file's last commit SHA."""

    @patch("subprocess.run")
    def test_get_file_commit_sha_success(self, mock_run):
        """Test successfully getting file's last commit SHA."""
        mock_run.return_value = MagicMock(returncode=0, stdout="def789ghi012\n")
        file_path = Path("notebooks/test.ipynb")

        result = get_file_last_commit_sha(file_path)

        assert result == "def789ghi012"
        mock_run.assert_called_once()
        assert str(file_path) in mock_run.call_args[0][0]

    @patch("subprocess.run")
    def test_get_file_commit_sha_with_cwd(self, mock_run):
        """Test getting file commit SHA with custom working directory."""
        mock_run.return_value = MagicMock(returncode=0, stdout="abc123\n")
        file_path = Path("test.ipynb")
        cwd = Path("/path/to/repo")

        result = get_file_last_commit_sha(file_path, cwd=cwd)

        assert result == "abc123"
        assert mock_run.call_args[1]["cwd"] == cwd

    @patch("subprocess.run")
    def test_get_file_commit_sha_failure(self, mock_run):
        """Test failure when getting file commit SHA."""
        mock_run.side_effect = subprocess.CalledProcessError(1, "git log")
        file_path = Path("nonexistent.ipynb")

        with pytest.raises(RuntimeError, match="Failed to get file commit SHA"):
            get_file_last_commit_sha(file_path)
