# CLI Interface Contract: Notebook Tools

**Feature**: Jupyter Notebook Support  
**Branch**: `002-i-think-we`  
**Date**: 2025-10-14

## Overview

This document defines the command-line interface contract for notebook tooling. Since this is infrastructure tooling (not a web service), there are no REST APIs. Instead, we define CLI commands, their arguments, and expected behaviors.

---

## Commands

### 1. `just create-notebook`

**Description**: Interactive command to create a new Jupyter notebook from a template with proper metadata.

**Usage**:
```bash
just create-notebook
```

**Interactive Prompts**:

1. **Category Selection**:
   ```
   Select notebook category:
   
   1. Exploratory - Rapid experimentation and hypothesis testing
      • Low governance, no SpecKit workflow required
      • Deleted after migration to production
      
   2. Tutorials - Learning materials and examples
      • Medium governance, referenced in specs
      • Retained for documentation
      
   3. Evaluations - Model performance assessment
      • Medium governance, documented in plan.md
      • Retained and tagged for audit
      
   4. Compliance - EU AI Act and regulatory documentation
      • High governance, documented in plan.md
      • Retained and tagged for audit
      
   5. Reporting - Parameterized stakeholder reports
      • Medium governance, automated execution
      • Retained for recurring use
   
   Enter choice (1-5): _
   ```

2. **Notebook Name**:
   ```
   Enter notebook name (without .ipynb extension): _
   
   Validation:
   - No spaces (use hyphens or underscores)
   - Valid filename characters only
   - Will be saved as: notebooks/{category}/{name}.ipynb
   ```

3. **Purpose**:
   ```
   What question does this notebook answer? (min 10 characters)
   > _
   ```

4. **Author** (optional):
   ```
   Author name [default: {git_config_user_name}]: _
   ```

5. **Category-Specific Prompts** (if applicable):
   
   **For Evaluations**:
   ```
   Model version being evaluated: _
   Baseline for comparison (optional): _
   ```
   
   **For Compliance**:
   ```
   Regulatory framework (e.g., EU AI Act, GDPR): _
   Risk level (low/medium/high): _
   ```
   
   **For Reporting**:
   ```
   Report schedule (e.g., weekly, monthly): _
   Parameters (comma-separated, optional): _
   ```

6. **Confirmation**:
   ```
   Summary:
   - Category: {category}
   - Path: notebooks/{category}/{name}.ipynb
   - Purpose: {purpose}
   - Author: {author}
   
   Create notebook? (y/n): _
   ```

**Success Output**:
```
✓ Created notebook: notebooks/{category}/{name}.ipynb
✓ Metadata populated
✓ Ready to edit

Next steps:
1. Open notebook: jupyter lab notebooks/{category}/{name}.ipynb
2. Add your code and analysis
3. Commit with: git add notebooks/{category}/{name}.ipynb && git commit
```

**Error Cases**:

| Error | Message | Exit Code |
|-------|---------|-----------|
| Invalid category | "Invalid category selection. Please choose 1-5." | 1 |
| Invalid filename | "Notebook name contains invalid characters. Use letters, numbers, hyphens, and underscores only." | 1 |
| File exists | "Notebook already exists at {path}. Choose a different name or delete the existing file." | 1 |
| Empty purpose | "Purpose must be at least 10 characters." | 1 |
| Template not found | "Template file not found: {template_path}. Please check installation." | 1 |

---

### 2. Pre-commit Hook: `notebook-metadata-validation`

**Description**: Validates notebook metadata before commit (invoked automatically by pre-commit framework).

**Usage** (automatic via pre-commit):
```bash
# Triggered automatically on git commit
git commit -m "Add evaluation notebook"

# Manual invocation for testing
uv run python -m notebook_tools.validators metadata notebooks/evaluations/my-notebook.ipynb
```

**Arguments**:
- `notebook_path`: Path to notebook file (passed by pre-commit framework)

**Validation Checks**:
1. Notebook is valid JSON
2. First markdown cell exists
3. Required metadata fields present: `category`, `purpose`, `author`, `created`, `data_sources`, `dependencies`
4. Category matches directory location
5. Purpose is non-empty (min 10 characters)
6. Created date is valid ISO 8601 format

**Success Output** (silent):
```
# No output on success (pre-commit convention)
```

**Error Output**:
```
Notebook metadata validation failed: notebooks/evaluations/my-notebook.ipynb

Errors:
  ✗ Missing required field: 'purpose'
  ✗ Category mismatch: metadata says 'exploratory' but file is in 'evaluations/'

Fix these issues and try again.

Example metadata format:
**Category**: evaluations
**Purpose**: Establish baseline performance metrics
**Author**: Your Name
**Created**: 2024-10-14
**Data Sources**: 
- data/dataset.csv
**Dependencies**:
- pandas==2.1.0
```

**Exit Codes**:
- `0`: Validation passed
- `1`: Validation failed (blocks commit)

---

### 3. Pre-commit Hook: `notebook-size-check`

**Description**: Checks notebook file size and warns/blocks based on thresholds.

**Usage** (automatic via pre-commit):
```bash
# Triggered automatically on git commit
git commit -m "Add notebook"

# Manual invocation
uv run python -m notebook_tools.validators size notebooks/exploratory/large-notebook.ipynb
```

**Arguments**:
- `notebook_path`: Path to notebook file

**Thresholds**:
- **Warning**: 5 MB (allows commit but prints warning)
- **Block**: 10 MB (prevents commit)

**Warning Output** (size > 5 MB, < 10 MB):
```
⚠ Warning: Notebook size is 6.2 MB

Large notebooks can slow down git operations and may contain embedded data.
Consider:
- Externalizing data to data/ directory
- Removing large embedded plots
- Using data references instead of inline data

Commit will proceed, but please review notebook size.
```

**Error Output** (size ≥ 10 MB):
```
✗ Error: Notebook size is 12.5 MB (exceeds 10 MB limit)

Notebooks must be under 10 MB to prevent repository bloat.

Solutions:
1. Move data to external files in data/ directory
2. Remove embedded large datasets
3. Use data references (URLs, file paths) instead of inline data
4. Remove unnecessary embedded images/plots

After fixing, try commit again.
```

**Exit Codes**:
- `0`: Size OK or warning only
- `1`: Size exceeds 10 MB (blocks commit)

---

### 4. Pre-commit Hook: `nbstripout`

**Description**: Strips notebook outputs before commit (third-party tool).

**Usage** (automatic via pre-commit):
```bash
# Configured in .pre-commit-config.yaml
# Runs automatically on git commit
```

**Behavior**:
- Removes all cell outputs
- Removes execution counts
- Preserves cell source code
- Preserves metadata
- Silent on success

**Configuration** (in `.pre-commit-config.yaml`):
```yaml
- repo: https://github.com/kynan/nbstripout
  rev: 0.6.1
  hooks:
    - id: nbstripout
      files: ^notebooks/.*\.ipynb$
```

---

### 5. Pre-commit Hook: `detect-secrets`

**Description**: Scans notebooks for hardcoded credentials (third-party tool).

**Usage** (automatic via pre-commit):
```bash
# Configured in .pre-commit-config.yaml
# Runs automatically on git commit
```

**Behavior**:
- Scans notebook JSON for credential patterns
- Checks against baseline file (`.secrets.baseline`)
- Blocks commit if new secrets detected

**Error Output**:
```
detect-secrets.............................................Failed
- hook id: detect-secrets
- exit code: 1

Potential secrets detected in notebooks/exploratory/my-notebook.ipynb:

Line 15: AWS Access Key ID
Line 23: Generic API Key

If these are false positives, add them to .secrets.baseline:
  detect-secrets scan --baseline .secrets.baseline

Otherwise, remove the credentials and use environment variables.
```

**Configuration** (in `.pre-commit-config.yaml`):
```yaml
- repo: https://github.com/Yelp/detect-secrets
  rev: v1.4.0
  hooks:
    - id: detect-secrets
      args: ['--baseline', '.secrets.baseline']
      files: ^notebooks/.*\.ipynb$
```

---

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `NOTEBOOKS_DIR` | Root directory for notebooks | `notebooks/` | No |
| `TEMPLATES_DIR` | Directory containing templates | `notebooks/templates/` | No |
| `GIT_AUTHOR_NAME` | Default author name | From git config | No |
| `SKIP_METADATA_VALIDATION` | Skip metadata validation (emergency) | `false` | No |

---

## Exit Code Conventions

| Code | Meaning | Usage |
|------|---------|-------|
| 0 | Success | Command completed successfully |
| 1 | Validation error | Pre-commit hook failed, blocks commit |
| 2 | User cancellation | User cancelled interactive prompt |
| 3 | System error | File I/O error, template missing, etc. |

---

## Integration with Git Workflow

### Normal Workflow

```bash
# 1. Create notebook
just create-notebook
# → Interactive prompts
# → Creates notebooks/evaluations/my-evaluation.ipynb

# 2. Edit notebook
jupyter lab notebooks/evaluations/my-evaluation.ipynb
# → Add code, run cells, generate outputs

# 3. Commit notebook
git add notebooks/evaluations/my-evaluation.ipynb
git commit -m "Add baseline evaluation for GPT-4"

# Pre-commit hooks run automatically:
# ✓ nbstripout (strips outputs)
# ✓ detect-secrets (scans for credentials)
# ✓ metadata-validation (checks required fields)
# ✓ size-check (warns if > 5 MB, blocks if > 10 MB)

# 4. Push to remote
git push origin 002-i-think-we
```

### Compliance Officer Workflow (Git Tagging)

```bash
# 1. Review compliance notebook
jupyter lab notebooks/compliance/model-v1-audit.ipynb

# 2. Verify compliance requirements met
# (manual review process)

# 3. Create annotated tag
git tag -a compliance/model-v1.0-audit-2024-10-14 \
  -m "Audit milestone for model v1.0 deployment - reviewed by Marie Dubois"

# 4. Push tag to remote
git push origin compliance/model-v1.0-audit-2024-10-14

# 5. Tag is now discoverable for audit
git tag --list "compliance/*"
```

---

## Error Handling Philosophy

1. **Fail fast**: Catch errors before commit, not after
2. **Clear messages**: Explain what's wrong and how to fix it
3. **Actionable**: Provide specific commands or steps to resolve
4. **Non-blocking warnings**: Allow commit with warnings for non-critical issues
5. **Emergency escape**: Provide `--skip` flags for exceptional cases (documented but discouraged)

---

## Future Extensions

### Planned (not in initial scope):

1. **`just validate-notebook <path>`**: Manual validation without commit
2. **`just list-notebooks [category]`**: List notebooks by category
3. **`just notebook-stats`**: Show notebook statistics (count by category, sizes, etc.)
4. **`just migrate-notebook <path>`**: Document migration to production
5. **Experiment tracking integration**: Log notebook execution to tracking system

---

## Summary

This CLI interface provides:
- **Interactive creation**: `just create-notebook` guides developers through setup
- **Automated validation**: Pre-commit hooks enforce governance rules
- **Clear feedback**: Error messages explain issues and solutions
- **Git-native workflow**: Integrates seamlessly with existing git practices
- **Compliance support**: Git tagging workflow for audit trail

No REST APIs or external services required - all tooling is local and git-based.
