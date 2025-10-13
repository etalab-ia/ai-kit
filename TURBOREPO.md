# Turborepo Configuration Guide

This document explains the `turbo.json` configuration for the ai-kit monorepo.

## Overview

Turborepo orchestrates tasks across packages with intelligent caching and parallel execution.

## Configuration (`turbo.json`)

### Schema
```json
"$schema": "https://turbo.build/schema.json"
```
Enables IDE autocomplete and validation.

### UI
```json
"ui": "tui"
```
Uses terminal UI for better task visualization.

### Tasks

#### lint
```json
"lint": {
  "cache": true,
  "inputs": ["**/*.py", "pyproject.toml", ".ruff.toml"]
}
```
- **cache**: Results are cached based on inputs
- **inputs**: Files that affect linting results
- **No outputs**: Linting doesn't produce files
- **No dependencies**: Can run independently

#### format
```json
"format": {
  "cache": true,
  "inputs": ["**/*.py", "pyproject.toml", ".ruff.toml"],
  "outputs": ["**/*.py"]
}
```
- **cache**: Caches formatted files
- **inputs**: Files that affect formatting
- **outputs**: Formatted Python files
- **No dependencies**: Can run independently

#### test
```json
"test": {
  "cache": true,
  "dependsOn": ["^build"],
  "inputs": ["**/*.py", "tests/**", "pyproject.toml"],
  "outputs": [".coverage", "htmlcov/**"]
}
```
- **cache**: Caches test results
- **dependsOn**: `^build` means "wait for dependencies to build first"
- **inputs**: Source code and test files
- **outputs**: Coverage reports

#### build
```json
"build": {
  "cache": true,
  "dependsOn": ["^build"],
  "inputs": ["src/**", "pyproject.toml"],
  "outputs": ["dist/**", "build/**", "*.egg-info/**"]
}
```
- **cache**: Caches build artifacts
- **dependsOn**: `^build` ensures dependencies build first
- **inputs**: Source code and package config
- **outputs**: Distribution files

## Dependency Notation

- `^task`: Run `task` in **dependencies** first (topological order)
- `task`: Run `task` in **this package** first
- No prefix: Run in parallel

## Cache Behavior

### Cache Hit
When inputs haven't changed:
- Turborepo replays logs from cache
- Outputs are restored from cache
- Task completes in milliseconds
- Shows "cache hit" in output

### Cache Miss
When inputs have changed:
- Task executes normally
- Results are cached for next run
- Shows "cache miss" in output

## Running Tasks

### Via pnpm (recommended)
```bash
pnpm turbo run lint        # Run lint across all packages
pnpm turbo run test        # Run tests (respects dependencies)
pnpm turbo run build       # Build all packages
```

### Via just (high-level)
```bash
just lint                  # Runs: turbo run lint
just test                  # Runs: turbo run test
just build                 # Runs: turbo run build
```

### Force rebuild (ignore cache)
```bash
pnpm turbo run build --force
```

### Filter by package
```bash
pnpm turbo run test --filter=@ai-kit/core
```

## Performance

### First Run (cache miss)
```
Tasks:    4 successful, 4 total
Cached:    0 cached, 4 total
  Time:    2.5s
```

### Second Run (cache hit)
```
Tasks:    4 successful, 4 total
Cached:    4 cached, 4 total
  Time:    50ms >>> FULL TURBO
```

**95% faster!** 🚀

## CI Integration

In GitHub Actions, Turborepo cache is persisted using `actions/cache`:

```yaml
- name: Setup Turborepo cache
  uses: actions/cache@v4
  with:
    path: .turbo
    key: ${{ runner.os }}-turbo-${{ github.sha }}
    restore-keys: |
      ${{ runner.os }}-turbo-
```

## Troubleshooting

### Cache not working
```bash
# Clear cache and rebuild
rm -rf .turbo
pnpm turbo run build --force
```

### Tasks running in wrong order
- Check `dependsOn` configuration
- Ensure `^build` is used for dependency builds

### Outputs not cached
- Verify `outputs` paths are correct
- Check that tasks actually produce those files

## Best Practices

1. **Inputs**: Include all files that affect task output
2. **Outputs**: List all generated files for proper caching
3. **Dependencies**: Use `^task` for topological ordering
4. **Cache**: Enable for all deterministic tasks
5. **Parallel**: Let Turborepo handle parallelization

## References

- [Turborepo Documentation](https://turbo.build/repo/docs)
- [Caching Guide](https://turbo.build/repo/docs/core-concepts/caching)
- [Configuration Reference](https://turbo.build/repo/docs/reference/configuration)
