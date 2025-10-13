# Documentation Index

Complete guide to all ai-kit documentation.

## Quick Start

**New to ai-kit?** Start here:
1. [README.md](./README.md) - Project overview and quick start
2. [CONTRIBUTING.md](./CONTRIBUTING.md) - Development guide
3. [Setup Guide](./docs/setup-platform-specific.md) - Platform-specific instructions

## Core Documentation

### Getting Started
- **[README.md](./README.md)** - Project overview, quick start, technology stack
- **[CONTRIBUTING.md](./CONTRIBUTING.md)** - Complete contributor guide
- **[VERSIONS.md](./VERSIONS.md)** - Tool versions and update policy

### Setup & Configuration
- **[Platform-Specific Setup](./docs/setup-platform-specific.md)** - macOS, Linux, Windows, Docker
- **[TURBOREPO.md](./TURBOREPO.md)** - Turborepo configuration explained
- **[.python-version](./.python-version)** - Python version (3.12.10)
- **[package.json](./package.json)** - Node.js and pnpm versions

### Development Workflow
- **[justfile](./justfile)** - Available commands (`just --list`)
- **[pyproject.toml](./pyproject.toml)** - Python workspace configuration
- **[turbo.json](./turbo.json)** - Turborepo pipeline configuration

## Troubleshooting Guides

### Common Issues
- **[CI Troubleshooting](./docs/troubleshooting-ci.md)** - Lint, format, test, dependency issues
- **[Virtual Environment Issues](./docs/troubleshooting-venv.md)** - .venv problems and edge cases
- **[Turborepo Issues](./docs/troubleshooting-turborepo.md)** - Cache corruption and performance

### Maintenance
- **[Updating Dependencies](./docs/updating-dependencies.md)** - Python, Node.js, tool updates
- **[CI Testing Guide](./.github/CI_TESTING.md)** - Testing CI failures

## Package Documentation

### Applications (apps/)
- **[CLI App](./apps/cli/README.md)** - Command-line interface
- **[Apps Overview](./apps/README.md)** - What goes in apps/

### Libraries (packages/)
- **[Core Library](./packages/core/README.md)** - Core functionality
- **[Packages Overview](./packages/README.md)** - What goes in packages/

## Validation & Quality

- **[VALIDATION.md](./VALIDATION.md)** - Success criteria validation results
- **[.pre-commit-config.yaml](./.pre-commit-config.yaml)** - Pre-commit hooks configuration
- **[.github/workflows/ci.yml](./.github/workflows/ci.yml)** - CI pipeline
- **[.github/workflows/pre-commit.yml](./.github/workflows/pre-commit.yml)** - Pre-commit validation

## Specification Documents

Located in `specs/001-setup-developer-experience/`:
- **[spec.md](./specs/001-setup-developer-experience/spec.md)** - Feature specification
- **[plan.md](./specs/001-setup-developer-experience/plan.md)** - Implementation plan
- **[tasks.md](./specs/001-setup-developer-experience/tasks.md)** - Task breakdown
- **[research.md](./specs/001-setup-developer-experience/research.md)** - Research findings
- **[quickstart.md](./specs/001-setup-developer-experience/quickstart.md)** - Quick reference

## Documentation by Role

### New Contributors
1. [README.md](./README.md) - Start here
2. [CONTRIBUTING.md](./CONTRIBUTING.md) - How to contribute
3. [Platform-Specific Setup](./docs/setup-platform-specific.md) - Install tools
4. [CI Troubleshooting](./docs/troubleshooting-ci.md) - Fix common issues

### Active Developers
1. [CONTRIBUTING.md](./CONTRIBUTING.md) - Development workflow
2. [TURBOREPO.md](./TURBOREPO.md) - Understanding Turborepo
3. [Updating Dependencies](./docs/updating-dependencies.md) - Maintenance
4. [Virtual Environment Issues](./docs/troubleshooting-venv.md) - Debug .venv

### Maintainers
1. [VERSIONS.md](./VERSIONS.md) - Version management
2. [VALIDATION.md](./VALIDATION.md) - Quality metrics
3. [CI Testing Guide](./.github/CI_TESTING.md) - CI validation
4. [Specification Documents](./specs/001-setup-developer-experience/) - Feature details

## Documentation by Topic

### Setup & Installation
- [README.md](./README.md) - Quick start
- [Platform-Specific Setup](./docs/setup-platform-specific.md) - Detailed setup
- [VERSIONS.md](./VERSIONS.md) - Tool versions

### Development
- [CONTRIBUTING.md](./CONTRIBUTING.md) - Development guide
- [justfile](./justfile) - Commands
- [TURBOREPO.md](./TURBOREPO.md) - Monorepo orchestration

### Troubleshooting
- [CI Troubleshooting](./docs/troubleshooting-ci.md) - CI issues
- [Virtual Environment Issues](./docs/troubleshooting-venv.md) - .venv problems
- [Turborepo Issues](./docs/troubleshooting-turborepo.md) - Cache issues

### Maintenance
- [Updating Dependencies](./docs/updating-dependencies.md) - Updates
- [VERSIONS.md](./VERSIONS.md) - Version policy

### Quality Assurance
- [VALIDATION.md](./VALIDATION.md) - Success criteria
- [CI Testing Guide](./.github/CI_TESTING.md) - Testing

## Quick Reference

### Common Commands
```bash
just --list          # List all commands
just setup           # Initial setup
just lint            # Run linting
just format          # Format code
just test            # Run tests
just build           # Build packages
just clean           # Clean artifacts
just cache-clear     # Clear Turborepo cache
```

### Tool Versions
- Python: 3.12.10
- Node.js: 22.14.0
- pnpm: 10.18.2
- uv: 0.7.x+
- ruff: 0.14.0
- Turborepo: 2.5.8

### Important Files
- `.python-version` - Python version
- `pyproject.toml` - Python workspace
- `package.json` - Node.js config
- `turbo.json` - Turborepo pipeline
- `justfile` - Commands
- `uv.lock` - Python dependencies
- `pnpm-lock.yaml` - Node.js dependencies

## Documentation Standards

All documentation follows these standards:
- ✅ Clear structure with table of contents
- ✅ Searchable headings
- ✅ Step-by-step instructions
- ✅ Code examples
- ✅ Troubleshooting sections
- ✅ Cross-references to related docs

## Contributing to Documentation

See [CONTRIBUTING.md](./CONTRIBUTING.md) for:
- Documentation style guide
- How to update docs
- Where to add new documentation

## Getting Help

Can't find what you need?
1. Search this index
2. Check [CONTRIBUTING.md](./CONTRIBUTING.md) troubleshooting
3. Search [GitHub Issues](https://github.com/your-org/ai-kit/issues)
4. Ask in [GitHub Discussions](https://github.com/your-org/ai-kit/discussions)

## Documentation Checklist

For new features, ensure documentation includes:
- [ ] README.md update (if user-facing)
- [ ] CONTRIBUTING.md update (if workflow changes)
- [ ] Troubleshooting guide (for common issues)
- [ ] Version updates (VERSIONS.md)
- [ ] Validation results (VALIDATION.md)
- [ ] This index (if new doc added)
