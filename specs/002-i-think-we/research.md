# Research: Jupyter Notebook Support

**Feature**: Jupyter Notebook Support  
**Branch**: `002-i-think-we`  
**Date**: 2025-10-14

## Overview

This document captures technical research and decisions for implementing Jupyter notebook governance infrastructure in ai-kit. Research focuses on tooling selection, best practices for notebook management in git repositories, and integration patterns with existing monorepo tooling.

## Research Areas

### 1. Notebook Output Stripping (nbstripout)

**Decision**: Use `nbstripout` as pre-commit hook

**Rationale**:
- Industry-standard tool for stripping notebook outputs before commit
- Lightweight Python package, easy to integrate with pre-commit framework
- Configurable to preserve specific outputs if needed (though we won't use this)
- Widely adopted in data science teams (10k+ GitHub stars)
- Actively maintained and compatible with Jupyter notebook format changes

**Alternatives Considered**:
- **Manual stripping**: Rejected - too error-prone, relies on developer discipline
- **Git filters**: Rejected - more complex setup, less discoverable than pre-commit hooks
- **Custom script**: Rejected - reinventing the wheel, nbstripout is battle-tested

**Implementation Notes**:
- Add to `.pre-commit-config.yaml` with `nbstripout` hook
- Configure to run on all `.ipynb` files in `notebooks/` directory
- No special configuration needed - default behavior strips all outputs

**References**:
- [nbstripout GitHub](https://github.com/kynan/nbstripout)
- [Pre-commit framework](https://pre-commit.com/)

---

### 2. Secret Scanning (detect-secrets vs gitleaks)

**Decision**: Use `detect-secrets` as primary tool, with option to add `gitleaks` later

**Rationale**:
- **detect-secrets** advantages:
  - Python-native (aligns with Principle X)
  - Integrates seamlessly with pre-commit framework
  - Supports custom plugins for French government-specific patterns (ProConnect tokens, OpenGateLLM keys)
  - Baseline file approach reduces false positives
  - Actively maintained by Yelp
  
- **gitleaks** advantages:
  - Go-based, very fast
  - Comprehensive default ruleset
  - Good for CI/CD scanning of entire history
  
- **Hybrid approach**: Start with detect-secrets for pre-commit, consider gitleaks for CI/CD full-repo scans

**Alternatives Considered**:
- **git-secrets** (AWS): Rejected - less actively maintained, AWS-focused
- **truffleHog**: Rejected - entropy-based detection causes many false positives
- **Custom regex**: Rejected - insufficient coverage, maintenance burden

**Implementation Notes**:
- Add `detect-secrets` to `.pre-commit-config.yaml`
- Create `.secrets.baseline` file to track known false positives
- Configure to scan all files in `notebooks/` directory
- Document process for adding French government-specific patterns

**References**:
- [detect-secrets GitHub](https://github.com/Yelp/detect-secrets)
- [gitleaks GitHub](https://github.com/gitleaks/gitleaks)

---

### 3. Notebook Linting (ruff + nbqa)

**Decision**: Use `ruff` via `nbqa` for linting notebook code cells

**Rationale**:
- `ruff` is already standardized in ai-kit (Principle IX)
- `nbqa` enables running any Python tool on Jupyter notebooks
- Fast execution (Rust-based ruff)
- Consistent code quality across notebooks and Python modules
- Configurable to ignore notebook-specific patterns (e.g., `# %%` cell markers)

**Alternatives Considered**:
- **flake8 + nbqa**: Rejected - ruff is faster and already standardized
- **No linting**: Rejected - code quality important even for exploratory work
- **Notebook-specific linters**: Rejected - no mature options, prefer consistency with main codebase

**Implementation Notes**:
- Add `nbqa` as dev dependency in `packages/notebook-tools/`
- Configure ruff to run via nbqa in pre-commit hooks (optional, not blocking)
- Use same `.ruff.toml` configuration as main codebase
- Make linting non-blocking for exploratory notebooks, blocking for compliance/evaluation

**References**:
- [nbqa GitHub](https://github.com/nbQA-dev/nbQA)
- [ruff documentation](https://docs.astral.sh/ruff/)

---

### 4. Parameterized Notebook Execution (papermill)

**Decision**: Use `papermill` for parameterized execution of reporting notebooks

**Rationale**:
- Industry-standard tool from Netflix for notebook parameterization
- Enables automated execution with different parameters
- Supports output to different formats (HTML, PDF via nbconvert)
- Integrates well with CI/CD pipelines
- Actively maintained by nteract project

**Alternatives Considered**:
- **nbconvert alone**: Rejected - no parameterization support
- **Custom execution script**: Rejected - papermill handles edge cases (errors, timeouts)
- **Jupyter nbclient**: Rejected - lower-level API, papermill is higher-level wrapper

**Implementation Notes**:
- Add `papermill` as dependency for reporting notebook execution
- Document parameterization patterns in reporting template
- Provide example justfile command for executing parameterized reports
- Consider integration with future experiment tracking system

**References**:
- [papermill GitHub](https://github.com/nteract/papermill)
- [papermill documentation](https://papermill.readthedocs.io/)

---

### 5. Notebook Metadata Validation

**Decision**: Implement custom pre-commit hook for metadata validation

**Rationale**:
- No existing tool validates Jupyter notebook metadata fields
- Simple Python script can parse `.ipynb` JSON and check first cell
- Enables enforcement of category-specific requirements (FR-018a, FR-018b)
- Can provide clear error messages guiding developers to fix issues

**Implementation Approach**:
- Create `packages/notebook-tools/src/notebook_tools/validators.py`
- Parse notebook JSON, extract first markdown cell or notebook-level metadata
- Check for required fields: `purpose`, `author`, `category`, `data_sources`, `dependencies`
- Validate category matches directory location
- Return clear error messages with examples

**Alternatives Considered**:
- **JSON Schema validation**: Rejected - too rigid, doesn't handle first-cell metadata pattern
- **Manual review**: Rejected - doesn't scale, error-prone
- **Post-commit validation**: Rejected - better to catch errors before commit

**Implementation Notes**:
- Hook runs after nbstripout but before secret scanning
- Non-blocking for exploratory notebooks (warning only)
- Blocking for tutorials, evaluations, compliance, reporting (error)
- Provide `--skip-metadata-validation` flag for emergency commits

---

### 6. CLI Command Implementation (`just create-notebook`)

**Decision**: Implement as Python script invoked via `just` task runner

**Rationale**:
- `just` is standardized task runner (Principle IX)
- Python script provides rich interactive prompts (using `questionary` or `rich`)
- Easy to test and maintain
- Can leverage template management utilities in `notebook_tools` package

**Implementation Approach**:
1. Add `create-notebook` command to `justfile`
2. Command invokes `uv run python -m notebook_tools.cli create`
3. CLI prompts for:
   - Category selection (with descriptions)
   - Notebook name
   - Purpose (pre-populates metadata)
   - Author (defaults to git config user.name)
4. CLI copies appropriate template, fills metadata, saves to correct directory
5. Opens notebook in default editor (optional)

**Alternatives Considered**:
- **Shell script**: Rejected - harder to test, less portable (Windows)
- **Separate CLI tool**: Rejected - adds installation complexity
- **IDE extension**: Rejected - not all developers use same IDE

**Implementation Notes**:
- Use `questionary` for interactive prompts (better UX than `input()`)
- Validate notebook name (no spaces, valid filename)
- Create directory if doesn't exist
- Print success message with path and next steps

**References**:
- [questionary GitHub](https://github.com/tmbo/questionary)
- [rich GitHub](https://github.com/Textualize/rich)

---

### 7. Git Tagging Conventions for Compliance

**Decision**: Use hierarchical tag naming: `{category}/{identifier}-{date}`

**Rationale**:
- Clear namespace separation by category
- Sortable by date
- Easy to discover via `git tag --list "compliance/*"`
- Aligns with semantic versioning patterns

**Tag Format Examples**:
- `compliance/model-v1.0-audit-2024-10-14`
- `evaluation/baseline-gpt4-2024-10-14`
- `compliance/risk-assessment-prod-2024-11-01`

**Implementation Notes**:
- Document tagging conventions in `docs/notebooks/compliance-officer-guide.md`
- Provide example commands for compliance officers
- Consider future tooling to assist with tag creation (not in initial scope)
- Tags are lightweight git refs, no storage overhead

**Alternatives Considered**:
- **Flat naming**: Rejected - harder to discover related tags
- **Branches instead of tags**: Rejected - tags are immutable, better for audit trail
- **External tracking system**: Rejected - git-native approach simpler, no additional infrastructure

---

### 8. Notebook Size Limits

**Decision**: Implement custom pre-commit hook for size checking

**Rationale**:
- GitHub warns at 50 MB, blocks at 100 MB
- 10 MB limit (warn at 5 MB) prevents most issues before they occur
- Encourages best practice of externalizing data
- Simple to implement (check file size before commit)

**Implementation Approach**:
- Add size check to custom pre-commit hook
- Warn at 5 MB: print message suggesting data externalization
- Block at 10 MB: fail commit with clear error message
- Provide guidance on alternatives (data/ directory, remote storage)

**Alternatives Considered**:
- **Git LFS**: Rejected - adds complexity, not needed for notebooks (should be code-only)
- **No limit**: Rejected - leads to repository bloat
- **Stricter limit (1 MB)**: Rejected - too restrictive for legitimate use cases (embedded plots)

---

### 9. Template Design

**Decision**: Create minimal templates with required metadata and guidance comments

**Rationale**:
- Templates should guide, not constrain
- Metadata fields enforced by pre-commit hooks
- Category-specific guidance in comments
- Easy to customize for specific use cases

**Template Structure**:
```python
# First cell (markdown):
"""
# [Notebook Title]

**Category**: {category}
**Purpose**: [What question does this answer?]
**Author**: {author}
**Created**: {date}
**Data Sources**: [List data sources and versions]
**Dependencies**: [List key dependencies]

## Context
[Provide context for this notebook]

## Expected Outcomes
[What should this notebook produce?]
"""

# Second cell (code):
# Standard imports and setup
import pandas as pd
import numpy as np
# ... category-specific imports

# Third cell onwards: category-specific guidance
```

**Category-Specific Guidance**:
- **Exploratory**: Emphasize rapid iteration, no SpecKit requirement
- **Tutorial**: Link to relevant spec.md, focus on clarity
- **Evaluation**: Require metrics documentation, reproducibility
- **Compliance**: EU AI Act checklist, risk assessment template
- **Reporting**: Parameterization examples, papermill usage

---

### 10. Integration with Experiment Tracking (Future)

**Research Notes**: While not implemented in initial scope, research indicates:

**Leading Options**:
- **MLflow**: Open source, comprehensive, Python-native
- **Weights & Biases**: Commercial with free tier, excellent UX
- **Neptune.ai**: Commercial, compliance-focused
- **Sovereign option**: Potential future ALLiaNCE offering

**Integration Points**:
- Notebook metadata could reference experiment IDs
- Evaluation notebooks could log to tracking system
- Git tags could be synced with experiment milestones
- Compliance notebooks could export to tracking system for audit

**Recommendation**: Document integration points in FR-040 to FR-042, but defer implementation until ALLiaNCE data stack provides standardized solution.

---

## Summary of Decisions

| Area | Decision | Key Rationale |
|------|----------|---------------|
| Output stripping | nbstripout | Industry standard, pre-commit integration |
| Secret scanning | detect-secrets | Python-native, customizable, pre-commit integration |
| Linting | ruff + nbqa | Consistent with ai-kit standards, fast |
| Parameterization | papermill | Industry standard for notebook execution |
| Metadata validation | Custom hook | No existing tool, simple to implement |
| CLI command | Python + just | Testable, rich UX, aligns with tooling standards |
| Git tagging | Hierarchical naming | Discoverable, sortable, audit-friendly |
| Size limits | 5 MB warn, 10 MB block | Prevents repo bloat, encourages best practices |
| Templates | Minimal + guidance | Guide without constraining, metadata-enforced |
| Experiment tracking | Future integration | Defer to ALLiaNCE data stack standardization |

## Next Steps

Phase 1 (Design & Contracts) will:
1. Define data model for notebook metadata, templates, validation results
2. Design CLI command interface and user flows
3. Create quickstart guide for developers and compliance officers
4. No API contracts needed (infrastructure tooling, not services)
