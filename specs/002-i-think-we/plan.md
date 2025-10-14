# Implementation Plan: Jupyter Notebook Support

**Branch**: `002-i-think-we` | **Date**: 2025-10-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-i-think-we/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement Jupyter notebook governance infrastructure for ai-kit to balance exploratory data science workflows with security, reproducibility, and EU AI Act compliance requirements. The feature provides six notebook categories (exploratory, tutorials, evaluations, compliance, reporting, templates), pre-commit hooks for security and metadata validation, a `just create-notebook` CLI command for guided notebook creation, and git-native lifecycle management with compliance officer oversight for audit tagging.

## Technical Context

**Language/Version**: Python 3.11+ (aligns with ai-kit monorepo standard)  
**Primary Dependencies**: 
- **nbstripout**: Pre-commit hook for stripping notebook outputs
- **detect-secrets** or **gitleaks**: Secret scanning for credential detection
- **ruff**: Linting notebook code cells (via nbqa)
- **papermill**: Parameterized notebook execution (for reporting category)
- **nbconvert**: Convert notebooks to scripts/documentation
- **uv**: Dependency management within monorepo workspace
- **just**: Task runner for `create-notebook` command

**Storage**: File system (notebooks stored in `notebooks/` directory structure), git for version control  
**Testing**: pytest for CLI command tests, pre-commit framework for hook validation  
**Target Platform**: Developer workstations (macOS, Linux, Windows via WSL)  
**Project Type**: Monorepo infrastructure (tooling + templates + pre-commit hooks)  
**Performance Goals**: 
- Notebook creation via `just create-notebook` < 30 seconds (SC-012)
- Pre-commit hook execution < 5 seconds for typical notebook
- Secret scanning complete within pre-commit timeout

**Constraints**: 
- Notebook file size: warn at 5 MB, block at 10 MB (FR-006a)
- Pre-commit hooks must not block legitimate workflows
- Must integrate with existing ai-kit monorepo structure (uv, just, ruff)
- Git tagging workflow must not burden developers (compliance officers handle)

**Scale/Scope**: 
- 6 notebook categories + templates
- ~10-15 notebook templates (2-3 per active category)
- Pre-commit hook configuration for nbstripout + secret scanning + metadata validation
- 1 CLI command (`just create-notebook`) with interactive prompts
- Documentation for compliance officers on git tagging workflow

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with ai-kit constitution principles:

- [x] **EU AI Act Compliance (Principle I)**: ✅ **COMPLIANT** - This feature enables EU AI Act compliance for notebooks used in high-risk AI systems. FR-030 to FR-035 require compliance and evaluation notebooks to document training data, evaluation metrics, risk assessments, and audit trails. Compliance officers (intrapreneurs/ALLiaNCE experts) review and tag notebooks for regulatory milestones.

- [x] **RGAA Accessibility Compliance (Principle II)**: ✅ **N/A** - No UI components. This is infrastructure tooling (CLI commands, pre-commit hooks, templates). The `just create-notebook` command is CLI-based and accessible via terminal.

- [x] **Security Homologation (Principle III)**: ✅ **COMPLIANT** - Feature directly supports homologation requirements. FR-001 to FR-006a enforce security (credential blocking, output stripping, size limits). Compliance notebooks (FR-034) support technical documentation for homologation dossiers. Audit trails via git tags enable security review.

- [x] **Open Source & Digital Commons (Principle IV)**: ✅ **COMPLIANT** - All tooling uses open source dependencies (nbstripout, detect-secrets/gitleaks, ruff, papermill). No proprietary tools required. Code will be published under ai-kit's open source license.

- [x] **DSFR Design System Compliance (Principle V)**: ✅ **N/A** - No UI components. CLI-only tooling.

- [x] **ProConnect Authentication (Principle VI)**: ✅ **N/A** - No user-facing authentication. Infrastructure tooling for developers.

- [x] **User-Centered Iteration (Principle VII)**: ✅ **COMPLIANT** - Feature supports user research through tutorial notebooks (FR-021) and enables data-driven decisions via evaluation notebooks (FR-022, FR-031). Analytics can be captured in reporting notebooks (FR-024, FR-014).

- [x] **Extensibility and Innovation (Principle VIII)**: ✅ **COMPLIANT** - Template-based approach (FR-009) allows easy addition of new notebook categories. Pre-commit hook framework is extensible. Future experiment tracking integration anticipated (FR-040 to FR-042).

- [x] **Developer Experience & Tooling (Principle IX)**: ✅ **COMPLIANT** - Uses standardized tooling: `just` for create-notebook command, `uv` for dependency management, `ruff` for linting (via nbqa). Integrates with existing monorepo structure. No TypeScript usage.

- [x] **Python-First Development (Principle X)**: ✅ **COMPLIANT** - All tooling is Python-based. Notebooks are Jupyter (Python-native). CLI command implemented in Python. No non-Python components.

- [x] **Specification-Driven Development (Principle XI)**: ✅ **COMPLIANT** - This feature follows SpecKit workflow: `/speckit.specify` → `/speckit.clarify` → `/speckit.plan` (current phase). All artifacts in `specs/002-i-think-we/`. Traceability maintained from spec to implementation.

- [x] **French Government AI Stack Integration (Principle XII)**: ✅ **FUTURE** - Experiment tracking integration (FR-040 to FR-042) anticipates future ALLiaNCE data stack integration. No current government AI services required for notebook infrastructure.

- [x] **Jupyter Notebook Discipline (Principle XIII)**: ✅ **IMPLEMENTS** - **This feature IS the implementation of Principle XIII**. Provides the infrastructure, governance, and tooling required by the constitution for notebook discipline.

- [x] **Streamlit-to-Production Bridge (Principle XIV)**: ✅ **N/A** - No Streamlit usage. Notebooks are separate from Streamlit prototyping workflow.

**Violations Requiring Justification**: None

## Project Structure

### Documentation (this feature)

```
specs/002-i-think-we/
├── spec.md                      # Feature specification (completed)
├── plan.md                      # This file (in progress)
├── research.md                  # Phase 0 output (to be generated)
├── data-model.md                # Phase 1 output (to be generated)
├── quickstart.md                # Phase 1 output (to be generated)
├── contracts/                   # Phase 1 output (to be generated)
├── tasks.md                     # Phase 2 output (/speckit.tasks - not created by /speckit.plan)
├── checklists/
│   └── requirements.md          # Specification quality checklist (completed)
└── OPTION2_IMPLEMENTATION.md    # Option 2 (Hybrid) decision documentation
```

### Source Code (repository root)

```
# Monorepo infrastructure additions for notebook support

notebooks/                       # Top-level notebook directory (NEW)
├── exploratory/                 # Rapid experimentation (low governance)
├── tutorials/                   # Learning materials (documentation standards)
├── evaluations/                 # Model performance assessment (medium governance)
├── compliance/                  # EU AI Act & regulatory docs (high governance)
├── reporting/                   # Parameterized stakeholder reports (medium governance)
├── templates/                   # Starter notebooks (reference materials)
│   ├── exploratory-template.ipynb
│   ├── tutorial-template.ipynb
│   ├── evaluation-template.ipynb
│   ├── compliance-template.ipynb
│   └── reporting-template.ipynb
└── .gitkeep files in each category

.pre-commit-config.yaml          # Pre-commit hook configuration (MODIFIED)
├── Add nbstripout hook
├── Add detect-secrets or gitleaks hook
├── Add custom metadata validation hook

justfile                         # Task runner commands (MODIFIED)
└── Add create-notebook command

packages/notebook-tools/         # Notebook tooling package (NEW)
├── pyproject.toml               # uv package configuration
├── src/
│   └── notebook_tools/
│       ├── __init__.py
│       ├── cli.py               # `just create-notebook` implementation
│       ├── validators.py        # Metadata validation for pre-commit hooks
│       └── templates.py         # Template management utilities
└── tests/
    ├── test_cli.py
    ├── test_validators.py
    └── test_templates.py

docs/                            # Documentation (MODIFIED)
└── notebooks/
    ├── governance.md            # Notebook governance guide
    ├── compliance-officer-guide.md  # Git tagging workflow for compliance officers
    └── migration-guide.md       # Notebook-to-production migration patterns

.gitignore                       # Git ignore patterns (MODIFIED)
└── Add notebook execution artifacts patterns
```

**Structure Decision**: This is a **monorepo infrastructure feature** that adds notebook governance tooling to the existing ai-kit repository. The implementation follows Option 1 (Single project) pattern with a dedicated `packages/notebook-tools/` package for CLI and validation logic. The feature integrates with existing monorepo tooling (`just`, `uv`, `.pre-commit-config.yaml`) rather than creating separate applications.

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

**Status**: ✅ No violations - complexity tracking not required

---

## Phase 0: Research (COMPLETED)

**Status**: ✅ Complete  
**Output**: `research.md`

**Key Decisions**:
1. **nbstripout** for output stripping (industry standard, pre-commit integration)
2. **detect-secrets** for credential scanning (Python-native, customizable)
3. **ruff + nbqa** for notebook linting (consistent with ai-kit standards)
4. **papermill** for parameterized execution (industry standard from Netflix)
5. **Custom pre-commit hook** for metadata validation (no existing tool)
6. **Python CLI + just** for create-notebook command (testable, rich UX)
7. **Hierarchical git tags** for compliance (`{category}/{identifier}-{date}`)
8. **5 MB warning, 10 MB block** for notebook size limits
9. **Minimal templates** with required metadata and guidance
10. **Future experiment tracking** integration (defer to ALLiaNCE data stack)

All technical unknowns resolved. Ready for implementation.

---

## Phase 1: Design & Contracts (COMPLETED)

**Status**: ✅ Complete  
**Outputs**: 
- `data-model.md` - Entity definitions and relationships
- `contracts/cli-interface.md` - CLI command specifications
- `quickstart.md` - User-facing getting started guide
- `.windsurf/rules/specify-rules.md` - Updated agent context

**Key Artifacts**:

1. **Data Model** (`data-model.md`):
   - Notebook Metadata structure (required/optional fields)
   - Category definitions with governance levels
   - Pre-commit hook configuration
   - Notebook template structure
   - Git tag reference format
   - Validation result schema
   - CLI configuration
   - State transitions and lifecycle

2. **CLI Interface** (`contracts/cli-interface.md`):
   - `just create-notebook` interactive flow
   - Pre-commit hook contracts (metadata validation, size check)
   - Integration with nbstripout and detect-secrets
   - Error codes and messages
   - Git workflow integration
   - Compliance officer tagging workflow

3. **Quickstart Guide** (`quickstart.md`):
   - 5-minute quick start
   - Category decision tree
   - Common workflows (exploratory → production, evaluation, tutorial)
   - Security best practices
   - Troubleshooting guide
   - Compliance officer instructions

4. **Agent Context** (`.windsurf/rules/specify-rules.md`):
   - Updated with Python 3.11+, file system storage, monorepo infrastructure
   - Enables AI agent to understand project context

**Constitution Re-Check**: ✅ Still compliant (no design changes affecting principles)

---

## Phase 2: Task Generation (NEXT STEP)

**Status**: ⏳ Pending  
**Command**: `/speckit.tasks`  
**Output**: `tasks.md`

This phase will generate dependency-ordered implementation tasks based on the design artifacts created in Phase 0 and Phase 1.

---

## Implementation Readiness

✅ **Specification complete** (`spec.md` with clarifications)  
✅ **Research complete** (all technical decisions made)  
✅ **Design complete** (data model, contracts, quickstart)  
✅ **Constitution compliant** (no violations)  
✅ **Agent context updated** (Windsurf rules file)

**Ready for**: `/speckit.tasks` to generate actionable implementation tasks
