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

### ✅ Required

- **Environment variables for credentials**:
  ```python
  import os
  api_key = os.getenv("API_KEY")
  ```

- **Metadata in first cell**:
  ```markdown
  **Category**: exploratory
  **Purpose**: Analyze customer churn patterns
  **Author**: Your Name
  **Created**: 2024-10-15
  **Data Sources**: data/customers.csv
  **Dependencies**: pandas==2.1.0
  ```

- **External data references**:
  ```python
  df = pd.read_csv("data/dataset.csv")  # Not inline data
  ```

### ❌ Forbidden

- **Hardcoded credentials** (blocked by pre-commit hook)
- **Committed outputs** (stripped automatically)
- **Files > 10 MB** (blocked by pre-commit hook)

## Pre-commit Hooks

When you commit a notebook, these hooks run automatically:

1. **nbstripout**: Strips all cell outputs
2. **detect-secrets**: Scans for hardcoded credentials
3. **metadata-validation**: Checks required metadata fields
4. **size-check**: Warns at 5 MB, blocks at 10 MB

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
