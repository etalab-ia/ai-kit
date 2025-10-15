# ai-kit CLI

Unified command-line interface for the ai-kit toolkit.

## Overview

This application provides a unified CLI for ai-kit functionality, including:
- **Notebook management**: Create, validate, and manage Jupyter notebooks
- **Future extensions**: Dataset management, Streamlit apps, compliance tools, experiment tracking

## Installation

This package is part of the ai-kit monorepo and is managed by uv workspaces.

## Development

```bash
# Run the CLI
uv run --package ai-kit-cli ai-kit

# Run tests
just test

# Run linting
just lint

# Format code
just format
```

## Usage

### Notebook Commands

```bash
# Create a new notebook (interactive)
just notebook create

# List all notebooks by category
just notebook list

# Validate notebook metadata
just notebook validate notebooks/exploratory/my-notebook.ipynb

# Show notebook statistics
just notebook stats

# Delete a notebook (with confirmation)
just notebook delete notebooks/exploratory/old-notebook.ipynb
```

### Direct CLI Usage

```bash
# Run via uv
uv run --package ai-kit-cli ai-kit notebook create

# Or use the justfile wrapper (recommended)
just notebook create
```

## Dependencies

- `ai-kit-core`: Core library (workspace dependency)
- `click`: CLI framework
- `questionary`: Interactive prompts
- `rich`: Formatted terminal output
- `nbformat`: Jupyter notebook manipulation
- `ruamel.yaml`: YAML processing

## Architecture

The CLI follows a modular command group structure:

```
ai_kit/cli/
├── main.py              # CLI entry point
├── commands/            # Command groups
│   └── notebook.py      # Notebook management commands
├── core/                # Core business logic
│   ├── config.py        # Configuration management
│   ├── validators.py    # Validation logic
│   └── templates.py     # Template management
└── utils/               # Utility functions
    ├── git.py           # Git operations
    ├── prompts.py       # Interactive prompts
    └── output.py        # Formatted output
```

## Extending the CLI

To add a new command group:

1. Create `commands/mycommand.py` with a click group
2. Register in `main.py`: `cli.add_command(mycommand.mycommand)`
3. Add justfile wrapper: `mycommand *ARGS: @uv run --directory apps/cli python -m ai_kit.cli.main mycommand {{ARGS}}`

## Testing

```bash
# Run all tests
cd apps/cli
uv run pytest

# Run specific test file
uv run pytest tests/commands/test_notebook.py

# Run with coverage
uv run pytest --cov=ai_kit.cli
```
