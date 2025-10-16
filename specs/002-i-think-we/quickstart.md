# Quickstart: Jupyter Notebook Support

**Feature**: Jupyter Notebook Support  
**Last Updated**: 2025-10-14

## Overview

This guide helps you get started with Jupyter notebooks in ai-kit. Learn how to create, organize, and manage notebooks while following security and compliance requirements.

---

## Prerequisites

- ai-kit repository cloned and set up
- Pre-commit hooks installed: `pre-commit install`
- Jupyter Lab or Jupyter Notebook installed: `uv add --dev jupyter`

---

## Quick Start (5 minutes)

### 1. Create Your First Notebook

```bash
# Run the interactive notebook creation command
just create-notebook
```

You'll be prompted to:
1. **Choose a category** (exploratory, tutorials, evaluations, compliance, or reporting)
2. **Name your notebook** (e.g., `my-first-analysis`)
3. **Describe its purpose** (what question does it answer?)
4. **Confirm your author name** (defaults to your git config)

The command creates a notebook with proper metadata and structure.

### 2. Edit Your Notebook

```bash
# Open Jupyter Lab
jupyter lab notebooks/exploratory/my-first-analysis.ipynb
```

Add your code, run cells, and generate outputs as usual.

### 3. Commit Your Notebook

```bash
# Add and commit
git add notebooks/exploratory/my-first-analysis.ipynb
git commit -m "Add exploratory analysis"
```

**What happens automatically:**
- ✅ Cell outputs are stripped (keeps repository clean)
- ✅ Credentials are scanned (prevents accidental leaks)
- ✅ Metadata is validated (ensures proper documentation)
- ✅ File size is checked (warns if > 5 MB, blocks if > 10 MB)

If any checks fail, you'll get clear error messages explaining how to fix them.

---

## Choosing the Right Category

### Decision Tree

```
What's the notebook's purpose?

├─ Quick experiment or hypothesis testing?
│  └─ Use: exploratory/
│     • No SpecKit workflow required
│     • Delete after migrating insights to production
│
├─ Teaching others how to use a feature?
│  └─ Use: tutorials/
│     • Link from relevant spec.md files
│     • Kept for documentation
│
├─ Evaluating model performance?
│  └─ Use: evaluations/
│     • Document metrics and validation
│     • Kept and tagged for audit
│
├─ Documenting compliance requirements?
│  └─ Use: compliance/
│     • EU AI Act, GDPR, risk assessments
│     • Kept and tagged for regulatory review
│
└─ Generating recurring stakeholder reports?
   └─ Use: reporting/
      • Parameterized for automation
      • Kept for reuse
```

### Category Details

| Category | When to Use | Governance | Lifecycle |
|----------|-------------|------------|-----------|
| **exploratory/** | Rapid experiments, hypothesis testing, one-time analysis | Low | Delete after migration |
| **tutorials/** | Learning materials, how-to guides, examples | Medium | Retain, link from specs |
| **evaluations/** | Model performance assessment, benchmarking | Medium | Retain, tag for audit |
| **compliance/** | EU AI Act docs, risk assessments, regulatory evidence | High | Retain, tag for audit |
| **reporting/** | Automated reports, dashboards, recurring analysis | Medium | Retain for reuse |

---

## Common Workflows

### Exploratory Analysis → Production Code

1. **Create exploratory notebook**:
   ```bash
   just create-notebook
   # Choose: 1 (Exploratory)
   # Name: customer-segmentation-experiment
   ```

2. **Experiment and iterate**:
   ```bash
   jupyter lab notebooks/exploratory/customer-segmentation-experiment.ipynb
   # Try different approaches, visualize results
   ```

3. **Extract validated code to production**:
   ```bash
   # Create package for production code
   mkdir -p packages/customer-segmentation/src/customer_segmentation
   
   # Extract reusable functions from notebook
   # Add tests, documentation
   ```

4. **Document migration in feature spec**:
   ```markdown
   ## Implementation Notes
   
   Insights from `notebooks/exploratory/customer-segmentation-experiment.ipynb`
   (commit SHA: abc123) were extracted to `packages/customer-segmentation/`.
   
   Key findings:
   - K-means with k=5 provided best silhouette score
   - Feature scaling critical for performance
   ```

5. **Delete exploratory notebook**:
   ```bash
   git rm notebooks/exploratory/customer-segmentation-experiment.ipynb
   git commit -m "Migrate customer segmentation to production (see spec.md)"
   ```

   Git history preserves the notebook if you need to reference it later.

---

### Model Evaluation for Compliance

1. **Create evaluation notebook**:
   ```bash
   just create-notebook
   # Choose: 3 (Evaluations)
   # Name: gpt4-baseline-evaluation
   # Model version: gpt-4-turbo-2024-04-09
   ```

2. **Document evaluation methodology**:
   ```python
   # In notebook:
   # - Load test dataset
   # - Run model inference
   # - Calculate metrics (accuracy, F1, bias metrics)
   # - Compare to baseline
   # - Document findings
   ```

3. **Commit evaluation results**:
   ```bash
   git add notebooks/evaluations/gpt4-baseline-evaluation.ipynb
   git commit -m "Add GPT-4 baseline evaluation on FAQ dataset"
   git push
   ```

4. **Request compliance review**:
   - Notify compliance officer (intrapreneur or ALLiaNCE expert)
   - Officer reviews notebook for completeness
   - Officer creates git tag when approved:
     ```bash
     git tag -a evaluations/gpt4-baseline-2024-10-14 \
       -m "Baseline evaluation approved for production deployment"
     git push origin evaluations/gpt4-baseline-2024-10-14
     ```

5. **Reference in compliance documentation**:
   ```markdown
   ## Model Evaluation Evidence
   
   Baseline evaluation documented in:
   - Notebook: `notebooks/evaluations/gpt4-baseline-evaluation.ipynb`
   - Git tag: `evaluations/gpt4-baseline-2024-10-14`
   - Metrics: 94% accuracy, F1=0.92, bias score=0.03
   ```

---

### Creating a Tutorial

1. **Create tutorial notebook**:
   ```bash
   just create-notebook
   # Choose: 2 (Tutorials)
   # Name: using-opengatellm-api
   ```

2. **Write clear, documented tutorial**:
   ```python
   # In notebook:
   # - Step-by-step instructions
   # - Code examples with explanations
   # - Expected outputs (as markdown, not cell outputs)
   # - Common pitfalls and solutions
   ```

3. **Link from feature spec**:
   ```markdown
   ## Quickstart
   
   See tutorial notebook: `notebooks/tutorials/using-opengatellm-api.ipynb`
   
   This tutorial covers:
   - Authentication setup
   - Basic API calls
   - Error handling
   - Best practices
   ```

4. **Keep tutorial updated**:
   - Update when API changes
   - Add new examples as needed
   - Tutorial stays in repository (never deleted)

---

## Security Best Practices

### ✅ DO

- **Use environment variables for credentials**:
  ```python
  import os
  api_key = os.getenv("OPENGATELLM_API_KEY")
  ```

- **Document data sources with versions**:
  ```markdown
  **Data Sources**:
  - `data/faq-dataset-v2.csv` (2024-10-01)
  - OpenGateLLM API (production endpoint)
  ```

- **Keep notebooks under 10 MB**:
  - Externalize data to `data/` directory
  - Use data references instead of inline data

### ❌ DON'T

- **Never hardcode credentials**:
  ```python
  # ❌ BAD - will be blocked by pre-commit hook
  api_key = "sk-proj-abc123..."
  
  # ✅ GOOD
  api_key = os.getenv("OPENGATELLM_API_KEY")
  ```

- **Don't commit large datasets in notebooks**:
  ```python
  # ❌ BAD - bloats repository
  df = pd.DataFrame({...huge inline data...})
  
  # ✅ GOOD - reference external file
  df = pd.read_csv("data/dataset.csv")
  ```

- **Don't skip pre-commit hooks** (except emergencies):
  ```bash
  # ❌ Avoid unless absolutely necessary
  git commit --no-verify
  
  # ✅ Fix the issues instead
  # Pre-commit hooks catch real problems
  ```

---

## Troubleshooting

### "Missing required field: 'purpose'"

**Problem**: Notebook metadata is incomplete.

**Solution**: Add metadata to the first markdown cell:
```markdown
# My Notebook Title

**Category**: exploratory
**Purpose**: Analyze customer churn patterns to identify key drivers
**Author**: Your Name
**Created**: 2024-10-14
**Data Sources**: 
- data/customers.csv
**Dependencies**:
- pandas==2.1.0
- scikit-learn==1.3.0
```

---

### "Category mismatch: metadata says 'exploratory' but file is in 'evaluations/'"

**Problem**: Notebook is in wrong directory or metadata is wrong.

**Solution**: Either move the notebook or update the metadata:
```bash
# Option 1: Move notebook to match metadata
git mv notebooks/evaluations/my-notebook.ipynb notebooks/exploratory/

# Option 2: Update metadata to match directory
# Edit first cell to say: **Category**: evaluations
```

---

### "Notebook size is 12.5 MB (exceeds 10 MB limit)"

**Problem**: Notebook file is too large (usually embedded data or plots).

**Solution**:
1. **Externalize data**:
   ```python
   # Instead of inline data
   df = pd.read_csv("data/large-dataset.csv")
   ```

2. **Remove large embedded plots**:
   ```python
   # Save plots to files instead
   plt.savefig("outputs/plot.png")
   plt.close()
   ```

3. **Use data references**:
   ```python
   # Reference external resources
   data_url = "https://data.gouv.fr/dataset/..."
   ```

---

### "Potential secrets detected"

**Problem**: Pre-commit hook found what looks like a credential.

**Solution**:

1. **If it's a real credential**: Remove it and use environment variables
   ```python
   # Remove hardcoded credential
   # Add to .env file (not committed)
   # Load with: os.getenv("API_KEY")
   ```

2. **If it's a false positive**: Add to baseline
   ```bash
   detect-secrets scan --baseline .secrets.baseline
   git add .secrets.baseline
   git commit -m "Update secrets baseline"
   ```

---

## For Compliance Officers

### Reviewing and Tagging Notebooks

1. **Review notebook for completeness**:
   - All required metadata present
   - Methodology clearly documented
   - Results reproducible
   - Meets regulatory requirements (EU AI Act, GDPR)

2. **Create git tag when approved**:
   ```bash
   # Format: {category}/{identifier}-{date}
   git tag -a compliance/model-v1.0-audit-2024-10-14 \
     -m "Compliance audit approved for model v1.0 - reviewed by [Your Name]"
   
   git push origin compliance/model-v1.0-audit-2024-10-14
   ```

3. **Discover tagged notebooks**:
   ```bash
   # List all compliance tags
   git tag --list "compliance/*"
   
   # List all evaluation tags
   git tag --list "evaluations/*"
   
   # Show tag details
   git show compliance/model-v1.0-audit-2024-10-14
   ```

4. **Reference in compliance documentation**:
   - Include tag name in homologation dossier
   - Link to specific commit SHA
   - Document review date and reviewer

---

## Next Steps

- **Read governance guide**: `docs/notebooks/governance.md` (detailed policies)
- **See compliance officer guide**: `docs/notebooks/compliance-officer-guide.md` (tagging workflow)
- **Learn migration patterns**: `docs/notebooks/migration-guide.md` (notebook → production)
- **Browse templates**: `notebooks/templates/` (starter notebooks for each category)

---

## Getting Help

- **Pre-commit hook errors**: Check error message for specific fix
- **Category selection**: Use decision tree above or ask team
- **Compliance questions**: Contact intrapreneur or ALLiaNCE expert
- **Technical issues**: Open issue in ai-kit repository

---

## Summary

**Creating notebooks**: `just create-notebook` → interactive prompts → ready to use

**Committing notebooks**: Automatic validation ensures security and quality

**Lifecycle management**: 
- Exploratory → delete after migration
- Compliance/Evaluations → retain and tag for audit
- Tutorials/Reporting → retain for reuse

**Security**: No credentials, outputs stripped, size limits enforced

**Compliance**: Git tags provide audit trail, reviewed by compliance officers

Start with exploratory notebooks to experiment, then migrate validated insights to production code!
