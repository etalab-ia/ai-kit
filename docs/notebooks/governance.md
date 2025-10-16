# Notebook Governance Guide

**Last Updated**: 2025-10-16

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

**Problem**: TruffleHog or GitHub Secret Scanning flags non-secret as credential.

**Solutions**:

**For TruffleHog (local pre-commit)**:
- Review the detected pattern
- If it's a test/example credential, use string concatenation to avoid detection:
  ```python
  # Instead of: api_key = "sk-test-abc123"
  api_key = "sk-test-" + "abc123"  # Breaks pattern matching
  ```

**For GitHub Secret Scanning (push protection)**:
- GitHub will provide a URL to allow the secret if it's a false positive
- Click "Allow this secret" if you're certain it's not a real credential
- Document why it's safe (e.g., "test token in integration test")

### Missing Template

**Problem**: Template not found when creating notebook.

**Solution**: Ensure templates exist in `notebooks/templates/`:
- exploratory-template.ipynb
- tutorial-template.ipynb
- evaluation-template.ipynb
- compliance-template.ipynb
- reporting-template.ipynb

## Pre-commit Hook Workflow

When you commit a notebook, the following hooks run automatically:

1. **ruff check**: Lints Python code
2. **ruff format**: Formats Python code
3. **nbstripout**: Strips all notebook outputs
4. **TruffleHog**: Scans for hardcoded secrets (700+ secret types)
5. **metadata-validation**: Checks required metadata fields
6. **size-check**: Warns at 5MB, blocks at 10MB

If any check fails, fix the issue and commit again.

### Secret Scanning (Defense in Depth)

**Two-layer protection** prevents credential leaks:

**Layer 1: TruffleHog (Local)**
- Runs in pre-commit hook before commit
- Detects 700+ secret types (API keys, tokens, passwords)
- Fast feedback during development
- Filters for verified and unknown results

**Layer 2: GitHub Secret Scanning (Remote)**
- Runs on push to GitHub
- Push protection blocks commits with secrets
- Continuous monitoring of repository
- Validates against 150+ provider patterns

**If TruffleHog blocks your commit**:
```bash
# Error example:
# TruffleHog...............................................................Failed
# - hook id: trufflehog
# - exit code: 183
# 
# Found verified secret: GitHub Personal Access Token
```

**Fix**: Remove the secret and use environment variables:
```python
# ❌ Blocked
api_key = "ghp_abc123..."

# ✅ Correct
import os
api_key = os.getenv("GITHUB_TOKEN")
```

**If GitHub blocks your push**:
```bash
# Error example:
# remote: error: GH013: Repository rule violations found
# remote: - GITHUB PUSH PROTECTION
# remote:   Push cannot contain secrets
```

**Fix**: Either remove the secret or use the provided URL to allow it if it's a false positive.

## Emergency Override

In exceptional cases, skip pre-commit hooks:
```bash
git commit --no-verify
```

**Use sparingly** - hooks catch real problems.

## EU AI Act Compliance Requirements

### High-Risk AI Systems

If your AI system falls under EU AI Act Annex III (high-risk), compliance and evaluation notebooks must address:

**Article 9: Risk Management**
- Identify and analyze risks (bias, discrimination, safety)
- Document mitigation measures
- Evaluate residual risks

**Article 10: Data Governance**
- Document training data sources and characteristics
- Assess data quality and representativeness
- Identify and mitigate biases in data

**Article 11: Technical Documentation**
- System description and intended purpose
- Design specifications and architecture
- Validation and testing procedures

**Article 12: Record-Keeping**
- Automatic logging of events
- Traceability throughout lifecycle

**Article 13: Transparency**
- Users informed of AI system interaction
- Capabilities and limitations communicated

**Article 14: Human Oversight**
- Human oversight measures defined
- Override mechanisms implemented

**Article 15: Accuracy, Robustness, Cybersecurity**
- Accuracy metrics defined and measured
- Robustness testing performed
- Cybersecurity measures implemented

### Required Notebooks for High-Risk Systems

1. **Compliance Notebook** (`notebooks/compliance/`)
   - Complete EU AI Act checklist
   - Risk assessment and mitigation
   - Training data documentation
   - Human oversight procedures

2. **Evaluation Notebook** (`notebooks/evaluations/`)
   - Performance metrics (accuracy, precision, recall)
   - Fairness and bias assessment
   - Robustness testing
   - Validation methodology

### Templates

Both templates include EU AI Act-specific sections:
- `notebooks/templates/compliance-template.ipynb`
- `notebooks/templates/evaluation-template.ipynb`

### Audit Trail

For high-risk systems:
1. Create compliance and evaluation notebooks
2. Have compliance officer review
3. Create git tags for audit trail:
   ```bash
   just notebook tag notebooks/compliance/[notebook].ipynb
   just notebook tag notebooks/evaluations/[notebook].ipynb
   ```
4. Reference tags in homologation dossier

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
