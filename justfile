# List all available commands
default:
    @just --list

# Setup development environment (install all tools and dependencies)
setup:
    @echo "🔧 Setting up development environment..."
    @echo "📦 Installing Node.js via Volta..."
    volta install node@22
    @echo "📦 Enabling Corepack for pnpm..."
    corepack enable
    @echo "📦 Syncing Python dependencies with uv..."
    uv sync --all-packages
    @echo "📦 Installing Node.js dependencies with pnpm..."
    pnpm install
    @echo "🪝 Installing pre-commit hooks..."
    pre-commit install
    @echo "✅ Setup complete! Run 'just --list' to see available commands."

# Sync dependencies for all packages
sync:
    @echo "📦 Syncing all package dependencies..."
    uv sync --all-packages

# Run linting on all packages
lint:
    @echo "🔍 Running linting checks..."
    turbo run lint

# Format all Python code
format:
    @echo "✨ Formatting Python code..."
    turbo run format

# Run tests on all packages
test:
    @echo "🧪 Running tests..."
    turbo run test

# Build all packages
build:
    @echo "🏗️  Building packages..."
    turbo run build

# Clean build artifacts and caches
clean:
    @echo "🧹 Cleaning build artifacts and caches..."
    rm -rf .venv
    rm -rf node_modules
    rm -rf .turbo
    find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
    @echo "✅ Clean complete!"

# Clear Turborepo cache only
cache-clear:
    @echo "🧹 Clearing Turborepo cache..."
    rm -rf .turbo
    @echo "✅ Cache cleared!"

# Generic CLI command (for any CLI functionality)
cli *ARGS:
    @uv run --directory apps/cli python -m ai_kit.cli.main {{ARGS}}

# Notebook management commands (convenience wrapper)
notebook *ARGS:
    @uv run --directory apps/cli python -m ai_kit.cli.main notebook {{ARGS}}
