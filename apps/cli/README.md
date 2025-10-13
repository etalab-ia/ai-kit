# ai-kit CLI

Command-line interface for the ai-kit toolkit.

## Overview

This application provides a command-line interface to interact with ai-kit functionality.

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

```bash
# Basic usage
ai-kit

# With a custom name
ai-kit Alice
```

## Dependencies

- `ai-kit-core`: Core library (workspace dependency)
