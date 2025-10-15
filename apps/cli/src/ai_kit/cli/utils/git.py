"""Git operations utilities."""

import subprocess
from pathlib import Path


def get_git_user_name() -> str | None:
    """Get git user name from config."""
    try:
        result = subprocess.run(
            ["git", "config", "user.name"],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    return None


def create_git_tag(tag_name: str, message: str, cwd: Path | None = None) -> bool:
    """Create an annotated git tag."""
    try:
        subprocess.run(
            ["git", "tag", "-a", tag_name, "-m", message],
            cwd=cwd,
            check=True,
            capture_output=True,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def list_git_tags(pattern: str | None = None, cwd: Path | None = None) -> list[str]:
    """List git tags, optionally filtered by pattern."""
    try:
        cmd = ["git", "tag", "--list"]
        if pattern:
            cmd.append(pattern)

        result = subprocess.run(
            cmd,
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        return [tag.strip() for tag in result.stdout.split("\n") if tag.strip()]
    except subprocess.CalledProcessError:
        return []


def get_current_commit_sha(cwd: Path | None = None) -> str:
    """Get current git commit SHA.

    Raises:
        RuntimeError: If git command fails
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get current commit SHA: {e}") from e


def get_file_last_commit_sha(file_path: Path, cwd: Path | None = None) -> str:
    """Get the last commit SHA that modified a file.

    Args:
        file_path: Path to the file
        cwd: Working directory for git command

    Returns:
        The commit SHA

    Raises:
        RuntimeError: If git command fails or file not in git
    """
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%H", "--", str(file_path)],
            cwd=cwd,
            check=True,
            capture_output=True,
            text=True,
        )
        sha = result.stdout.strip()
        if not sha:
            raise RuntimeError(f"File not found in git history: {file_path}")
        return sha
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to get file commit SHA: {e}") from e
