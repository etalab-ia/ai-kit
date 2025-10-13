# CI Troubleshooting Guide

Common CI issues and how to resolve them.

## Table of Contents

- [Linting Failures](#linting-failures)
- [Formatting Issues](#formatting-issues)
- [Test Failures](#test-failures)
- [Undeclared Dependencies](#undeclared-dependencies)
- [Cache Issues](#cache-issues)
- [Environment Differences](#environment-differences)

## Linting Failures

### Symptom
```
error: Failed to run ruff check
src/module.py:10:1: F401 [*] `os` imported but unused
```

### Cause
Code doesn't pass ruff linting checks.

### Solution
```bash
# Run linting locally
just lint

# Auto-fix issues
uv run ruff check --fix .

# Check what will be fixed
uv run ruff check --diff .
```

### Prevention
- Install pre-commit hooks: `uv run pre-commit install`
- Run `just lint` before committing
- Configure IDE to run ruff on save

## Formatting Issues

### Symptom
```
error: 2 files would be reformatted
src/module.py
src/utils.py
```

### Cause
Code doesn't match ruff formatting standards.

### Solution
```bash
# Format all code
just format

# Check formatting without changes
uv run ruff format --check .

# Format specific file
uv run ruff format src/module.py
```

### Prevention
- Run `just format` before committing
- Enable format-on-save in your IDE
- Pre-commit hooks will auto-format

## Test Failures

### Symptom
```
FAILED tests/test_core.py::test_hello - AssertionError: assert 'Hello, Alice!' == 'Hi, Alice!'
```

### Cause
Test assertions don't match actual behavior.

### Solutions

#### Run tests locally
```bash
# All tests
just test

# Specific package
uv run --package ai-kit-core pytest packages/core/tests/

# Specific test
uv run pytest packages/core/tests/test_core.py::test_hello

# With verbose output
uv run pytest -v

# With print statements
uv run pytest -s
```

#### Debug failing test
```python
# Add print statements
def test_hello():
    result = hello("Alice")
    print(f"Result: {result}")  # Debug output
    assert result == "Hello, Alice!"
```

#### Check test isolation
```bash
# Run tests in random order
uv run pytest --random-order

# Run specific test multiple times
uv run pytest --count=10 tests/test_core.py::test_hello
```

### Prevention
- Write tests before code (TDD)
- Run tests locally before pushing
- Use descriptive test names
- Keep tests independent

## Undeclared Dependencies

### Symptom
```
error: Failed to sync package ai-kit-cli
ModuleNotFoundError: No module named 'requests'
```

### Cause
Package imports a module not declared in `pyproject.toml`.

CI uses **strict package isolation** (`uv sync --package <name>`), which only installs declared dependencies.

### Solution

#### 1. Identify the missing dependency
Check the import statement:
```python
import requests  # This needs to be in pyproject.toml
```

#### 2. Add to pyproject.toml
```toml
[project]
dependencies = [
    "requests>=2.31.0",
]
```

#### 3. For workspace dependencies
```toml
[project]
dependencies = [
    "ai-kit-core",
]

[tool.uv.sources]
ai-kit-core = { workspace = true }
```

#### 4. Sync and test
```bash
# Sync with strict isolation (like CI)
uv sync --package ai-kit-cli

# Test the package
uv run --package ai-kit-cli pytest apps/cli/tests/
```

### Prevention
- Test with strict isolation locally:
  ```bash
  uv sync --package <your-package>
  ```
- Declare all imports in `pyproject.toml`
- Review dependency changes in PRs

## Cache Issues

### Symptom
- Turborepo not using cache
- Slow CI runs despite no changes
- "cache miss" for unchanged code

### Solutions

#### Clear Turborepo cache
```bash
# Local
rm -rf .turbo
pnpm turbo run build --force

# CI: Push a commit to clear cache
```

#### Verify cache configuration
Check `turbo.json`:
```json
{
  "tasks": {
    "lint": {
      "cache": true,
      "inputs": ["**/*.py", "pyproject.toml"]
    }
  }
}
```

#### Check cache keys
In GitHub Actions logs, look for:
```
Cache restored from key: Linux-turbo-abc123
```

### Prevention
- Don't modify files during tasks
- Include all relevant files in `inputs`
- Use deterministic commands

## Environment Differences

### Symptom
- Tests pass locally but fail in CI
- "Works on my machine"
- Platform-specific failures

### Common Causes & Solutions

#### 1. Python version mismatch
```bash
# Check local version
uv python list | grep "3.12"

# CI uses version from .python-version
cat .python-version  # Should be 3.12.10
```

#### 2. Dependency version mismatch
```bash
# Sync exact versions from lockfile
uv sync

# Check for version conflicts
uv pip list
```

#### 3. Path separators (Windows vs Unix)
```python
# Bad
path = "src/module.py"

# Good
from pathlib import Path
path = Path("src") / "module.py"
```

#### 4. Line endings (CRLF vs LF)
```bash
# Configure git to use LF
git config --global core.autocrlf input

# Fix existing files
uv run pre-commit run --all-files
```

#### 5. Missing system dependencies
```yaml
# In .github/workflows/ci.yml
- name: Install system dependencies
  run: sudo apt-get update && sudo apt-get install -y libfoo-dev
```

### Prevention
- Use `.python-version` for consistency
- Commit lockfiles (`uv.lock`, `pnpm-lock.yaml`)
- Use `Path` for file paths
- Configure git line endings
- Test in Docker locally:
  ```bash
  docker run -it --rm -v $(pwd):/app python:3.12 bash
  cd /app && just test
  ```

## General Debugging Steps

### 1. Reproduce Locally
```bash
# Use same commands as CI
uv sync --package <package-name>
uv run --package <package-name> pytest
```

### 2. Check CI Logs
- Click on failed job in GitHub Actions
- Expand failed step
- Look for error message
- Check which files caused failure

### 3. Compare Environments
```bash
# Local
uv python list
uv pip list

# CI (from logs)
# Look for "Set up Python" and "Install dependencies" steps
```

### 4. Incremental Debugging
```bash
# Test one thing at a time
just lint          # Does linting pass?
just format        # Does formatting pass?
just test          # Do tests pass?
uv build           # Does build work?
```

### 5. Ask for Help
If stuck, create an issue with:
- Link to failed CI run
- Error message
- Steps to reproduce
- What you've tried

## Quick Reference

| Issue | Quick Fix |
|-------|-----------|
| Lint failures | `just lint` then `uv run ruff check --fix .` |
| Format issues | `just format` |
| Test failures | `just test` with `-v` flag |
| Missing dependency | Add to `pyproject.toml` |
| Cache problems | `rm -rf .turbo` |
| Environment mismatch | `uv sync` and check `.python-version` |

## Related Documentation

- [CI Testing Guide](../.github/CI_TESTING.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Turborepo Guide](../TURBOREPO.md)
