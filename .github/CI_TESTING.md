# CI Testing Guide

This document describes how to test CI failures to ensure the pipeline catches issues correctly.

## Test Scenarios

### 1. Test Lint Violations

**Create a lint violation:**
```python
# In packages/core/src/ai_kit_core/__init__.py
import os  # Unused import - should fail ruff check
```

**Expected**: CI lint job should fail with ruff error

**Cleanup**: Remove the unused import

### 2. Test Format Issues

**Create a format issue:**
```python
# In packages/core/src/ai_kit_core/__init__.py
def hello(name: str = "World") -> str:
    return f"Hello, {name}!"  # Remove proper spacing
```

**Expected**: CI format-check job should fail

**Cleanup**: Run `just format` to fix

### 3. Test Failing Tests

**Create a failing test:**
```python
# In packages/core/tests/test_core.py
def test_hello_fail():
    """This test should fail."""
    assert hello() == "Goodbye, World!"  # Wrong expected value
```

**Expected**: CI test job should fail

**Cleanup**: Remove or fix the test

### 4. Test Undeclared Dependencies

**Use undeclared dependency:**
```python
# In apps/cli/src/ai_kit_cli/main.py
import requests  # Not declared in pyproject.toml
```

**Expected**: CI should fail when syncing with strict package isolation

**Cleanup**: Either add `requests` to dependencies or remove the import

### 5. Test Pre-commit Hook Failures

**Create pre-commit violation:**
```bash
# Make a commit with formatting issues
echo "def bad_format( ):pass" >> packages/core/src/ai_kit_core/temp.py
git add .
git commit -m "test: bad format"
```

**Expected**: Pre-commit hooks should block the commit locally

**Cleanup**: Fix formatting or remove the file

## Running Tests Locally

### Test Individual Jobs

```bash
# Test lint
pnpm turbo run lint

# Test format check
pnpm turbo run format

# Test all tests
pnpm turbo run test

# Test build
pnpm turbo run build
```

### Test Strict Package Isolation

```bash
# Test core package isolation
uv sync --package ai-kit-core
uv run --package ai-kit-core pytest packages/core/tests/

# Test CLI package isolation
uv sync --package ai-kit-cli
uv run --package ai-kit-cli pytest apps/cli/tests/
```

## CI Workflow Validation

After pushing changes, verify:

1. ✅ All jobs run in parallel (lint, format-check, test)
2. ✅ Build job waits for other jobs to complete
3. ✅ Turborepo cache is used (check job logs)
4. ✅ Strict package isolation catches undeclared dependencies
5. ✅ Pre-commit workflow runs on PRs
6. ✅ Clear error messages when failures occur

## Success Criteria

- **SC-006**: CI completes in <5 minutes for typical PRs
- **SC-007**: Zero "works on my machine" issues
- **SC-008**: CI catches undeclared dependencies via strict sync
- **FR-020**: CI fails fast on lint/format violations
- **FR-021**: Strict package isolation in ALL jobs
