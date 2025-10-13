# Phase 0: Research & Technical Decisions

**Feature**: Setup Developer Experience & Tooling for ai-kit  
**Date**: 2025-10-13  
**Status**: Completed

## Overview

This document captures research findings and technical decisions for establishing the developer experience infrastructure for ai-kit. All decisions align with Constitution Principle IX (Developer Experience & Tooling Consistency).

## Research Areas

### 1. Python Tooling Stack

#### Decision: uv for Package Management

**Chosen**: uv 0.7.x+ with workspace support

**Rationale**:
- **Native workspace support**: Single `.venv` at root, automatic local package linking
- **Performance**: Rust-based, 10-100x faster than pip
- **Modern**: Replaces pip, pip-tools, virtualenv, and poetry in one tool
- **Government context**: Open source (Apache 2.0/MIT), actively maintained by Astral

**Alternatives Considered**:
- **Poetry**: Mature but slower, doesn't support true workspaces (only path dependencies)
- **PDM**: Good workspace support but less adoption, smaller ecosystem
- **pip + pip-tools**: Traditional but no workspace support, manual management

**References**:
- uv workspaces: https://docs.astral.sh/uv/concepts/workspaces/
- Real-world examples: carderne/postmodern-mono, JasperHG90/uv-monorepo

#### Decision: ruff for Linting & Formatting

**Chosen**: ruff 0.14.x+

**Rationale**:
- **All-in-one**: Replaces flake8, black, isort, pyupgrade in single tool
- **Performance**: Rust-based, 10-100x faster than alternatives
- **Compatible**: Drop-in replacement for existing tools
- **Maintained**: By Astral (same team as uv), strong ecosystem support

**Alternatives Considered**:
- **black + flake8 + isort**: Traditional stack but slower, multiple tools to configure
- **pylint**: More comprehensive but much slower, opinionated

#### Decision: just for Task Runner

**Chosen**: just 1.43.x+

**Rationale**:
- **Simple**: Make-like syntax but cross-platform (Windows, macOS, Linux)
- **Modern**: Better error messages, no tab/space issues
- **Discoverable**: `just --list` shows all commands with descriptions
- **Composable**: Can call other tools (uv, ruff, Turborepo)

**Alternatives Considered**:
- **Make**: Traditional but Windows compatibility issues, tab/space problems
- **invoke (Python)**: Requires Python, adds dependency, less discoverable
- **npm scripts**: Would require Node.js for Python-only tasks

### 2. Node.js Tooling Stack

#### Decision: Volta + Corepack Hybrid

**Chosen**: Volta 2.0.x+ for Node.js version management, Corepack for pnpm version management

**Rationale**:
- **Automatic switching**: Volta reads `volta` field in `package.json`, switches Node.js versions on `cd`
- **Critical for government**: Developers work on multiple projects (legacy Node 16/18/20, modern Node 22)
- **Industry standard**: Corepack's `packageManager` field is expected by Turborepo and modern tools
- **Future-proof**: Corepack removed from Node 25+ but available via npm, so both tools require installation anyway
- **Best DX**: No manual `nvm use` or version management needed

**Alternatives Considered**:
- **Corepack only**: No automatic Node version switching, painful multi-project DX
- **Volta only**: Loses `packageManager` field standard, not compatible with Turborepo expectations
- **nvm**: Manual switching (`nvm use`), no automatic detection, shell-specific

**References**:
- Volta + Corepack compatibility: https://github.com/volta-cli/volta/issues/1200
- Corepack official docs: https://nodejs.org/api/corepack.html
- Industry adoption: Vercel (Turborepo), Yarn Berry, pnpm all recommend Corepack

#### Decision: pnpm 10.x+ for Package Manager

**Chosen**: pnpm 10.x+ (latest stable)

**Rationale**:
- **Workspace support**: Native monorepo support, aligns with uv workspaces
- **Efficiency**: Content-addressable storage, saves disk space
- **Strict**: Prevents phantom dependencies better than npm/yarn
- **Performance**: Faster than npm, comparable to yarn
- **Constitution compliance**: Standardized in Principle IX (v1.6.2)

**Alternatives Considered**:
- **npm**: Slower, less strict dependency resolution
- **yarn (classic)**: Deprecated, being replaced by Yarn Berry
- **yarn (berry)**: Good but less adoption than pnpm, different workflow

#### Decision: Turborepo 2.5.x+ for Monorepo Orchestration

**Chosen**: Turborepo 2.5.x+

**Rationale**:
- **Language agnostic**: Works with Python packages via `package.json` scripts
- **Caching**: Remote and local caching reduces CI time by 50%+
- **Parallel execution**: Runs independent tasks across packages simultaneously
- **Industry standard**: Used by Vercel, widely adopted for monorepos
- **Proven with Python**: Examples exist (sinanbekar/monorepo-turborepo-python)

**Alternatives Considered**:
- **Nx**: More features but heavier, TypeScript-focused, steeper learning curve
- **Lerna**: Deprecated, maintenance mode
- **Rush**: Microsoft tool, less adoption, more complex
- **Bazel**: Overkill for this scale, steep learning curve

**References**:
- Turborepo with Python: https://github.com/sinanbekar/monorepo-turborepo-python
- Turborepo docs: https://turbo.build/repo/docs

### 3. Monorepo Structure

#### Decision: apps/ and packages/ Folders

**Chosen**: `apps/` for deployable applications, `packages/` for importable libraries

**Rationale**:
- **Clear separation**: Deployable vs importable is intuitive
- **Python convention**: Matches uv monorepo examples (postmodern-mono, uv-monorepo)
- **Turborepo convention**: Standard pattern in Turborepo monorepos
- **Scalable**: Easy to understand which packages are entry points vs libraries

**Alternatives Considered**:
- **Flat structure**: All packages at root, harder to distinguish apps from libraries
- **src/ and libs/**: Less clear, "src" ambiguous in monorepo context
- **services/ and packages/**: "Services" implies microservices, not always accurate

### 4. CI/CD Strategy

#### Decision: Strict Package Isolation in ALL CI Jobs

**Chosen**: Every CI job (lint, test, build) syncs only the specific package being tested

**Rationale**:
- **Maximum safety**: Catches undeclared dependencies before production
- **ai-kit as exemplar**: Demonstrates best practices for government projects
- **Prevents phantom dependencies**: Package imports work locally (shared `.venv`) but fail in production
- **Compliance**: Security auditing requires clear dependency graphs

**Alternatives Considered**:
- **Full workspace sync**: Faster but misses undeclared dependencies
- **Dedicated validation job only**: Catches issues but not in every job, less strict

**References**:
- Best practice: carderne/postmodern-mono CI approach
- Rationale: https://github.com/carderne/postmodern-mono#ci-setup

### 5. Code Quality Enforcement

#### Decision: Mandatory Pre-commit Hooks

**Chosen**: Pre-commit hooks installed automatically, cannot be disabled

**Rationale**:
- **Stable foundation**: Ensures code quality at commit time, not just in CI
- **Fast feedback**: Developers see issues immediately, not after push
- **Reduces CI load**: Fewer failed CI runs due to formatting/linting
- **Government context**: Consistent quality standards across all contributors

**Alternatives Considered**:
- **Optional hooks**: Developers might skip them, inconsistent quality
- **CI-only checks**: Slower feedback loop, more failed CI runs
- **Manual installation**: Requires discipline, easy to forget

### 6. Version Requirements

#### Decisions Summary

| Tool | Version | Rationale |
|------|---------|-----------|
| Python | 3.12+ | Modern features, excellent performance, type hints improvements |
| Node.js | 22.x LTS | Current Active LTS (until April 2026), Corepack built-in, stable |
| pnpm | 10.x+ | Latest stable, excellent workspace support, aligns with Corepack |
| uv | 0.7.x+ | Workspace support stable, actively maintained (latest: 0.7.8) |
| ruff | 0.14.x+ | Latest stable, all linting/formatting features (latest: 0.14.0) |
| just | 1.43.x+ | Stable, cross-platform (latest: 1.43.0) |
| Volta | 2.0.x+ | Latest stable, automatic version switching (latest: 2.0.2) |
| Turborepo | 2.5.x+ | Latest stable, improved caching (latest: 2.5.8) |

## Configuration Examples

### Root pyproject.toml

```toml
[project]
name = "ai-kit"
version = "0.1.0"
requires-python = ">=3.12"

[tool.uv.workspace]
members = ["apps/*", "packages/*"]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W"]
ignore = []
```

### Root package.json

```json
{
  "name": "ai-kit",
  "version": "0.1.0",
  "private": true,
  "volta": {
    "node": "22.14.0"
  },
  "packageManager": "pnpm@10.14.0",
  "engines": {
    "node": ">=22.0.0",
    "pnpm": ">=10.0.0"
  },
  "workspaces": [
    "apps/*",
    "packages/*"
  ]
}
```

### turbo.json

```json
{
  "$schema": "https://turbo.build/schema.json",
  "pipeline": {
    "lint": {
      "cache": true,
      "inputs": ["**/*.py", "pyproject.toml", "ruff.toml"]
    },
    "format": {
      "cache": true,
      "inputs": ["**/*.py", "pyproject.toml", "ruff.toml"]
    },
    "test": {
      "cache": true,
      "dependsOn": ["^build"],
      "inputs": ["**/*.py", "tests/**", "pyproject.toml"]
    },
    "build": {
      "cache": true,
      "dependsOn": ["^build"],
      "outputs": ["dist/**"]
    }
  }
}
```

### justfile

```makefile
# List all available commands
default:
    @just --list

# Setup development environment
setup:
    uv sync --all-packages
    pnpm install
    pre-commit install

# Sync dependencies for all packages
sync:
    uv sync --all-packages

# Run linting on all packages
lint:
    turbo run lint

# Format all Python code
format:
    turbo run format

# Run tests on all packages
test:
    turbo run test

# Build all packages
build:
    turbo run build

# Clean build artifacts and caches
clean:
    rm -rf .venv
    rm -rf node_modules
    rm -rf .turbo
    find . -type d -name "__pycache__" -exec rm -rf {} +
    find . -type d -name "dist" -exec rm -rf {} +
```

## Implementation Priorities

### Phase 1: Python Tooling (P1)
1. Create root `pyproject.toml` with workspace configuration
2. Initialize uv workspace with `apps/` and `packages/` folders
3. Configure ruff for linting and formatting
4. Create justfile with basic commands
5. Setup pre-commit hooks

### Phase 2: Monorepo Structure (P2)
6. Create folder structure (`apps/`, `packages/`)
7. Add `.gitkeep` files as placeholders
8. Update `.gitignore` for Python + Node.js

### Phase 3: Node.js Integration (P2)
9. Create root `package.json` with Volta and pnpm configuration
10. Create `pnpm-workspace.yaml`
11. Configure Turborepo with `turbo.json`
12. Add minimal `package.json` to each package (template)

### Phase 4: CI/CD (P3)
13. Create GitHub Actions workflow with strict package isolation
14. Configure caching for Turborepo and dependencies
15. Add pre-commit hook validation

### Phase 5: Documentation (P3)
16. Update README.md with setup instructions
17. Create CONTRIBUTING.md with developer guide
18. Create quickstart.md with onboarding flow

## Success Metrics

- ✅ Setup time: <10 minutes for new contributors
- ✅ Lint/format: <30 seconds for typical changes
- ✅ CI time: <5 minutes for typical PRs
- ✅ Turborepo cache: ≥50% build time reduction
- ✅ Automatic version switching: Works seamlessly via Volta

## Open Questions

None - all clarifications resolved during specification phase.

## References

### Documentation
- uv: https://docs.astral.sh/uv/
- ruff: https://docs.astral.sh/ruff/
- just: https://just.systems/
- Volta: https://volta.sh/
- Corepack: https://nodejs.org/api/corepack.html
- pnpm: https://pnpm.io/
- Turborepo: https://turbo.build/repo/docs

### Real-World Examples
- carderne/postmodern-mono: Python monorepo with uv workspaces
- JasperHG90/uv-monorepo: uv workspace pattern with justfile
- sinanbekar/monorepo-turborepo-python: Turborepo with Python (FastAPI)

### Constitution
- ai-kit Constitution v1.6.2: Principle IX (Developer Experience & Tooling Consistency)
