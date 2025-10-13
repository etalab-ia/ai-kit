# ai-kit

**AI toolkit for French Government digital services**

A Python-first monorepo providing tools, templates, and libraries for building AI-powered applications that comply with French Government standards (EU AI Act, RGAA, Security Homologation).

## Quick Start

### Prerequisites

- **Python**: 3.12+ (managed by uv)
- **Node.js**: 22.x LTS (managed by Volta)
- **Tools**: [uv](https://docs.astral.sh/uv/), [just](https://github.com/casey/just), [Volta](https://volta.sh/)

### Setup (< 10 minutes)

```bash
# Clone the repository
git clone https://github.com/your-org/ai-kit.git
cd ai-kit

# Run setup (installs all tools and dependencies)
just setup

# Verify installation
just --list
```

That's it! You're ready to develop. 🎉

## Development Workflow

### Common Commands

```bash
# Sync dependencies
just sync

# Run linting
just lint

# Format code
just format

# Run tests
just test

# Build packages
just build

# Clean artifacts
just clean
```

### Running the CLI

```bash
# Run the example CLI
uv run --package ai-kit-cli ai-kit "Your Name"
```

## Monorepo Structure

```
ai-kit/
├── apps/                    # Deployable applications
│   └── cli/                # Example CLI application
├── packages/                # Importable libraries
│   └── core/               # Core library
├── .github/workflows/       # CI/CD pipelines
├── pyproject.toml          # Root workspace configuration
├── package.json            # Turborepo configuration
└── justfile                # Development commands
```

### Apps vs Packages

- **apps/**: Deployable applications with entry points (CLI tools, servers, web apps)
- **packages/**: Importable libraries without entry points (core, templates, utilities)

## Technology Stack

### Python Tooling
- **uv** (0.7.x+): Package and dependency management with workspace support
- **ruff** (0.14.x+): Lightning-fast linting and formatting
- **just** (1.43.x+): Command runner for development tasks
- **pytest** (8.x+): Testing framework

### Node.js Tooling
- **Volta** (2.0.x+): Node.js version management with automatic switching
- **pnpm** (10.x+): Fast, efficient package manager (via Corepack)
- **Turborepo** (2.5.x+): Monorepo build system with caching

### Code Quality
- **pre-commit**: Git hooks for automated quality checks
- **GitHub Actions**: CI/CD pipelines with strict package isolation

## Key Features

✅ **Python-First**: Python 3.12+ with modern tooling (uv, ruff)  
✅ **Monorepo**: Single repository, multiple packages, shared virtual environment  
✅ **Fast**: Turborepo caching reduces build time by 95%  
✅ **Strict**: Package isolation catches undeclared dependencies  
✅ **Automated**: Pre-commit hooks and CI/CD pipelines  
✅ **Cross-Platform**: Works on macOS, Linux, and Windows  

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed development guidelines.

## Documentation

- **Setup Guide**: [quickstart.md](./specs/001-setup-developer-experience/quickstart.md)
- **Contributing Guide**: [CONTRIBUTING.md](./CONTRIBUTING.md)
- **CI Testing**: [.github/CI_TESTING.md](./.github/CI_TESTING.md)
- **Package READMEs**: See individual package directories

## Architecture

This project follows a **hybrid Python + Node.js monorepo** architecture:

- **Python workspace** (uv): Single `.venv` at root, all packages share dependencies
- **Node.js workspace** (pnpm): Mirrors Python structure for Turborepo orchestration
- **Task orchestration** (Turborepo): Parallel execution, intelligent caching

## Success Metrics

- ⏱️ **Setup time**: <10 minutes for new contributors
- 🚀 **Lint/format**: <30 seconds for typical changes
- ⚡ **CI pipeline**: <5 minutes for typical PRs
- 📦 **Cache hit**: 95% faster builds for unchanged packages

## License

MIT

## Support

- **Issues**: [GitHub Issues](https://github.com/your-org/ai-kit/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-org/ai-kit/discussions)
- **Documentation**: [specs/](./specs/)
