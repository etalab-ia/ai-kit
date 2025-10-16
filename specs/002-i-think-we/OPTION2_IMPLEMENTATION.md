# Option 2 (Hybrid) Implementation Summary

**Date**: 2025-10-14  
**Decision**: Implement git-native notebook lifecycle with selective retention for compliance

## What Changed

### Removed
- ❌ `notebooks/archive/` directory (7th category eliminated)
- ❌ General archiving requirement for all notebooks
- ❌ Manual archive management overhead

### Added
- ✅ Git-native lifecycle: Delete exploratory notebooks after migration
- ✅ Git tagging for compliance/evaluation milestones (e.g., `compliance/model-v1.0-audit`)
- ✅ Experiment tracking integration requirements (FR-040, FR-041, FR-042)
- ✅ Clear retention policy: exploratory = delete, compliance/evaluation = retain + tag
- ✅ Git commit SHA references in migration documentation

## Key Changes by Section

### User Story 2 - Organized Notebook Categories
- **Before**: 7 categories including `archive/`
- **After**: 6 categories (removed `archive/`)
- **New scenarios**:
  - Scenario 7: Exploratory notebooks deleted, git history preserves
  - Scenario 8: Compliance/evaluation notebooks tagged for audit discovery

### User Story 4 - Notebook-to-Production Migration
- **Before**: Move notebooks to `archive/` directory
- **After**: 
  - Exploratory: Delete after documenting git commit SHA
  - Compliance/Evaluation: Retain in original category + git tag

### Functional Requirements

#### Directory Structure (FR-007)
- **Before**: 7 directories
- **After**: 6 directories (removed `archive/`)

#### Migration & Lifecycle (FR-025 to FR-029)
- **FR-025**: Git-native lifecycle guidance (delete vs. retain)
- **FR-026**: Migration docs must include git commit references
- **FR-027**: Git tags for audit milestones
- **FR-028**: Retain compliance/evaluation in original directories
- **FR-029**: NEW - Delete exploratory after migration

#### EU AI Act Compliance (FR-035)
- **NEW**: Git tagging requirement for regulatory milestones

#### Experiment Tracking (FR-040 to FR-042)
- **NEW**: Integration with experiment tracking systems
- **NEW**: Guidance on logging experiments
- **NEW**: Reference tracking IDs in evaluation notebooks

### Key Entities

#### Notebook Category
- **Before**: 7 categories with `archive/` as "historical record"
- **After**: 6 categories with lifecycle annotations:
  - Exploratory: "deleted after migration"
  - Tutorials: "retained"
  - Evaluations: "retained and tagged"
  - Compliance: "retained and tagged"
  - Reporting: "retained"
  - Templates: "retained"

#### Migration Record
- **Before**: Links to archived notebooks
- **After**: Uses git commit SHAs for deleted notebooks, paths for retained

#### Git Tag Reference (NEW)
- Represents milestone tags for compliance/evaluation notebooks
- Enables audit discovery without archive directory

### Success Criteria (SC-008)
- **Before**: "linking archived notebooks to production code"
- **After**: "using git references (commit SHAs for deleted, tags for retained)"

## Rationale

### Problems Solved
1. **Eliminates clutter**: No accumulation of old exploratory notebooks
2. **Git-native workflow**: Leverages existing version control capabilities
3. **Maintains compliance**: Retains regulatory documentation where needed
4. **Simplifies mental model**: Clear delete vs. retain decision tree

### Compliance Maintained
- ✅ EU AI Act audit trail (via git tags on compliance/evaluation notebooks)
- ✅ Security homologation documentation (retained in original directories)
- ✅ GDPR data governance (documented in retained compliance notebooks)

### Developer Experience Improved
- ✅ Fewer directories to navigate
- ✅ Standard git workflow (delete files, use history)
- ✅ Clear retention policy (exploratory = delete, compliance = keep)
- ✅ Git tags make audit milestones discoverable

## Migration from Previous Approach

If any notebooks were already in an `archive/` directory:

1. **Exploratory notebooks**: Can be deleted (git history preserves them)
2. **Compliance/evaluation notebooks**: Move back to original category and tag appropriately
3. **Update documentation**: Replace archive references with git commit SHAs or tags

## Future Work: Experiment Tracking

Added to "Future Considerations" section:
- Acknowledge need for standardized experiment tracking in ALLiaNCE stack
- Propose future constitution amendment for experiment tracking principle
- Suggest evaluation of MLflow, Weights & Biases, or sovereign solutions
- Complement git-native approach with structured metadata capture

## Implementation Checklist

When implementing this feature:

- [ ] Create 6 directories (not 7): `exploratory/`, `tutorials/`, `evaluations/`, `compliance/`, `reporting/`, `templates/`
- [ ] Document git tagging conventions for compliance/evaluation milestones
- [ ] Provide guidance on discovering deleted notebooks via git history
- [ ] Create migration documentation template with git commit SHA fields
- [ ] Add experiment tracking integration guidance (even without chosen solution)
- [ ] Update decision tree to clarify delete vs. retain policy

## References

- Original discussion: User questioned archive directory rationale given git history
- Research: Industry best practices favor git-native approach for exploratory work
- Decision: Option 2 (Hybrid) balances compliance needs with developer experience
- Next step: Consider experiment tracking principle for constitution amendment
