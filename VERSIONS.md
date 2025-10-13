# Tool Versions

This document lists all pinned tool versions for reproducible builds.

**Last Updated**: 2025-10-13

## Python Tooling

| Tool | Version | Pinned In | Purpose |
|------|---------|-----------|---------|
| **Python** | 3.12.10 | `.python-version` | Runtime |
| **uv** | 0.7.x+ | CI workflow | Package manager |
| **ruff** | 0.14.0 | `pyproject.toml`, `.pre-commit-config.yaml` | Linter & formatter |
| **pytest** | 8.0.0+ | `pyproject.toml` | Testing framework |
| **pre-commit** | 4.0.0+ | `pyproject.toml` | Git hooks |

## Node.js Tooling

| Tool | Version | Pinned In | Purpose |
|------|---------|-----------|---------|
| **Node.js** | 22.14.0 | `package.json` (volta) | Runtime |
| **pnpm** | 10.18.2 | `package.json` (packageManager) | Package manager |
| **Turborepo** | 2.5.8 | `package.json` | Build orchestration |

## System Tools

| Tool | Version | Installation | Purpose |
|------|---------|--------------|---------|
| **just** | 1.43.x+ | System package manager | Command runner |
| **Volta** | 2.0.x+ | curl install script | Node.js version manager |
| **Corepack** | Built-in | Enabled via `corepack enable` | Package manager version manager |

## Version Update Policy

### When to Update

- **Security patches**: Update immediately
- **Bug fixes**: Update in next sprint
- **New features**: Evaluate and plan update
- **Major versions**: Test thoroughly before updating

### How to Update

#### Python Dependencies
```bash
# Update all Python dependencies
uv sync --upgrade

# Update specific package
uv add --upgrade ruff

# Update lockfile
uv lock --upgrade
```

#### Node.js Dependencies
```bash
# Update pnpm version
# Edit package.json: "packageManager": "pnpm@X.Y.Z"
corepack prepare pnpm@X.Y.Z --activate
pnpm install

# Update Turborepo
pnpm add -D turbo@latest

# Update Node.js version
# Edit package.json: "volta": { "node": "X.Y.Z" }
volta install node@X.Y.Z
```

#### Pre-commit Hooks
```bash
# Update hook versions
uv run pre-commit autoupdate

# Test updated hooks
uv run pre-commit run --all-files
```

### Version Compatibility Matrix

| Python | Node.js | uv | ruff | Turborepo |
|--------|---------|-------|------|-----------|
| 3.12.10 | 22.14.0 | 0.7.x+ | 0.14.0 | 2.5.8 |
| 3.12.x | 22.x LTS | 0.7.x+ | 0.14.x | 2.5.x+ |

## CI/CD Versions

GitHub Actions uses the same versions as local development:

```yaml
# .github/workflows/ci.yml
- name: Install uv
  uses: astral-sh/setup-uv@v5  # Latest stable

- name: Set up Python
  run: uv python install  # Uses .python-version (3.12.10)
```

## Verification

Check installed versions:

```bash
# Python tooling
python --version          # 3.12.10
uv --version             # 0.7.x
uv run ruff --version    # 0.14.0
uv run pytest --version  # 8.x

# Node.js tooling
node --version           # v22.14.0
pnpm --version           # 10.18.2
pnpm turbo --version     # 2.5.8

# System tools
just --version           # 1.43.x
volta --version          # 2.0.x
```

## Changelog

### 2025-10-13
- Initial version documentation
- Python 3.12.10 (latest 3.12.x via uv)
- Node.js 22.14.0 (LTS)
- pnpm 10.18.2 (updated from 10.14.0)
- ruff 0.14.0
- Turborepo 2.5.8
- pytest 8.0.0+
- pre-commit 4.0.0+
