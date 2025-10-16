# Jupyter Notebooks

This directory contains Jupyter notebooks for the ai-kit project, organized by category and governed by security and compliance requirements.

## Quick Start

### Create a New Notebook

```bash
just notebook create
```

Follow the interactive prompts to create a notebook with proper metadata and structure.

### List Notebooks

```bash
just notebook list
```

### Validate a Notebook

```bash
just notebook validate notebooks/exploratory/my-notebook.ipynb
```

## Directory Structure

```
notebooks/
├── exploratory/     # Rapid experimentation (low governance)
├── tutorials/       # Learning materials (medium governance)
├── evaluations/     # Model performance assessment (medium governance)
├── compliance/      # EU AI Act & regulatory docs (high governance)
├── reporting/       # Parameterized reports (medium governance)
└── templates/       # Starter templates for each category
```

## Category Guidelines

### Exploratory
- **Purpose**: Quick experiments, hypothesis testing, one-time analysis
- **Governance**: Low - metadata validation warnings only
- **Lifecycle**: Delete after migrating insights to production
- **SpecKit**: Not required

### Tutorials
- **Purpose**: Learning materials, how-to guides, examples
- **Governance**: Medium - full validation required
- **Lifecycle**: Retained for documentation
- **SpecKit**: Yes - referenced in specs

### Evaluations
- **Purpose**: Model performance assessment, benchmarking
- **Governance**: Medium - full validation required
- **Lifecycle**: Retained and tagged for audit
- **SpecKit**: Yes - documented in plan.md

### Compliance
- **Purpose**: EU AI Act, GDPR, risk assessments, regulatory evidence
- **Governance**: High - full validation required
- **Lifecycle**: Retained and tagged for audit
- **SpecKit**: Yes - documented in plan.md

### Reporting
- **Purpose**: Automated reports, dashboards, recurring analysis
- **Governance**: Medium - full validation required
- **Lifecycle**: Retained for reuse
- **SpecKit**: Not required

## Security Requirements

### ✅ Required: Environment Variables for Credentials

**ALWAYS use environment variables for API keys, tokens, and passwords:**

```python
import os

# ✅ Correct - use environment variables
api_key = os.getenv("OPENGATELLM_API_KEY")
db_password = os.getenv("DATABASE_PASSWORD")
github_token = os.getenv("GITHUB_TOKEN")

# Check if credentials are available
if not api_key:
    raise ValueError("OPENGATELLM_API_KEY environment variable not set")
```

**Set environment variables in your shell**:
```bash
# Add to ~/.zshrc or ~/.bashrc
export OPENGATELLM_API_KEY="your-key-here"
export DATABASE_PASSWORD="your-password-here"

# Or use .env file (never commit this!)
echo "OPENGATELLM_API_KEY=your-key-here" >> .env
```

**Load from .env file in notebooks**:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Load from .env file
api_key = os.getenv("OPENGATELLM_API_KEY")
```

### ✅ Required: Metadata in First Cell

```markdown
**Category**: exploratory
**Purpose**: Analyze customer churn patterns
**Author**: Your Name
**Created**: 2024-10-15
**Data Sources**: data/customers.csv
**Dependencies**: pandas==2.1.0
```

### ✅ Required: External Data References

```python
# ✅ Correct - reference external files
df = pd.read_csv("data/dataset.csv")

# ❌ Forbidden - inline data
# df = pd.DataFrame({"col1": [1, 2, 3], ...})  # Use external files instead
```

### ❌ Forbidden

- **Hardcoded credentials** (blocked by TruffleHog and GitHub Secret Scanning)
  ```python
  # ❌ NEVER DO THIS
  api_key = "sk-proj-abc123..."  # Will be blocked!
  password = "my-secret-password"  # Will be blocked!
  ```

- **Committed outputs** (stripped automatically by nbstripout)

- **Files > 10 MB** (blocked by size-check hook)

### Secret Scanning Best Practices

1. **Use environment variables** for ALL credentials
2. **Never hardcode** API keys, tokens, or passwords
3. **Add .env to .gitignore** (already configured)
4. **Use descriptive variable names**: `OPENGATELLM_API_KEY` not `KEY`
5. **Document required variables** in notebook metadata
6. **Test without credentials** to ensure graceful error handling

## Pre-commit Hooks

When you commit a notebook, these hooks run automatically:

1. **ruff check**: Lints Python code
2. **ruff format**: Formats Python code
3. **nbstripout**: Strips all cell outputs
4. **TruffleHog**: Scans for hardcoded secrets (700+ secret types)
5. **metadata-validation**: Checks required metadata fields
6. **size-check**: Warns at 5 MB, blocks at 10 MB

### Secret Scanning (Defense in Depth)

**Two-layer protection** prevents credential leaks:

**TruffleHog (Local)**: Blocks commits with secrets before they leave your machine
**GitHub Secret Scanning (Remote)**: Blocks pushes with secrets and monitors repository

If a secret is detected, you'll see an error message. **Never commit credentials!**

## Common Commands

```bash
# Create notebook
just notebook create

# List all notebooks
just notebook list

# Validate notebook
just notebook validate notebooks/exploratory/my-notebook.ipynb

# Show statistics
just notebook stats

# Delete notebook (with confirmation)
just notebook delete notebooks/exploratory/old-notebook.ipynb
```

## Documentation

- **Governance Guide**: `docs/notebooks/governance.md` - Detailed policies and requirements
- **Compliance Officer Guide**: `docs/notebooks/compliance-officer-guide.md` - Git tagging workflow
- **Migration Guide**: `docs/notebooks/migration-guide.md` - Notebook-to-production patterns
- **Quickstart**: `specs/002-i-think-we/quickstart.md` - Getting started guide

## Compliance Officer Workflow

For compliance and evaluation notebooks requiring audit trail:

```bash
# Review notebook
jupyter lab notebooks/compliance/model-audit.ipynb

# Create git tag after approval
git tag -a compliance/model-v1.0-audit-2024-10-15 \
  -m "Compliance audit approved - reviewed by [Officer Name]"

# Push tag
git push origin compliance/model-v1.0-audit-2024-10-15

# Discover tags
git tag --list "compliance/*"
git tag --list "evaluations/*"
```

## Getting Help

- **Pre-commit errors**: Check error message for specific fix
- **Category selection**: See decision tree in quickstart.md
- **Compliance questions**: Contact intrapreneur or ALLiaNCE expert
- **Technical issues**: Open issue in ai-kit repository

## Examples

See `notebooks/templates/` for starter notebooks for each category.
