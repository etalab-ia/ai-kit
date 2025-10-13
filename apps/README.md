# Apps

This directory contains **deployable applications** with entry points.

## Purpose

Applications in this folder are:
- **Executable**: Have entry points (CLI tools, servers, web apps)
- **Deployable**: Can be run independently
- **User-facing**: Provide functionality to end users

## Examples

- CLI tools (command-line interfaces)
- API servers (REST, GraphQL)
- Web applications
- Background workers
- Scheduled jobs

## Structure

Each app should have:
- `pyproject.toml` - Python dependencies
- `package.json` - Turborepo task scripts
- `src/` - Source code with entry point
- `tests/` - Application tests
- `README.md` - App-specific documentation

## vs Packages

**Apps** (this folder):
- Have entry points
- Are deployed/run
- Import from packages

**Packages** (`../packages/`):
- No entry points
- Are imported
- Provide reusable functionality
