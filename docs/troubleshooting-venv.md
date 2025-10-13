# Virtual Environment Troubleshooting

Common issues with the shared `.venv` and how to resolve them.

## Table of Contents

- [Conflicting Dependencies](#conflicting-dependencies)
- [Import Errors](#import-errors)
- [Version Conflicts](#version-conflicts)
- [Corrupted .venv](#corrupted-venv)
- [Platform Issues](#platform-issues)

## Conflicting Dependencies

### Symptom
```
error: Failed to resolve dependencies
Package A requires foo>=2.0
Package B requires foo<2.0
```

### Cause
Two packages in the workspace have incompatible dependency requirements.

### Solution

#### 1. Check dependency versions
```bash
# List all dependencies
uv pip list | grep foo

# Check which packages depend on foo
uv pip show foo
```

#### 2. Align versions in pyproject.toml
```toml
# packages/package-a/pyproject.toml
[project]
dependencies = [
    "foo>=2.0,<3.0",  # More specific range
]

# packages/package-b/pyproject.toml
[project]
dependencies = [
    "foo>=2.0,<3.0",  # Match the range
]
```

#### 3. Re-sync
```bash
uv sync --all-packages
```

### Prevention
- Use compatible version ranges
- Test dependency changes across all packages
- Use `uv lock` to verify resolution

## Import Errors

### Undeclared Dependencies in Shared .venv

**Critical Edge Case**: Package imports a module available in shared `.venv` but not declared in its own `pyproject.toml`.

#### Symptom
```python
# In packages/my-package/src/my_package/module.py
import requests  # Works locally, fails in CI

# Error in CI:
ModuleNotFoundError: No module named 'requests'
```

#### Cause
- Locally: `requests` is in shared `.venv` (installed by another package)
- CI: Strict isolation (`uv sync --package my-package`) only installs declared deps

#### Solution

**1. Identify the undeclared import**
```bash
# Check what's importing requests
grep -r "import requests" packages/my-package/src/
```

**2. Add to pyproject.toml**
```toml
# packages/my-package/pyproject.toml
[project]
dependencies = [
    "requests>=2.31.0",
]
```

**3. Test with strict isolation (like CI)**
```bash
# Remove .venv to start fresh
rm -rf .venv

# Sync only this package
uv sync --package my-package

# Try to run/test
uv run --package my-package pytest
```

#### Prevention
- Always test with `uv sync --package <name>` before pushing
- CI uses strict isolation by default (catches this)
- Review imports when adding new code

### Module Not Found After Sync

#### Symptom
```python
ModuleNotFoundError: No module named 'ai_kit_core'
```

#### Cause
Package not installed or workspace dependency not configured.

#### Solution

**1. Check workspace dependency**
```toml
# apps/cli/pyproject.toml
[project]
dependencies = [
    "ai-kit-core",
]

[tool.uv.sources]
ai-kit-core = { workspace = true }  # Required!
```

**2. Re-sync**
```bash
uv sync --all-packages
```

**3. Verify installation**
```bash
uv pip list | grep ai-kit
```

## Version Conflicts

### Symptom
```
error: Package foo==2.0.0 conflicts with foo==1.5.0
```

### Cause
Multiple packages pin different versions of the same dependency.

### Solution

#### 1. Find conflicting packages
```bash
uv pip show foo
```

#### 2. Use version ranges instead of pins
```toml
# Bad
dependencies = ["foo==2.0.0"]

# Good
dependencies = ["foo>=2.0.0,<3.0.0"]
```

#### 3. Update lockfile
```bash
uv lock --upgrade
uv sync
```

### Prevention
- Use version ranges, not exact pins
- Keep dependencies up to date
- Test upgrades across all packages

## Corrupted .venv

### Symptom
- Import errors for installed packages
- Unexpected behavior
- `uv sync` fails with strange errors

### Cause
- Interrupted installation
- Manual file modifications
- Disk corruption

### Solution

#### 1. Remove and recreate
```bash
# Remove corrupted .venv
rm -rf .venv

# Recreate from scratch
uv sync --all-packages

# Verify
just test
```

#### 2. Clear uv cache (if issues persist)
```bash
uv cache clean
uv sync --all-packages
```

#### 3. Check disk space
```bash
df -h .
```

### Recovery Steps
```bash
# Full cleanup
just clean

# Recreate everything
uv sync --all-packages
pnpm install

# Verify
just test
```

### Prevention
- Don't manually modify `.venv/`
- Ensure adequate disk space
- Use `uv sync` for all changes

## Platform Issues

### Binary Dependencies

#### Symptom
```
error: Failed to build package
gcc: command not found
```

#### Cause
Python package with C extensions requires compilation tools.

#### Solution

**macOS**:
```bash
xcode-select --install
```

**Linux (Ubuntu/Debian)**:
```bash
sudo apt-get install python3-dev build-essential
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install python3-devel gcc
```

**Windows**:
- Install Visual Studio Build Tools
- Or use pre-built wheels

#### Prevention
- Document system dependencies in README
- Use packages with pre-built wheels when possible
- Test on target platforms

### Platform-Specific Paths

#### Symptom
```python
# Works on macOS/Linux, fails on Windows
path = "src/module.py"
```

#### Cause
Hard-coded path separators.

#### Solution
```python
# Use pathlib
from pathlib import Path

path = Path("src") / "module.py"
```

### Line Endings (Windows)

#### Symptom
Pre-commit hooks fail on Windows with CRLF line endings.

#### Cause
Git converts LF to CRLF on Windows.

#### Solution
```bash
# Configure git
git config --global core.autocrlf input
git config --global core.eol lf

# Fix existing files
uv run pre-commit run --all-files
```

## Debugging Checklist

When encountering .venv issues:

1. **Check installation**
   ```bash
   uv pip list
   ```

2. **Verify package location**
   ```bash
   uv pip show <package-name>
   ```

3. **Test strict isolation**
   ```bash
   uv sync --package <package-name>
   ```

4. **Check for conflicts**
   ```bash
   uv pip check
   ```

5. **Recreate if needed**
   ```bash
   rm -rf .venv
   uv sync --all-packages
   ```

## Best Practices

### Do
- ✅ Use version ranges in dependencies
- ✅ Declare all imports in pyproject.toml
- ✅ Test with strict isolation before pushing
- ✅ Keep dependencies up to date
- ✅ Use `uv sync` for all changes

### Don't
- ❌ Manually modify .venv/
- ❌ Pin exact versions unless necessary
- ❌ Import without declaring
- ❌ Assume local = CI
- ❌ Ignore import errors

## Related Documentation

- [CI Troubleshooting](./troubleshooting-ci.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Platform-Specific Setup](./setup-platform-specific.md)
