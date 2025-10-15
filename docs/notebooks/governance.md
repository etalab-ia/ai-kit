# Notebook Governance Guide

**Last Updated**: 2025-10-15

## Overview

This guide defines governance policies for Jupyter notebooks in ai-kit. It ensures security, reproducibility, and compliance with EU AI Act requirements.

## Security Requirements

### Credential Management

**MANDATORY**: Never commit hardcoded credentials to notebooks.

✅ **Correct approach**:
```python
import os
api_key = os.getenv("OPENGATELLM_API_KEY")
```

❌ **Forbidden**:
```python
api_key = "sk-proj-abc123..."  # Will be blocked by pre-commit hook
```

### Output Stripping

All notebook outputs are automatically stripped before commit via `nbstripout` pre-commit hook. This:
- Keeps repository clean and diff-friendly
- Prevents accidental data leakage
- Reduces repository size

### File Size Limits

- **Warning threshold**: 5 MB
- **Block threshold**: 10 MB

Large notebooks indicate embedded data. Solutions:
1. Move data to `data/` directory
2. Use data references (URLs, file paths)
3. Remove unnecessary embedded images

## Category Governance Levels

### Exploratory (Low Governance)

- **Purpose**: Rapid experimentation, hypothesis testing
- **SpecKit required**: No
- **Lifecycle**: Delete after migration to production
- **Pre-commit**: Metadata validation (warning only)

**Best practices**:
- Document key findings before deletion
- Capture commit SHA in migration notes
- Extract validated code to packages

### Tutorials (Medium Governance)

- **Purpose**: Learning materials, how-to guides
- **SpecKit required**: Yes (referenced in specs)
- **Lifecycle**: Retain for documentation
- **Pre-commit**: Full validation (blocking)

**Best practices**:
- Link from relevant spec.md files
- Keep updated with API changes
- Clear step-by-step explanations

### Evaluations (Medium Governance)

- **Purpose**: Model performance assessment
- **SpecKit required**: Yes (documented in plan.md)
- **Lifecycle**: Retain and tag for audit
- **Pre-commit**: Full validation (blocking)

**Best practices**:
- Document evaluation methodology
- Include baseline comparisons
- Request compliance officer review for production decisions

### Compliance (High Governance)

- **Purpose**: EU AI Act, GDPR, regulatory documentation
- **SpecKit required**: Yes (documented in plan.md)
- **Lifecycle**: Retain and tag for audit
- **Pre-commit**: Full validation (blocking)

**Best practices**:
- Complete all checklist items
- Request compliance officer review
- Create git tag after approval

### Reporting (Medium Governance)

- **Purpose**: Automated stakeholder reports
- **SpecKit required**: No
- **Lifecycle**: Retain for recurring use
- **Pre-commit**: Full validation (blocking)

**Best practices**:
- Use papermill parameters
- Document schedule and recipients
- Test automated execution

## Metadata Requirements

All notebooks must include metadata in the first markdown cell:

```markdown
# Notebook Title

**Category**: [category]
**Purpose**: [What question does this answer?]
**Author**: [Your Name]
**Created**: [YYYY-MM-DD]
**Data Sources**: 
- [List data sources and versions]

**Dependencies**:
- [List key dependencies with versions]
```

### Category-Specific Metadata

**Evaluations**:
- Model Version
- Evaluation Metrics
- Baseline Comparison

**Compliance**:
- Risk Level
- Regulatory Framework
- Review Date

**Reporting**:
- Parameters
- Schedule
- Recipients

## Reproducibility Best Practices

### Dependency Documentation

**All notebooks must document dependencies with exact versions** to ensure reproducibility.

✅ **Correct approach**:
```markdown
**Dependencies**:
```
pandas>=2.1.0
scikit-learn>=1.3.0
openai>=1.3.0
```

**Environment**:
- Python: 3.12+
- Workspace: ai-kit (uv workspace)
```

**Add to project dependencies**:
```bash
# Add to pyproject.toml
uv add pandas scikit-learn openai
```

### Data Source Documentation

**Document all data sources with complete access information**:

```markdown
**Data Sources**:
- Path: `data/faq-dataset-v2.csv`
- Version/Date: 2024-10-01
- Access method: Local file / API / Database
- Size: ~2.5 MB
- Schema: id (int), question (str), answer (str), category (str)
```

**Best practices**:
- Include data version or snapshot date
- Document access credentials location (env vars)
- Note data refresh schedule for automated reports
- Link to data documentation or schema

### Environment Reproducibility

**Use uv workspace for consistent environments**:

```bash
# Sync all dependencies
uv sync

# Run notebook with correct environment
jupyter lab
```

**Python version** is pinned in `.python-version` (3.12+).

### Parameterized Execution with Papermill

**Reporting notebooks support parameterized execution** for automation.

**1. Tag parameters cell**:
```python
# Cell tagged with "parameters" in notebook metadata
start_date = '2024-01-01'
end_date = '2024-01-31'
output_format = 'html'
```

**2. Run with CLI** (recommended):
```bash
# Execute notebook with parameters
just notebook run input.ipynb output.ipynb \
  -p start_date=2024-02-01 \
  -p end_date=2024-02-28 \
  -p output_format=pdf

# Convert to HTML report
just notebook convert output.ipynb html

# Convert to PDF (requires pandoc + LaTeX)
just notebook convert output.ipynb pdf -o report.pdf

# Convert to Python script
just notebook convert output.ipynb script
```

**Alternative: Direct papermill usage**:
```bash
# Run with papermill directly
papermill input.ipynb output.ipynb \
  -p start_date '2024-02-01' \
  -p end_date '2024-02-28'

# Convert with nbconvert directly
jupyter nbconvert output.ipynb --to html
```

**Automation example**:
```bash
# Weekly automated report
just notebook run reporting/weekly-metrics.ipynb \
  output/metrics-$(date +%Y-%m-%d).ipynb \
  -p start_date=$(date -d '7 days ago' +%Y-%m-%d) \
  -p end_date=$(date +%Y-%m-%d)

# Generate HTML report
just notebook convert output/metrics-$(date +%Y-%m-%d).ipynb html
```

**Available conversion formats**:
- `html` - HTML report (default)
- `pdf` - PDF report (requires pandoc + LaTeX)
- `markdown` - Markdown document
- `script` - Python script (.py)
- `slides` - HTML slides (reveal.js)

### Code Quality with nbqa

**Optional: Lint notebook code cells with ruff**:

```bash
# Manual linting (not enforced by pre-commit)
pre-commit run nbqa-ruff --files notebooks/exploratory/my-notebook.ipynb
```

This helps maintain code quality but is **non-blocking** to allow exploratory work.

## Migration to Production

### Exploratory → Production Workflow

1. **Validate insights** in exploratory notebook
2. **Extract code** to appropriate package:
   ```bash
   mkdir -p packages/my-feature/src/my_feature
   # Extract functions, add tests
   ```
3. **Document migration** in feature spec:
   ```markdown
   Insights from `notebooks/exploratory/experiment.ipynb` 
   (commit SHA: abc123) migrated to `packages/my-feature/`.
   ```
4. **Delete notebook**:
   ```bash
   git rm notebooks/exploratory/experiment.ipynb
   git commit -m "Migrate experiment to production"
   ```

Git history preserves the notebook for future reference.

### Compliance/Evaluation Retention

Compliance and evaluation notebooks are **never deleted**. They provide audit trail for regulatory compliance.

## Git Tagging for Audit

Compliance officers create git tags for audit milestones:

```bash
# Format: {category}/{identifier}-{date}
git tag -a compliance/model-v1.0-audit-2024-10-14 \
  -m "Compliance audit approved - reviewed by [Officer Name]"

git push origin compliance/model-v1.0-audit-2024-10-14
```

Discover tags:
```bash
git tag --list "compliance/*"
git tag --list "evaluations/*"
```

## Edge Cases

### Notebook in Wrong Directory

**Problem**: Notebook category doesn't match directory.

**Solution**: Move notebook or update metadata:
```bash
git mv notebooks/evaluations/notebook.ipynb notebooks/exploratory/
# OR update first cell: **Category**: exploratory
```

### Large Embedded Datasets

**Problem**: Notebook exceeds size limits due to embedded data.

**Solutions**:
1. Externalize to `data/` directory
2. Use data references (URLs)
3. Sample data for demonstration

### False Positive Secret Detection

**Problem**: Pre-commit hook flags non-secret as credential.

**Solution**: Update baseline:
```bash
detect-secrets scan --baseline .secrets.baseline
git add .secrets.baseline
git commit -m "Update secrets baseline"
```

### Missing Template

**Problem**: Template not found when creating notebook.

**Solution**: Ensure templates exist in `notebooks/templates/`:
- exploratory-template.ipynb
- tutorial-template.ipynb
- evaluation-template.ipynb
- compliance-template.ipynb
- reporting-template.ipynb

## Pre-commit Hook Workflow

When you commit a notebook:

1. **nbstripout**: Strips all outputs
2. **detect-secrets**: Scans for credentials
3. **metadata-validation**: Checks required fields
4. **size-check**: Warns/blocks based on size

If any check fails, fix the issue and commit again.

## Emergency Override

In exceptional cases, skip pre-commit hooks:
```bash
git commit --no-verify
```

**Use sparingly** - hooks catch real problems.

## Compliance Officer Responsibilities

1. **Review notebooks** for completeness and regulatory compliance
2. **Create git tags** for audit milestones
3. **Document reviews** in compliance documentation
4. **Maintain audit trail** for homologation dossiers

See: `docs/notebooks/compliance-officer-guide.md`

## Questions?

- **Pre-commit errors**: Check error message for specific fix
- **Category selection**: See decision tree in quickstart.md
- **Compliance questions**: Contact intrapreneur or ALLiaNCE expert
- **Technical issues**: Open issue in ai-kit repository
