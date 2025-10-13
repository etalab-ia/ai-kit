# Contributing to ai-kit

Thank you for contributing to ai-kit! This guide will help you get started.

## Table of Contents

- [Environment Setup](#environment-setup)
- [Code Quality](#code-quality)
- [Testing](#testing)
- [Pull Request Process](#pull-request-process)
- [Monorepo Guidelines](#monorepo-guidelines)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)
- [Getting Help](#getting-help)

## Environment Setup

### Prerequisites

Install the following tools:

1. **uv** - Python package manager
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **just** - Command runner
   ```bash
   # macOS
   brew install just
   
   # Linux
   curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to ~/bin
   ```

3. **Volta** - Node.js version manager
   ```bash
   curl https://get.volta.sh | bash
   ```

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/your-org/ai-kit.git
cd ai-kit

# Run automated setup
just setup

# Verify everything works
just lint
just test
```

**Setup time**: Should complete in <10 minutes

## Code Quality

### Linting and Formatting

We use **ruff** for both linting and formatting:

```bash
# Run linting
just lint

# Auto-fix linting issues
uv run ruff check --fix .

# Format code
just format

# Check formatting without changes
uv run ruff format --check .
```

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit:

```bash
# Manually run pre-commit on all files
uv run pre-commit run --all-files

# Skip hooks (NOT recommended)
git commit --no-verify
```

**Note**: CI will catch skipped hooks, so it's better to fix issues locally.

### Code Style

- **Line length**: 100 characters
- **Python version**: 3.12+ features allowed
- **Type hints**: Required for public APIs
- **Docstrings**: Required for all public functions/classes (Google style)

Example:
```python
def hello(name: str = "World") -> str:
    """Return a greeting message.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A greeting message.

    Examples:
        >>> hello()
        'Hello, World!'
        >>> hello("Alice")
        'Hello, Alice!'
    """
    return f"Hello, {name}!"
```

## Testing

### Running Tests

```bash
# Run all tests
just test

# Run tests for specific package
uv run --package ai-kit-core pytest packages/core/tests/

# Run with coverage
uv run pytest --cov=src --cov-report=html
```

### Writing Tests

- Place tests in `tests/` directory
- Name test files `test_*.py`
- Name test functions `test_*`
- Use descriptive test names
- Aim for >80% coverage

Example:
```python
def test_hello_with_custom_name():
    """Test hello function with custom name."""
    result = hello("Alice")
    assert result == "Hello, Alice!"
```

## Pull Request Process

### 1. Create a Branch

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Create bugfix branch
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write code following our style guide
- Add tests for new functionality
- Update documentation as needed
- Run `just lint` and `just test` before committing

### 3. Commit Changes

```bash
# Stage changes
git add .

# Commit (pre-commit hooks will run)
git commit -m "feat: add new feature"
```

**Commit Message Format**:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

### 4. Push and Create PR

```bash
# Push to your fork
git push origin feature/your-feature-name

# Create PR on GitHub
# - Fill in the PR template
# - Link related issues
# - Request reviews
```

### 5. CI Checks

All PRs must pass:
- ✅ Linting (ruff check)
- ✅ Formatting (ruff format --check)
- ✅ Tests (pytest)
- ✅ Build (uv build)
- ✅ Pre-commit hooks

## Monorepo Guidelines

### Adding a New Package

#### Library Package (packages/)

```bash
# Create package structure
mkdir -p packages/my-package/src/ai_kit_my_package packages/my-package/tests

# Create pyproject.toml
cat > packages/my-package/pyproject.toml <<EOF
[project]
name = "ai-kit-my-package"
version = "0.1.0"
description = "Description of my package"
requires-python = ">=3.12"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
EOF

# Create package.json for Turborepo
cat > packages/my-package/package.json <<EOF
{
  "name": "@ai-kit/my-package",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "lint": "uv run ruff check src/",
    "format": "uv run ruff format src/",
    "test": "uv run pytest",
    "build": "uv build"
  }
}
EOF

# Sync workspace
uv sync --all-packages
```

#### Application (apps/)

Same structure as library, but add entry point in `pyproject.toml`:

```toml
[project.scripts]
my-cli = "ai_kit_my_app.main:main"
```

### Package Dependencies

#### Workspace Dependencies

To depend on another workspace package:

```toml
# In apps/cli/pyproject.toml
[project]
dependencies = [
    "ai-kit-core",
]

[tool.uv.sources]
ai-kit-core = { workspace = true }
```

#### External Dependencies

```toml
[project]
dependencies = [
    "requests>=2.31.0",
    "pydantic>=2.0.0",
]
```

### Turborepo Tasks

Tasks are defined in `turbo.json` and run via `pnpm turbo`:

```bash
# Run lint across all packages (parallel)
pnpm lint

# Run tests (respects dependencies)
pnpm test

# Build all packages
pnpm build
```

## Common Tasks

### Update Dependencies

```bash
# Update Python dependencies
uv sync --upgrade

# Update Node.js dependencies
pnpm update

# Update pre-commit hooks
uv run pre-commit autoupdate
```

### Clear Caches

```bash
# Clear all caches and artifacts
just clean

# Clear Turborepo cache only
rm -rf .turbo

# Clear uv cache
uv cache clean
```

### Run Specific Package

```bash
# Run CLI app
uv run --package ai-kit-cli ai-kit

# Run tests for specific package
uv run --package ai-kit-core pytest packages/core/tests/
```

## Troubleshooting

### "Command not found: uv/just/volta"

**Solution**: Install the missing tool (see [Prerequisites](#prerequisites))

### "Module not found" errors

**Solution**: Sync dependencies
```bash
uv sync --all-packages
```

### Pre-commit hooks failing

**Solution**: Run hooks manually and fix issues
```bash
uv run pre-commit run --all-files
just format
just lint
```

### CI failing but tests pass locally

**Possible causes**:
1. **Undeclared dependency**: CI uses strict package isolation
   - **Fix**: Add missing dependency to `pyproject.toml`
2. **Formatting differences**: Different ruff version
   - **Fix**: Run `uv sync` to match versions
3. **Platform differences**: macOS vs Linux
   - **Fix**: Test in Docker or check CI logs

### Turborepo cache issues

**Solution**: Clear cache and rebuild
```bash
rm -rf .turbo
pnpm build --force
```

### Import errors in workspace packages

**Solution**: Ensure workspace dependency is declared
```toml
[tool.uv.sources]
ai-kit-core = { workspace = true }
```

## Getting Help

- **Documentation**: Check [specs/](./specs/) for detailed guides
- **Issues**: Search [existing issues](https://github.com/your-org/ai-kit/issues)
- **Discussions**: Ask in [GitHub Discussions](https://github.com/your-org/ai-kit/discussions)
- **CI Troubleshooting**: See [.github/CI_TESTING.md](./.github/CI_TESTING.md)

## Code of Conduct

Be respectful, inclusive, and professional. We follow the [Contributor Covenant](https://www.contributor-covenant.org/).

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
