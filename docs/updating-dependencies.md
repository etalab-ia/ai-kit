# Dependency Update Guide

How to safely update Python and Node.js dependencies.

## Table of Contents

- [Python Dependencies](#python-dependencies)
- [Node Dependencies](#node-dependencies)
- [Tool Versions](#tool-versions)
- [Testing Updates](#testing-updates)
- [Rollback](#rollback)

## Python Dependencies

### Update All Dependencies

```bash
# Update all Python dependencies to latest compatible versions
uv sync --upgrade

# Review changes
git diff uv.lock
```

### Update Specific Package

```bash
# Update specific package
uv add --upgrade ruff

# Or edit pyproject.toml and sync
uv sync
```

### Update Dev Dependencies

```bash
# Update pre-commit hooks
uv run pre-commit autoupdate

# Test updated hooks
uv run pre-commit run --all-files
```

### Check for Outdated Packages

```bash
# List installed packages
uv pip list

# Check specific package version
uv pip show <package-name>
```

### Update Process

1. **Check current versions**
   ```bash
   uv pip list > before.txt
   ```

2. **Update dependencies**
   ```bash
   uv sync --upgrade
   ```

3. **Review changes**
   ```bash
   uv pip list > after.txt
   diff before.txt after.txt
   git diff uv.lock
   ```

4. **Test thoroughly**
   ```bash
   just lint
   just test
   just build
   ```

5. **Commit if successful**
   ```bash
   git add uv.lock pyproject.toml
   git commit -m "chore: update Python dependencies"
   ```

## Node Dependencies

### Update All Dependencies

```bash
# Update all Node.js dependencies
pnpm update

# Review changes
git diff pnpm-lock.yaml
```

### Update Specific Package

```bash
# Update Turborepo
pnpm add -D turbo@latest

# Or update to specific version
pnpm add -D turbo@2.6.0
```

### Update pnpm Version

```bash
# Edit package.json
# "packageManager": "pnpm@10.19.0"

# Activate new version
corepack prepare pnpm@10.19.0 --activate

# Reinstall
pnpm install
```

### Update Node.js Version

```bash
# Edit package.json
# "volta": { "node": "22.15.0" }

# Install new version
volta install node@22.15.0

# Verify
node --version
```

### Update Process

1. **Check current versions**
   ```bash
   pnpm list > before.txt
   ```

2. **Update dependencies**
   ```bash
   pnpm update
   ```

3. **Review changes**
   ```bash
   pnpm list > after.txt
   diff before.txt after.txt
   git diff pnpm-lock.yaml
   ```

4. **Test thoroughly**
   ```bash
   pnpm lint
   pnpm test
   pnpm build
   ```

5. **Commit if successful**
   ```bash
   git add pnpm-lock.yaml package.json
   git commit -m "chore: update Node.js dependencies"
   ```

## Tool Versions

### Python Version

```bash
# Check available versions
uv python list

# Install new version
uv python install 3.12.11

# Update .python-version
echo "3.12.11" > .python-version

# Recreate venv with new version
rm -rf .venv
uv sync --all-packages
```

### uv Version

```bash
# Update uv itself
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify
uv --version
```

### Ruff Version

```bash
# Update in pyproject.toml
# [dependency-groups]
# dev = ["ruff>=0.15.0"]

# Update pre-commit hook
# Edit .pre-commit-config.yaml
# rev: v0.15.0

# Sync
uv sync
uv run pre-commit autoupdate
```

### Turborepo Version

```bash
# Update in package.json
pnpm add -D turbo@latest

# Verify
pnpm turbo --version
```

## Testing Updates

### Pre-Update Checklist

- [ ] Create a new branch
- [ ] Backup current lockfiles
- [ ] Note current versions
- [ ] Ensure clean working directory

### Testing Strategy

#### 1. Unit Tests
```bash
# Run all tests
just test

# Run specific package tests
uv run --package ai-kit-core pytest
```

#### 2. Integration Tests
```bash
# Test CLI app
uv run --package ai-kit-cli ai-kit "Test"

# Test imports
uv run python -c "from ai_kit_core import hello; print(hello())"
```

#### 3. Linting and Formatting
```bash
# Run linting
just lint

# Run formatting
just format

# Check pre-commit hooks
uv run pre-commit run --all-files
```

#### 4. Build Tests
```bash
# Build all packages
just build

# Verify dist/ contents
ls -la packages/core/dist/
ls -la apps/cli/dist/
```

#### 5. CI Simulation
```bash
# Test strict package isolation (like CI)
rm -rf .venv
uv sync --package ai-kit-core
uv run --package ai-kit-core pytest packages/core/tests/

uv sync --package ai-kit-cli
uv run --package ai-kit-cli pytest apps/cli/tests/
```

### Post-Update Validation

```bash
# Full validation
just clean
just setup
just lint
just test
just build

# Verify versions
python --version
node --version
pnpm --version
uv --version
uv run ruff --version
```

## Rollback

### If Update Causes Issues

#### 1. Revert Lockfiles
```bash
# Revert Python lockfile
git checkout HEAD -- uv.lock

# Revert Node.js lockfile
git checkout HEAD -- pnpm-lock.yaml

# Reinstall
uv sync
pnpm install
```

#### 2. Revert Specific Package
```bash
# Python package
uv add package-name@1.2.3

# Node.js package
pnpm add -D package-name@1.2.3
```

#### 3. Full Rollback
```bash
# Discard all changes
git reset --hard HEAD

# Reinstall
just clean
just setup
```

### Emergency Rollback

If environment is broken:

```bash
# Nuclear option - start fresh
rm -rf .venv node_modules .turbo
git checkout HEAD -- uv.lock pnpm-lock.yaml
just setup
```

## Update Schedule

### Recommended Frequency

| Type | Frequency | Priority |
|------|-----------|----------|
| Security patches | Immediately | Critical |
| Bug fixes | Weekly | High |
| Minor versions | Monthly | Medium |
| Major versions | Quarterly | Low |
| Tool versions | As needed | Medium |

### Security Updates

```bash
# Check for security advisories
uv pip check

# Update immediately if vulnerabilities found
uv sync --upgrade
```

## Best Practices

### Do
- ✅ Update dependencies regularly
- ✅ Test thoroughly before committing
- ✅ Update one thing at a time (Python OR Node, not both)
- ✅ Read changelogs for major updates
- ✅ Keep lockfiles committed
- ✅ Document breaking changes

### Don't
- ❌ Update without testing
- ❌ Skip lockfile commits
- ❌ Update during active development
- ❌ Ignore deprecation warnings
- ❌ Update major versions without review

## Troubleshooting

### Dependency Conflicts

```bash
# Check for conflicts
uv pip check

# Resolve by adjusting version ranges
# Edit pyproject.toml
uv sync
```

### Build Failures After Update

```bash
# Clear caches
just clean

# Reinstall from scratch
uv sync --all-packages
pnpm install

# Test again
just test
```

### Version Mismatch Between Local and CI

```bash
# Ensure lockfiles are committed
git status uv.lock pnpm-lock.yaml

# Push lockfiles
git add uv.lock pnpm-lock.yaml
git commit -m "chore: update lockfiles"
git push
```

## Update Checklist

Before updating:
- [ ] Create update branch
- [ ] Note current versions
- [ ] Backup lockfiles

During update:
- [ ] Update dependencies
- [ ] Review changes
- [ ] Run tests
- [ ] Check CI

After update:
- [ ] Commit lockfiles
- [ ] Update VERSIONS.md
- [ ] Document breaking changes
- [ ] Notify team

## Related Documentation

- [VERSIONS.md](../VERSIONS.md) - Current tool versions
- [CI Troubleshooting](./troubleshooting-ci.md)
- [Contributing Guide](../CONTRIBUTING.md)
