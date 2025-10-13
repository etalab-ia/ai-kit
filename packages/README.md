# Packages

This directory contains **importable libraries** without entry points.

## Purpose

Packages in this folder are:
- **Importable**: Provide reusable functionality
- **Library code**: No entry points or executables
- **Shared**: Used by apps and other packages

## Examples

- Core library (shared business logic)
- Templates (code generation, scaffolding)
- Configuration utilities
- Common utilities and helpers
- Shared types and interfaces

## Structure

Each package should have:
- `pyproject.toml` - Python dependencies
- `package.json` - Turborepo task scripts
- `src/` - Source code (no entry point)
- `tests/` - Package tests
- `README.md` - Package-specific documentation

## vs Apps

**Packages** (this folder):
- No entry points
- Are imported
- Provide reusable functionality

**Apps** (`../apps/`):
- Have entry points
- Are deployed/run
- Import from packages
