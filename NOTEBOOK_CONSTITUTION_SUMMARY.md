# Jupyter Notebook Constitution Amendment Summary

**Date**: 2025-10-13  
**Version Change**: 1.7.1 → 1.8.0 (MINOR)  
**Amendment**: Added Principle XIII: Jupyter Notebook Discipline (swapped with Streamlit-to-Production Bridge, now XIV)

## What Was Added

### New Principle XIII: Jupyter Notebook Discipline

A comprehensive governance framework for Jupyter notebooks in the top-level `notebooks/` directory that balances:
- **Exploratory freedom** for data science experimentation
- **Security requirements** to prevent credential leakage
- **Compliance obligations** for EU AI Act and security homologation
- **Quality standards** for reproducibility and documentation

## Key Components

### 1. Notebook Categorization

Three distinct categories with different governance levels:

- **`notebooks/exploratory/`**: Rapid experimentation, not subject to SpecKit workflow
- **`notebooks/documentation/`**: Tutorials and examples, subject to documentation standards
- **`notebooks/production-adjacent/`**: Model evaluation and compliance reporting, subject to EU AI Act requirements

### 2. Security Requirements (NON-NEGOTIABLE)

- No hardcoded credentials or sensitive data
- `nbstripout` pre-commit hook to remove outputs
- `.gitignore` patterns for notebook execution artifacts
- Security review before public publication
- GDPR compliance for data sources

### 3. Quality Standards

- Reproducibility: dependency specifications required
- Documentation: purpose, author, data sources, runtime requirements
- Version control: outputs stripped before commit
- Code quality: ruff linting where practical
- Cell organization: structured narrative with markdown

### 4. Integration with SpecKit Workflow

- **Exploratory**: Not required to follow SpecKit, but insights must be captured when productionized
- **Documentation**: Referenced in spec.md and quickstart guides
- **Production-adjacent**: Documented in plan.md research section

### 5. EU AI Act Compliance

Production-adjacent notebooks for high-risk AI systems must document:
- Model training data characteristics
- Evaluation metrics and validation results
- Risk assessment findings
- Model selection audit trail
- Technical documentation for homologation dossier

### 6. Tooling Standards

- **nbstripout**: Remove outputs before commit
- **nbconvert**: Convert to scripts/docs
- **papermill**: Parameterize and execute programmatically
- **ruff**: Lint notebook code (via nbqa)
- **uv**: Manage dependencies in monorepo

### 7. Migration to Production

Clear 5-step process:
1. Extract code to `packages/` or `apps/`
2. Document migration in feature spec
3. Archive exploratory notebooks
4. Retain production-adjacent for compliance
5. Follow Principle XI for production implementation

## Why This Matters

### Problems Solved

1. **Security Risk**: Prevents accidental credential commits in notebooks
2. **Compliance Liability**: Ensures notebooks support EU AI Act documentation requirements
3. **Technical Debt**: Provides clear migration path from exploration to production
4. **Irreproducibility**: Mandates dependency management and documentation
5. **Audit Trail**: Establishes governance for model decisions and evaluations

### Alignment with Existing Principles

- **Principle I (EU AI Act)**: Production-adjacent notebooks support compliance documentation
- **Principle III (Security Homologation)**: Security requirements prevent credential leakage
- **Principle IV (Open Source)**: Guidance on what can be published publicly
- **Principle X (Python-First)**: Notebooks align with Python-first culture
- **Principle XI (SpecKit)**: Integration with specification-driven workflow

## Template Updates

### ✅ Completed

- **constitution.md**: Added Principle XIII (Jupyter Notebook Discipline) with full governance framework, swapped with Streamlit-to-Production Bridge (now XIV)
- **plan-template.md**: Updated Constitution Check section with correct principle ordering (XIII: Notebooks, XIV: Streamlit)

### No Changes Required

- **spec-template.md**: No principle-specific references
- **tasks-template.md**: No principle-specific references

## Next Steps (Follow-up TODOs)

When you create the notebooks support feature, you should:

1. **Create feature spec**: `specs/002-jupyter-notebook-support/`
2. **Pre-commit hooks**: Add nbstripout configuration
3. **Gitignore patterns**: Add `notebooks/**/*.ipynb` output patterns
4. **Notebook templates**: Create templates for each category
5. **Ruff configuration**: Add notebook linting via nbqa
6. **Migration guide**: Document notebook-to-production patterns
7. **Directory structure**: Create `notebooks/{exploratory,documentation,production-adjacent,archive}/`

## Rationale for MINOR Version Bump

This is a **MINOR** (1.8.0) rather than PATCH because:
- **New principle added**: Expands governance scope to notebooks
- **New mandatory requirements**: Security and quality standards for notebooks
- **New tooling standards**: nbstripout, papermill, nbqa
- **Material guidance expansion**: Comprehensive framework, not just clarification

Not MAJOR because:
- **No breaking changes**: Existing projects without notebooks are unaffected
- **Backward compatible**: Adds requirements only for new notebook usage
- **No principle removals**: All existing principles remain intact

## Suggested Commit Message

```
docs: amend constitution to v1.8.0 (add Principle XIV: Jupyter Notebook Discipline)

- Add comprehensive governance framework for notebooks/ directory
- Establish security requirements (nbstripout, no credentials)
- Define notebook categories (exploratory, documentation, production-adjacent)
- Integrate with SpecKit workflow and EU AI Act compliance
- Update plan-template.md Constitution Check with Principle XIV
- Provide clear migration path from notebooks to production code

Rationale: Jupyter notebooks are essential for AI/ML experimentation but
require governance to prevent security risks, compliance liabilities, and
technical debt accumulation.
```

## Questions for Clarification

Before creating the feature spec, consider:

1. **Notebook execution environment**: Should notebooks run in the shared `.venv` or isolated environments?
2. **CI/CD integration**: Should notebooks be executed in CI for validation?
3. **Notebook templates**: What starter templates would be most valuable (data exploration, model evaluation, compliance reporting)?
4. **Integration with existing tools**: How should notebooks interact with `apps/` and `packages/`?
5. **Compliance tooling**: Do you need automated compliance checks for production-adjacent notebooks?

---

**Constitution Version**: 1.8.0  
**Amendment Status**: ✅ Complete  
**Ready for Feature Spec**: Yes
