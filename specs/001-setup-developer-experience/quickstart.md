# Developer Quickstart Guide: ai-kit

**Last Updated**: 2025-10-13  
**Target Audience**: New contributors to ai-kit  
**Estimated Setup Time**: <10 minutes

## Overview

This guide will help you set up your development environment for ai-kit. The repository uses a **hybrid Python-first monorepo** with modern tooling for optimal developer experience.

## Prerequisites

### Required Software

Before you begin, ensure you have the following installed:

1. **Git** (2.x+)
   ```bash
   git --version
   ```

2. **Python 3.12+**
   ```bash
   python --version  # or python3 --version
   ```
   
   If you don't have Python 3.12+, download from [python.org](https://www.python.org/downloads/) or use your system's package manager.

3. **Node.js 22.x LTS** (for Turborepo)
   - Will be installed via Volta in the setup steps below
   ```bash
   node --version  # Should show v22.x.x (after Volta installation)
   ```

### Required Tools (Install These First)

These tools are **required** for ai-kit development:

1. **Volta** (Node.js version manager - standardized for ai-kit)
   ```bash
   curl https://get.volta.sh | bash
   ```
   
   **Why Volta is required**: It automatically switches Node.js versions when you `cd` between projects. This is critical for government developers working on multiple projects with different Node versions (e.g., legacy Node 16/18/20 projects alongside modern Node 22 projects like ai-kit).

2. **uv** (Python package manager)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **just** (Task runner)
   ```bash
   # macOS
   brew install just
   
   # Linux
   curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin
   
   # Windows (via cargo)
   cargo install just
   ```

## Quick Setup (5 Steps)

### 1. Clone the Repository

```bash
git clone https://github.com/your-org/ai-kit.git
cd ai-kit
```

### 2. Install Node.js 22.x (if using Volta)

```bash
volta install node@22
```

Volta will automatically use Node 22.x whenever you're in the ai-kit directory.

### 3. Enable Corepack (for pnpm management)

```bash
corepack enable
```

This allows Corepack to manage pnpm versions automatically based on the `packageManager` field in `package.json`.

### 4. Run Setup Command

```bash
just setup
```

This single command will:
- Install all Python dependencies via uv (creates `.venv/`)
- Install all Node.js dependencies via pnpm
- Install pre-commit hooks for code quality

### 5. Verify Installation

```bash
just --list
```

You should see all available development commands.

## Development Workflow

### Common Commands

All commands are available via `just`:

```bash
# List all available commands
just --list

# Sync dependencies (after pulling changes)
just sync

# Run linting on all packages
just lint

# Format all Python code
just format

# Run tests on all packages
just test

# Build all packages
just build

# Clean build artifacts
just clean
```

### Working with Packages

The repository is organized as a monorepo:

```
ai-kit/
├── apps/          # Deployable applications (CLI tools, servers)
├── packages/      # Importable libraries (core, templates, configs)
└── .venv/         # Single shared virtual environment
```

**Key concept**: All Python packages share a single `.venv` at the repository root. This is managed automatically by uv.

### Adding Dependencies

#### To a specific package:

```bash
# Navigate to the package
cd packages/core

# Add a dependency
uv add requests

# The dependency is added to packages/core/pyproject.toml
# and installed in the shared .venv
```

#### To the root (shared dependencies):

```bash
# At repository root
uv add --dev pytest pytest-cov
```

### Running Package-Specific Commands

```bash
# Run tests for a specific package
cd packages/core
pytest

# Or use Turborepo to run across all packages
turbo run test
```

### Pre-commit Hooks

Pre-commit hooks run automatically on every commit to ensure code quality:

- **ruff check**: Linting
- **ruff format**: Code formatting

If hooks fail, the commit is blocked. Fix the issues and try again.

**Note**: Pre-commit hooks are **mandatory** and cannot be disabled. This ensures consistent code quality across all contributors.

## Troubleshooting

### Issue: "command not found: uv"

**Solution**: Install uv using the installation script:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal or run:
```bash
source ~/.bashrc  # or ~/.zshrc
```

### Issue: "command not found: just"

**Solution**: Install just using your package manager (see Prerequisites section above).

### Issue: "Python version 3.12+ required"

**Solution**: Install Python 3.12 or higher:
```bash
# macOS (via Homebrew)
brew install python@3.12

# Ubuntu/Debian
sudo apt install python3.12

# Or download from python.org
```

### Issue: "Node.js version mismatch"

**Solution**: Volta should automatically switch to Node 22.x when you enter the ai-kit directory. If you see a version mismatch:

```bash
# Ensure Volta is installed
volta --version

# Install Node 22.x via Volta
volta install node@22

# Verify it's working
cd ai-kit
node --version  # Should show v22.x.x
```

If Volta isn't installed, follow the installation instructions in the Prerequisites section.

### Issue: "pnpm: command not found"

**Solution**: Enable Corepack:
```bash
corepack enable
```

Corepack is included with Node.js 22.x and will automatically install the correct pnpm version.

### Issue: Pre-commit hooks not running

**Solution**: Reinstall hooks:
```bash
pre-commit install
```

### Issue: CI failing with "undeclared dependency"

**Explanation**: ai-kit uses **strict package isolation** in CI. Each package is synced independently to catch undeclared dependencies.

**Solution**: Ensure all dependencies are declared in the package's `pyproject.toml`:
```bash
cd packages/your-package
uv add missing-dependency
```

## Understanding the Tooling Stack

### Python Tools

| Tool | Purpose | Why? |
|------|---------|------|
| **uv** | Package & dependency management | 10-100x faster than pip, native workspace support |
| **ruff** | Linting & formatting | All-in-one tool, replaces flake8 + black + isort |
| **just** | Task runner | Cross-platform Make alternative, simple syntax |

### Node.js Tools

| Tool | Purpose | Why? |
|------|---------|------|
| **Volta** | Node.js version management | Automatic version switching between projects |
| **Corepack** | Package manager version management | Official Node.js tool for pnpm/yarn versioning |
| **pnpm** | Package manager | Efficient, strict, native workspace support |
| **Turborepo** | Monorepo orchestration | Task caching, parallel execution |

### Why This Stack?

This tooling stack is mandated by **Constitution Principle IX** (Developer Experience & Tooling Consistency) to:

1. **Minimize cognitive load**: Standardized tools across all ai-kit projects
2. **Maximize productivity**: Fast tools (uv, ruff) reduce wait time
3. **Support multi-project work**: Volta enables seamless switching between projects
4. **Ensure quality**: Mandatory pre-commit hooks and strict CI validation

## Next Steps

### For New Contributors

1. **Read CONTRIBUTING.md**: Understand the contribution workflow
2. **Explore the codebase**: Start with `packages/` to see library structure
3. **Pick an issue**: Look for "good first issue" labels on GitHub
4. **Ask questions**: Join the team chat or open a discussion

### For Package Authors

1. **Create a new package**: Follow the monorepo structure (`apps/` or `packages/`)
2. **Add dependencies**: Use `uv add` in the package directory
3. **Add task scripts**: Create `package.json` with Turborepo scripts
4. **Write tests**: Use pytest, ensure tests pass in isolation
5. **Document**: Add README.md to your package

### Learning Resources

- **uv documentation**: https://docs.astral.sh/uv/
- **ruff documentation**: https://docs.astral.sh/ruff/
- **Turborepo documentation**: https://turbo.build/repo/docs
- **ai-kit Constitution**: `.specify/memory/constitution.md`

## Getting Help

- **Documentation issues**: Open an issue with the "documentation" label
- **Setup problems**: Check the Troubleshooting section above
- **Questions**: Open a GitHub Discussion
- **Bugs**: Open an issue with reproduction steps

## Feedback

This quickstart guide is continuously improved based on contributor feedback. If you found anything confusing or have suggestions, please:

1. Open an issue with the "documentation" label
2. Propose changes via pull request
3. Share feedback in team discussions

**Goal**: Every new contributor should be productive within 10 minutes of cloning the repository.
