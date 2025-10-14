# Data Model: Jupyter Notebook Support

**Feature**: Jupyter Notebook Support  
**Branch**: `002-i-think-we`  
**Date**: 2025-10-14

## Overview

This document defines the data entities, structures, and relationships for the Jupyter notebook governance infrastructure. Since this is infrastructure tooling (not a database-backed application), the "data model" primarily describes configuration files, metadata structures, and validation schemas.

## Core Entities

### 1. Notebook Metadata

**Description**: Structured metadata embedded in the first markdown cell or notebook-level metadata of every Jupyter notebook.

**Required Fields**:
```python
{
    "category": str,          # One of: exploratory, tutorials, evaluations, compliance, reporting
    "purpose": str,           # What question does this notebook answer?
    "author": str,            # Author name (from git config or manual entry)
    "created": str,           # ISO 8601 date (YYYY-MM-DD)
    "data_sources": list[str], # List of data sources and versions
    "dependencies": list[str]  # List of key dependencies (Python packages, external services)
}
```

**Optional Fields**:
```python
{
    "updated": str,           # ISO 8601 date of last significant update
    "experiment_id": str,     # Reference to experiment tracking system (future)
    "spec_reference": str,    # Link to relevant spec.md file
    "production_code": str,   # Link to production code if migrated
    "git_commit_sha": str,    # Commit SHA before deletion (for exploratory notebooks)
}
```

**Validation Rules**:
- `category` must match one of the six valid categories
- `category` must match the directory where notebook is stored
- `purpose` must be non-empty string (min 10 characters)
- `author` must be non-empty string
- `created` must be valid ISO 8601 date
- `data_sources` and `dependencies` can be empty lists but must be present

**Storage Location**:
- **Option 1 (Preferred)**: First markdown cell with YAML frontmatter
- **Option 2**: Notebook-level metadata (`.ipynb` JSON `metadata` field)

**Example (First Cell Markdown)**:
```markdown
# Model Evaluation: GPT-4 Baseline

**Category**: evaluations  
**Purpose**: Establish baseline performance metrics for GPT-4 on French government FAQ dataset  
**Author**: Marie Dubois  
**Created**: 2024-10-14  
**Data Sources**: 
- `data/faq-dataset-v2.csv` (2024-10-01)
- OpenGateLLM API (production endpoint)

**Dependencies**:
- openai==1.3.0
- pandas==2.1.0
- scikit-learn==1.3.0
```

---

### 2. Notebook Category

**Description**: Defines the governance level and lifecycle rules for notebooks.

**Structure**:
```python
class NotebookCategory:
    name: str                    # Category identifier
    display_name: str            # Human-readable name
    description: str             # Purpose and use cases
    governance_level: str        # low, medium, high
    speckit_required: bool       # Whether SpecKit workflow is required
    retention_policy: str        # delete_after_migration, retain, retain_and_tag
    required_metadata: list[str] # Additional metadata fields beyond base
    template_file: str           # Path to template notebook
```

**Category Definitions**:

| Name | Display Name | Governance | SpecKit | Retention | Template |
|------|--------------|------------|---------|-----------|----------|
| `exploratory` | Exploratory | Low | No | Delete after migration | `exploratory-template.ipynb` |
| `tutorials` | Tutorials | Medium | Yes (referenced in specs) | Retain | `tutorial-template.ipynb` |
| `evaluations` | Evaluations | Medium | Yes (documented in plan.md) | Retain + tag | `evaluation-template.ipynb` |
| `compliance` | Compliance | High | Yes (documented in plan.md) | Retain + tag | `compliance-template.ipynb` |
| `reporting` | Reporting | Medium | No | Retain | `reporting-template.ipynb` |
| `templates` | Templates | N/A | No | Retain | N/A (these ARE the templates) |

**Additional Metadata by Category**:
- **Evaluations**: `model_version`, `evaluation_metrics`, `baseline_comparison`
- **Compliance**: `risk_level`, `regulatory_framework`, `review_date`
- **Reporting**: `parameters`, `schedule`, `recipients`

---

### 3. Pre-commit Hook Configuration

**Description**: Configuration for pre-commit hooks that enforce notebook governance.

**File**: `.pre-commit-config.yaml`

**Structure**:
```yaml
repos:
  - repo: https://github.com/kynan/nbstripout
    rev: 0.6.1
    hooks:
      - id: nbstripout
        files: ^notebooks/.*\.ipynb$
        
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
        files: ^notebooks/.*\.ipynb$
        
  - repo: local
    hooks:
      - id: notebook-metadata-validation
        name: Validate notebook metadata
        entry: uv run python -m notebook_tools.validators
        language: system
        files: ^notebooks/.*\.ipynb$
        pass_filenames: true
        
      - id: notebook-size-check
        name: Check notebook file size
        entry: uv run python -m notebook_tools.validators size
        language: system
        files: ^notebooks/.*\.ipynb$
        pass_filenames: true
```

**Validation Flow**:
1. **nbstripout**: Strip outputs (always runs first)
2. **detect-secrets**: Scan for credentials
3. **metadata-validation**: Check required fields
4. **size-check**: Warn at 5 MB, block at 10 MB

---

### 4. Notebook Template

**Description**: Starter notebook for each category with pre-populated metadata and guidance.

**Structure**:
```python
{
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# {TITLE}\n",
                "\n",
                "**Category**: {CATEGORY}\n",
                "**Purpose**: {PURPOSE}\n",
                "**Author**: {AUTHOR}\n",
                "**Created**: {DATE}\n",
                "**Data Sources**: \n",
                "- [List your data sources]\n",
                "\n",
                "**Dependencies**:\n",
                "- [List key dependencies]\n",
                "\n",
                "## {CATEGORY_SPECIFIC_GUIDANCE}\n"
            ]
        },
        {
            "cell_type": "code",
            "metadata": {},
            "source": [
                "# Standard imports\n",
                "import pandas as pd\n",
                "import numpy as np\n",
                "\n",
                "# {CATEGORY_SPECIFIC_IMPORTS}\n"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 5
}
```

**Template Variables** (replaced by `just create-notebook`):
- `{TITLE}`: User-provided notebook title
- `{CATEGORY}`: Selected category
- `{PURPOSE}`: User-provided purpose
- `{AUTHOR}`: From git config or user input
- `{DATE}`: Current date (ISO 8601)
- `{CATEGORY_SPECIFIC_GUIDANCE}`: Category-specific instructions
- `{CATEGORY_SPECIFIC_IMPORTS}`: Category-specific import suggestions

---

### 5. Git Tag Reference

**Description**: Git tag marking compliance or evaluation notebook milestone for audit.

**Naming Convention**: `{category}/{identifier}-{date}`

**Structure** (conceptual, not a file):
```python
class GitTagReference:
    tag_name: str              # e.g., "compliance/model-v1.0-audit-2024-10-14"
    category: str              # compliance or evaluations
    identifier: str            # model-v1.0-audit
    date: str                  # ISO 8601 date
    notebook_path: str         # Path to tagged notebook
    created_by: str            # Compliance officer name
    commit_sha: str            # Git commit SHA of tagged state
```

**Creation Process**:
1. Compliance officer reviews notebook
2. Officer creates annotated tag: `git tag -a compliance/model-v1.0-audit-2024-10-14 -m "Audit milestone for model v1.0 deployment"`
3. Tag pushed to remote: `git push origin compliance/model-v1.0-audit-2024-10-14`
4. Tag referenced in compliance documentation

**Discovery**:
```bash
# List all compliance tags
git tag --list "compliance/*"

# List all evaluation tags
git tag --list "evaluations/*"

# Show tag details
git show compliance/model-v1.0-audit-2024-10-14
```

---

### 6. Validation Result

**Description**: Result of pre-commit hook validation for a notebook.

**Structure**:
```python
class ValidationResult:
    notebook_path: str
    passed: bool
    errors: list[ValidationError]
    warnings: list[ValidationWarning]
    
class ValidationError:
    code: str                  # e.g., "MISSING_METADATA", "CATEGORY_MISMATCH"
    message: str               # Human-readable error
    field: str                 # Metadata field that failed
    suggestion: str            # How to fix
    
class ValidationWarning:
    code: str                  # e.g., "SIZE_WARNING", "MISSING_OPTIONAL_FIELD"
    message: str
    suggestion: str
```

**Error Codes**:
- `MISSING_METADATA`: Required metadata field missing
- `CATEGORY_MISMATCH`: Category in metadata doesn't match directory
- `INVALID_CATEGORY`: Category not in allowed list
- `EMPTY_PURPOSE`: Purpose field is empty or too short
- `SIZE_EXCEEDED`: Notebook exceeds 10 MB limit
- `CREDENTIALS_DETECTED`: Hardcoded credentials found
- `OUTPUTS_PRESENT`: Cell outputs not stripped (nbstripout failed)

**Warning Codes**:
- `SIZE_WARNING`: Notebook exceeds 5 MB (warning threshold)
- `MISSING_OPTIONAL_FIELD`: Optional metadata field missing
- `LINT_ISSUES`: Ruff linting found code quality issues

---

### 7. CLI Command Configuration

**Description**: Configuration for `just create-notebook` command.

**Structure** (in `packages/notebook-tools/src/notebook_tools/config.py`):
```python
class CLIConfig:
    categories: dict[str, CategoryConfig]
    template_dir: Path
    notebooks_dir: Path
    default_author: str  # From git config
    
class CategoryConfig:
    name: str
    display_name: str
    description: str
    template_file: str
    prompt_text: str
    additional_prompts: list[PromptConfig]
    
class PromptConfig:
    field: str
    prompt_text: str
    default: str | None
    required: bool
    validation: Callable[[str], bool]
```

**Interactive Prompt Flow**:
1. **Category Selection**: List categories with descriptions
2. **Notebook Name**: Validate filename (no spaces, .ipynb extension)
3. **Purpose**: Multi-line input, min 10 characters
4. **Author**: Default from git config, allow override
5. **Category-Specific Prompts**: Based on category configuration
6. **Confirmation**: Show summary, confirm creation

---

## Relationships

```
NotebookCategory (1) -----> (N) NotebookMetadata
    |
    +-----> (1) NotebookTemplate

NotebookMetadata (1) -----> (N) ValidationResult

GitTagReference (1) -----> (1) NotebookMetadata (for compliance/evaluations)

CLIConfig (1) -----> (N) CategoryConfig
    |
    +-----> (1) NotebookTemplate (per category)
```

---

## File System Structure

```
notebooks/
├── exploratory/
│   ├── .gitkeep
│   └── [user notebooks].ipynb
├── tutorials/
│   ├── .gitkeep
│   └── [user notebooks].ipynb
├── evaluations/
│   ├── .gitkeep
│   └── [user notebooks].ipynb
├── compliance/
│   ├── .gitkeep
│   └── [user notebooks].ipynb
├── reporting/
│   ├── .gitkeep
│   └── [user notebooks].ipynb
└── templates/
    ├── exploratory-template.ipynb
    ├── tutorial-template.ipynb
    ├── evaluation-template.ipynb
    ├── compliance-template.ipynb
    └── reporting-template.ipynb
```

---

## State Transitions

### Exploratory Notebook Lifecycle

```
Created (exploratory/) 
  → Developed (outputs stripped on commit)
  → Validated (insights captured)
  → Migrated to production (code extracted to packages/)
  → Deleted (git history preserves)
```

### Compliance/Evaluation Notebook Lifecycle

```
Created (compliance/ or evaluations/)
  → Developed (outputs stripped on commit)
  → Reviewed by compliance officer
  → Tagged for audit (git tag created)
  → Retained in repository (never deleted)
  → Updated if needed (new tag created for new version)
```

---

## Validation State Machine

```
Notebook Commit Attempt
  ↓
nbstripout (strip outputs)
  ↓
detect-secrets (scan for credentials)
  ↓ (if pass)
metadata-validation (check required fields)
  ↓ (if pass)
size-check (warn/block based on size)
  ↓ (if pass)
Commit Allowed
```

---

## Summary

This data model defines the structure and relationships for notebook governance infrastructure. Key design decisions:

1. **Metadata-driven validation**: Required fields enforced by pre-commit hooks
2. **Category-based governance**: Different rules for different notebook purposes
3. **Git-native lifecycle**: Tags for audit, deletion for exploratory work
4. **Template-based creation**: CLI command ensures consistent structure
5. **Validation pipeline**: Multi-stage pre-commit hooks catch issues early

No database or external storage required - all state is in git repository and file system.
