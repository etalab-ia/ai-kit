# Compliance Officer Guide: Notebook Tagging Workflow

**Last Updated**: 2025-10-15

## Overview

This guide is for compliance officers (intrapreneurs and ALLiaNCE experts) responsible for reviewing and tagging notebooks for regulatory compliance.

## Responsibilities

As a compliance officer, you:

1. **Review** compliance and evaluation notebooks for completeness
2. **Validate** regulatory requirements are met
3. **Create git tags** for audit milestones
4. **Maintain** audit trail for homologation dossiers

## Review Process

### 1. Identify Notebooks for Review

Notebooks requiring compliance review:
- `notebooks/compliance/` - EU AI Act, GDPR documentation
- `notebooks/evaluations/` - Model performance assessments used for production decisions

### 2. Review Checklist

For each notebook, verify:

#### Completeness
- [ ] All required metadata present
- [ ] Purpose clearly stated
- [ ] Author identified
- [ ] Data sources documented with versions
- [ ] Dependencies listed with versions

#### Methodology
- [ ] Evaluation methodology clearly documented
- [ ] Metrics appropriate for use case
- [ ] Baseline comparisons included (for evaluations)
- [ ] Results reproducible

#### Regulatory Compliance
- [ ] EU AI Act requirements addressed (for high-risk systems)
- [ ] Risk assessment completed (for compliance notebooks)
- [ ] Training data characteristics documented
- [ ] Model selection rationale provided
- [ ] Limitations identified

#### Documentation Quality
- [ ] Technical documentation complete
- [ ] Findings clearly stated
- [ ] Recommendations actionable
- [ ] Audit trail established

### 3. Request Changes (if needed)

If notebook is incomplete:

1. **Document issues** in notebook review comments
2. **Request updates** from author
3. **Re-review** after updates

## Git Tagging Workflow

### Tag Naming Convention

Format: `{category}/{identifier}-{date}`

**Examples**:
- `compliance/model-v1.0-audit-2024-10-14`
- `evaluations/gpt4-baseline-2024-10-14`
- `compliance/risk-assessment-prod-2024-11-01`

**Components**:
- **category**: `compliance` or `evaluations`
- **identifier**: Descriptive name (system, model, purpose)
- **date**: ISO 8601 format (YYYY-MM-DD)

### Creating Tags

After successful review, create a git tag to mark the audit milestone.

**Option A: Using CLI** (recommended):

```bash
# Interactive tagging with prompts
just notebook tag notebooks/compliance/model-v1-audit.ipynb

# Or provide details directly
just notebook tag notebooks/compliance/model-v1-audit.ipynb \
  --identifier model-v1.0-audit \
  --message "Compliance audit approved for model v1.0 deployment. Reviewed by Jane Doe." \
  --push
```

**What this does**:
- Validates notebook category (prevents tagging exploratory notebooks)
- Generates tag name with date: `compliance/model-v1.0-audit-2024-10-14`
- Creates annotated git tag with your message
- Optionally pushes to remote with `--push` flag
- Provides discovery commands

**Option B: Manual git commands**:

```bash
# Create annotated tag
git tag -a compliance/model-v1.0-audit-2024-10-14 \
  -m "Compliance audit approved for model v1.0 deployment
  
Reviewed by: [Your Name]
Review date: 2024-10-14
Notebook: notebooks/compliance/model-v1-audit.ipynb
Status: Approved for production deployment
Regulatory framework: EU AI Act (High-Risk AI System)
"

# Push tag to remote
git push origin compliance/model-v1.0-audit-2024-10-14
```

### Tag Message Template

```
[Brief description of what was reviewed]

Reviewed by: [Officer Name]
Review date: [YYYY-MM-DD]
Notebook: [path to notebook]
Status: [Approved/Conditional/Rejected]
Regulatory framework: [EU AI Act/GDPR/etc.]
Notes: [Any additional context]
```

## Discovering Tagged Notebooks

### List All Notebook Tags

**Option A: Using CLI** (recommended):

```bash
# List all notebook tags
just notebook tags

# List tags for specific category
just notebook tags --category compliance
just notebook tags --category evaluations
```

Output:
```
Notebook Tags:

  compliance:
    - compliance/model-v1.0-audit-2024-10-14
    - compliance/risk-assessment-prod-2024-11-01
  
  evaluations:
    - evaluations/gpt4-baseline-2024-10-14

Total: 3 tags
```

**Option B: Manual git commands**:

```bash
# List all compliance tags
git tag --list "compliance/*"

# List all evaluation tags
git tag --list "evaluations/*"
```

### View Tag Details

```bash
git show compliance/model-v1.0-audit-2024-10-14
```

Shows:
- Tag message
- Commit SHA
- Notebook state at time of tag
- Full commit details

### Checkout Tagged Version

```bash
# View notebook at tagged state
git checkout compliance/model-v1.0-audit-2024-10-14
jupyter lab notebooks/compliance/model-v1-audit.ipynb

# Return to latest
git checkout main
```

## Audit Trail Documentation

### For Homologation Dossiers

Include in compliance documentation:

1. **Tag reference**:
   ```
   Compliance review: compliance/model-v1.0-audit-2024-10-14
   Commit SHA: abc123def456...
   ```

2. **Review summary**:
   - Reviewer name and date
   - Regulatory framework
   - Key findings
   - Approval status

3. **Notebook location**:
   - Path in repository
   - How to access tagged version

### Example Documentation

```markdown
## Model Evaluation Evidence

**Evaluation Notebook**: `notebooks/evaluations/gpt4-baseline.ipynb`
**Git Tag**: `evaluations/gpt4-baseline-2024-10-14`
**Commit SHA**: `abc123def456...`
**Reviewed by**: Marie Dubois (ALLiaNCE Expert)
**Review Date**: 2024-10-14

### Findings
- Accuracy: 94% (exceeds 90% threshold)
- F1 Score: 0.92
- Bias metrics: Within acceptable range
- Recommendation: Approved for production deployment

### Access
```bash
git show evaluations/gpt4-baseline-2024-10-14
```
```

## Common Scenarios

### Scenario 1: Model Deployment Approval

**Situation**: Development team requests approval to deploy model to production.

**Workflow**:
1. Review evaluation notebook in `notebooks/evaluations/`
2. Verify performance metrics meet requirements
3. Check bias and fairness assessments
4. Create tag: `evaluations/[model]-[version]-[date]`
5. Document approval in deployment request

### Scenario 2: EU AI Act Compliance Documentation

**Situation**: High-risk AI system requires compliance documentation.

**Workflow**:
1. Review compliance notebook in `notebooks/compliance/`
2. Verify all EU AI Act checklist items completed
3. Validate risk assessment and mitigation measures
4. Create tag: `compliance/[system]-audit-[date]`
5. Include tag reference in homologation dossier

### Scenario 3: Periodic Compliance Review

**Situation**: Quarterly review of production AI systems.

**Workflow**:
1. List all compliance tags from previous quarter
2. Review any updated notebooks
3. Create new tags for updated reviews
4. Document changes in compliance report

## Tag Management

### Updating Reviews

If notebook is updated after initial review:

1. **New tag** for new review:
   ```bash
   git tag -a compliance/model-v1.1-audit-2024-11-01 -m "Updated review"
   ```

2. **Keep old tag** for audit trail

3. **Document relationship** in tag message:
   ```
   Updated review of model v1.1
   Previous review: compliance/model-v1.0-audit-2024-10-14
   Changes: [describe what changed]
   ```

### Deleting Tags (Rare)

Only delete tags if created in error:

```bash
# Delete local tag
git tag -d compliance/wrong-tag

# Delete remote tag
git push origin :refs/tags/compliance/wrong-tag
```

**Important**: Deleting tags breaks audit trail. Only do this immediately after creation if tag was created incorrectly.

## Best Practices

1. **Timely reviews**: Review notebooks within 5 business days of request
2. **Clear communication**: Provide specific feedback if changes needed
3. **Consistent tagging**: Follow naming convention strictly
4. **Detailed messages**: Include all relevant context in tag message
5. **Documentation**: Reference tags in all compliance documentation
6. **Preservation**: Never delete tags except in error cases

## Tools and Commands

### Quick Reference

```bash
# List notebooks needing review
find notebooks/compliance notebooks/evaluations -name "*.ipynb"

# Create tag
git tag -a [tag-name] -m "[message]"

# Push tag
git push origin [tag-name]

# List tags
git tag --list "[category]/*"

# View tag
git show [tag-name]

# Checkout tagged version
git checkout [tag-name]
```

## Questions?

- **Tagging questions**: Contact DevOps team
- **Regulatory questions**: Consult legal/compliance team
- **Technical issues**: Open issue in ai-kit repository
- **Process improvements**: Suggest in team retrospective
