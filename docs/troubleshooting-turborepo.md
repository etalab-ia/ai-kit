# Turborepo Troubleshooting

Common Turborepo cache issues and recovery procedures.

## Table of Contents

- [Cache Corruption](#cache-corruption)
- [Cache Misses](#cache-misses)
- [Slow Builds](#slow-builds)
- [Cache Clear Command](#cache-clear-command)

## Cache Corruption

### Symptom
- Tasks fail with cryptic errors
- "cache hit" but outputs are missing or incorrect
- Inconsistent behavior between runs

### Detection
```bash
# Run task twice - should be identical
pnpm build
pnpm build

# If second run shows different results, cache may be corrupted
```

### Cause
- Interrupted build process
- Disk corruption
- Manual modification of cached files
- Bug in Turborepo (rare)

### Recovery

#### 1. Clear Turborepo cache
```bash
# Remove cache directory
rm -rf .turbo

# Force rebuild
pnpm build --force
```

#### 2. Clear all caches (comprehensive)
```bash
# Use justfile command
just clean

# Or manually
rm -rf .turbo
rm -rf node_modules/.cache
rm -rf .venv
uv sync --all-packages
pnpm install
```

#### 3. Verify recovery
```bash
# Run build twice
pnpm build
pnpm build

# Second run should show "cache hit"
```

### Prevention
- Don't manually modify `.turbo/` directory
- Ensure adequate disk space
- Let tasks complete fully
- Use `--force` when testing cache behavior

## Cache Misses

### Symptom
```
Tasks:    4 successful, 4 total
Cached:    0 cached, 4 total  # Expected some cache hits
  Time:    2.5s
```

### Debugging Cache Misses

#### 1. Check task inputs
```json
// turbo.json
{
  "tasks": {
    "build": {
      "inputs": ["src/**", "pyproject.toml"]  # These files affect cache
    }
  }
}
```

**Common issues**:
- Missing files in `inputs`
- Too broad glob patterns
- Generated files in inputs

#### 2. Verify no file changes
```bash
# Check git status
git status

# Check for generated files
find . -name "*.pyc" -o -name "__pycache__"
```

#### 3. Check cache configuration
```bash
# View turbo configuration
cat turbo.json

# Check cache location
ls -la .turbo/cache/
```

#### 4. Enable verbose logging
```bash
# See why cache missed
pnpm build --verbosity=2
```

### Common Causes

#### Generated Files in Inputs
```json
// Bad - includes generated files
{
  "inputs": ["**/*.py"]  // Includes __pycache__/*.pyc
}

// Good - excludes generated files
{
  "inputs": ["src/**/*.py", "tests/**/*.py", "pyproject.toml"]
}
```

#### Missing Inputs
```json
// Bad - missing config file
{
  "inputs": ["src/**"]
}

// Good - includes config
{
  "inputs": ["src/**", "pyproject.toml", ".ruff.toml"]
}
```

#### Timestamp Changes
Files modified but content unchanged still trigger cache miss.

**Solution**: Ensure clean working directory
```bash
git status  # Should be clean
```

## Slow Builds

### Symptom
- Builds take longer than expected
- Cache hits but still slow
- "FULL TURBO" but not fast

### Diagnosis

#### 1. Check cache hit rate
```bash
pnpm build

# Look for:
# Cached:    X cached, Y total
# Should be high percentage on unchanged code
```

#### 2. Profile task execution
```bash
# Run with timing
time pnpm build

# Check individual task times in output
```

#### 3. Check for expensive operations
```bash
# Look for tasks that always run
pnpm build --verbosity=2
```

### Optimization

#### 1. Optimize cache keys
```json
// turbo.json
{
  "tasks": {
    "lint": {
      "cache": true,
      "inputs": [
        "**/*.py",           // Only Python files
        "pyproject.toml",    // Config
        ".ruff.toml"         // Ruff config
      ]
      // Don't include: tests/, docs/, etc.
    }
  }
}
```

#### 2. Parallelize independent tasks
```json
{
  "tasks": {
    "lint": {
      "cache": true
      // No dependsOn - runs in parallel
    },
    "test": {
      "cache": true,
      "dependsOn": ["^build"]  // Only depends on build
    }
  }
}
```

#### 3. Use task dependencies wisely
```json
// Bad - unnecessary dependency
{
  "test": {
    "dependsOn": ["lint", "format", "^build"]  // Too many deps
  }
}

// Good - minimal dependencies
{
  "test": {
    "dependsOn": ["^build"]  // Only what's needed
  }
}
```

#### 4. Optimize task outputs
```json
{
  "build": {
    "outputs": [
      "dist/**",           // Only dist files
      "*.egg-info/**"      // And egg-info
    ]
    // Don't include: logs, temp files, etc.
  }
}
```

## Cache Clear Command

### Add to justfile

```bash
# Add this to your justfile
cache-clear:
    @echo "🧹 Clearing Turborepo cache..."
    rm -rf .turbo
    @echo "✅ Cache cleared!"
```

### Usage

```bash
# Clear cache
just cache-clear

# Clear and rebuild
just cache-clear && just build
```

### When to Clear Cache

- ✅ After Turborepo version upgrade
- ✅ When debugging cache issues
- ✅ After changing `turbo.json` configuration
- ✅ When cache behavior seems incorrect
- ❌ Not needed for normal development

## Advanced Troubleshooting

### Inspect Cache Contents

```bash
# List cached tasks
ls -la .turbo/cache/

# View cache metadata
cat .turbo/cache/<hash>.json | jq .
```

### Compare Cache Keys

```bash
# Run task and note cache key
pnpm build --verbosity=2

# Make a change
echo "# comment" >> src/file.py

# Run again and compare keys
pnpm build --verbosity=2
```

### Test Cache Isolation

```bash
# Clear cache
rm -rf .turbo

# Run task
pnpm build

# Modify unrelated file
echo "# comment" >> README.md

# Should still cache hit
pnpm build
```

## Performance Benchmarks

### Expected Performance

| Scenario | Time | Cache Status |
|----------|------|--------------|
| First build | 2-5s | Cache miss |
| No changes | 50-100ms | Cache hit (FULL TURBO) |
| One file changed | 500ms-1s | Partial cache hit |
| Config changed | 2-5s | Cache miss (all tasks) |

### Measuring Improvement

```bash
# Before optimization
time pnpm build

# After optimization
time pnpm build

# Calculate improvement
# (before - after) / before * 100 = % improvement
```

## Best Practices

### Do
- ✅ Include all relevant files in `inputs`
- ✅ Exclude generated files from `inputs`
- ✅ Use specific glob patterns
- ✅ Clear cache when debugging
- ✅ Test cache behavior after config changes

### Don't
- ❌ Manually modify `.turbo/` directory
- ❌ Include too many files in `inputs`
- ❌ Add unnecessary task dependencies
- ❌ Ignore cache misses
- ❌ Commit `.turbo/` to git (already in .gitignore)

## Troubleshooting Checklist

When Turborepo isn't working as expected:

1. **Check configuration**
   ```bash
   cat turbo.json
   ```

2. **Verify clean working directory**
   ```bash
   git status
   ```

3. **Clear cache and test**
   ```bash
   rm -rf .turbo
   pnpm build --force
   ```

4. **Check for generated files**
   ```bash
   find . -name "*.pyc" -o -name "__pycache__"
   ```

5. **Enable verbose logging**
   ```bash
   pnpm build --verbosity=2
   ```

6. **Verify inputs/outputs**
   - Are all relevant files in `inputs`?
   - Are `outputs` correctly specified?
   - Are there unnecessary dependencies?

## Related Documentation

- [Turborepo Guide](../TURBOREPO.md)
- [CI Troubleshooting](./troubleshooting-ci.md)
- [Contributing Guide](../CONTRIBUTING.md)
- [Official Turborepo Docs](https://turbo.build/repo/docs)
