# Implementation Plan: Jupyter Notebook Support

**Branch**: `002-i-think-we` | **Date**: 2025-10-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-i-think-we/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement Jupyter notebook governance infrastructure for ai-kit to balance exploratory data science workflows with security, reproducibility, and EU AI Act compliance requirements. The feature provides six notebook categories (exploratory, tutorials, evaluations, compliance, reporting, templates), hybrid secret scanning (Gitleaks + GitHub) for defense-in-depth security, pre-commit hooks for metadata validation, a `just notebook` CLI command group for guided notebook creation, and git-native lifecycle management with compliance officer oversight for audit tagging.

## Technical Context

**Language/Version**: Python 3.11+ (aligns with ai-kit monorepo standard)  
**Primary Dependencies**: 
- **nbstripout**: Pre-commit hook for stripping notebook outputs
- **GitHub Secret Scanning**: Native secret detection (continuous monitoring, free for public repos)
- **gitleaks**: Pre-commit secret blocking (defense in depth, local validation)
- **ruff**: Linting notebook code cells (via nbqa)
- **papermill**: Parameterized notebook execution (for reporting category)
- **nbconvert**: Convert notebooks to scripts/documentation
- **uv**: Dependency management within monorepo workspace
- **just**: Task runner for `notebook` command group

**Storage**: File system (notebooks stored in `notebooks/` directory structure), git for version control  
**Testing**: pytest for CLI command tests, pre-commit framework for hook validation  
**Target Platform**: Developer workstations (macOS, Linux, Windows via WSL)  
**Project Type**: Monorepo infrastructure (tooling + templates + pre-commit hooks)  
**Performance Goals**: 
- Notebook creation via `just notebook create` < 30 seconds (SC-012)
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
- Unified CLI with `notebook` command group (create, list, validate, delete, migrate, stats subcommands)
- Documentation for compliance officers on git tagging workflow

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with ai-kit constitution principles:

- [x] **EU AI Act Compliance (Principle I)**: ✅ **COMPLIANT** - This feature enables EU AI Act compliance for notebooks used in high-risk AI systems. FR-030 to FR-035 require compliance and evaluation notebooks to document training data, evaluation metrics, risk assessments, and audit trails. Compliance officers (intrapreneurs/ALLiaNCE experts) review and tag notebooks for regulatory milestones.

- [x] **RGAA Accessibility Compliance (Principle II)**: ✅ **N/A** - No UI components. This is infrastructure tooling (CLI commands, pre-commit hooks, templates). The `just notebook` commands are CLI-based and accessible via terminal.

- [x] **Security Homologation (Principle III)**: ✅ **COMPLIANT** - Feature directly supports homologation requirements. FR-001 to FR-006a enforce security (credential blocking, output stripping, size limits). Compliance notebooks (FR-034) support technical documentation for homologation dossiers. Audit trails via git tags enable security review.

- [x] **Open Source & Digital Commons (Principle IV)**: ✅ **COMPLIANT** - All tooling uses open source dependencies (nbstripout, gitleaks, ruff, papermill). GitHub Secret Scanning is a free platform feature for public repos. Code will be published under ai-kit's open source license.

- [x] **DSFR Design System Compliance (Principle V)**: ✅ **N/A** - No UI components. CLI-only tooling.

- [x] **ProConnect Authentication (Principle VI)**: ✅ **N/A** - No user-facing authentication. Infrastructure tooling for developers.

- [x] **User-Centered Iteration (Principle VII)**: ✅ **COMPLIANT** - Feature supports user research through tutorial notebooks (FR-021) and enables data-driven decisions via evaluation notebooks (FR-022, FR-031). Analytics can be captured in reporting notebooks (FR-024, FR-014).

- [x] **Extensibility and Innovation (Principle VIII)**: ✅ **COMPLIANT** - Template-based approach (FR-009) allows easy addition of new notebook categories. Pre-commit hook framework is extensible. Future experiment tracking integration anticipated (FR-040 to FR-042).

- [x] **Developer Experience & Tooling (Principle IX)**: ✅ **COMPLIANT** - Uses standardized tooling: `just` for notebook command group, `uv` for dependency management, `ruff` for linting (via nbqa). Integrates with existing monorepo structure. No TypeScript usage.

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
├── research.md                  # Phase 0 output (completed)
├── research-secret-scanning.md  # Secret scanning alternatives research (completed)
├── MIGRATION_SECRET_SCANNING.md # Migration guide from detect-secrets (completed)
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

notebooks/                       # Top-level notebook directory (NEW - see spec.md Key Entities for governance details)
├── exploratory/                 # Rapid experimentation
├── tutorials/                   # Learning materials
├── evaluations/                 # Model performance assessment
├── compliance/                  # EU AI Act & regulatory docs
├── reporting/                   # Parameterized stakeholder reports
├── templates/                   # Starter notebooks
│   ├── exploratory-template.ipynb
│   ├── tutorial-template.ipynb
│   ├── evaluation-template.ipynb
│   ├── compliance-template.ipynb
│   └── reporting-template.ipynb
└── .gitkeep files in each category

.pre-commit-config.yaml          # Pre-commit hook configuration (MODIFIED)
├── Add nbstripout hook
├── Add gitleaks hook (pre-commit blocking, defense in depth)
├── Add custom metadata validation hook
├── Remove detect-secrets hook (replaced by hybrid GitHub + Gitleaks)

.gitleaks.toml                   # Gitleaks configuration (NEW)
└── Allowlist for notebook metadata hex strings

.secrets.baseline                # Legacy detect-secrets baseline (DELETE)

justfile                         # Task runner commands (MODIFIED)
└── Add notebook command group (just notebook <subcommand>)

apps/cli/                        # Unified ai-kit CLI application (NEW)
├── pyproject.toml               # uv package configuration
├── src/
│   └── ai_kit/
│       └── cli/                 # CLI package (per Constitution Principle XV)
│           ├── __init__.py
│           ├── main.py          # CLI entry point
│           ├── commands/
│           │   ├── __init__.py
│           │   └── notebook.py  # Notebook command group
│           ├── core/
│           │   ├── config.py    # Configuration management
│           │   ├── validators.py # Validation logic
│           │   └── templates.py # Template management
│           └── utils/
│               ├── git.py       # Git operations
│               ├── prompts.py   # Interactive prompts
│               └── output.py    # Formatted output
└── tests/
    ├── commands/
    │   └── test_notebook.py     # Tests for notebook command group
    ├── core/
    │   ├── test_config.py       # Tests for configuration
    │   ├── test_validators.py   # Tests for validators
    │   └── test_templates.py    # Tests for templates
    └── utils/
        ├── test_git.py          # Tests for git utilities
        ├── test_prompts.py      # Tests for prompts
        └── test_output.py       # Tests for output formatting

docs/                            # Documentation (MODIFIED)
└── notebooks/
    ├── governance.md            # Notebook governance guide
    ├── compliance-officer-guide.md  # Git tagging workflow for compliance officers
    └── migration-guide.md       # Notebook-to-production migration patterns

.gitignore                       # Git ignore patterns (MODIFIED)
└── Add notebook execution artifacts patterns
```

**Structure Decision**: This is a **monorepo infrastructure feature** that adds notebook governance tooling to the existing ai-kit repository. The implementation follows Option 1 (Single project) pattern with a unified CLI application in `apps/cli/` using the `ai_kit.cli` namespace (per Constitution Principle XV). The feature integrates with existing monorepo tooling (`just`, `uv`, `.pre-commit-config.yaml`) and establishes the foundation for future ai-kit command groups (dataset, streamlit, compliance, experiment).

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

**Status**: ✅ No violations - complexity tracking not required

---

## Phase 0: Research (COMPLETED)

**Status**: ✅ Complete  
**Output**: `research.md`

**Key Decisions**:
1. **nbstripout** for output stripping (industry standard, pre-commit integration)
2. **Hybrid Secret Scanning** (GitHub + Gitleaks) for defense in depth:
   - **GitHub Secret Scanning**: Continuous monitoring, validity checking, 150+ providers
   - **Gitleaks**: Pre-commit blocking, local validation, fast performance
3. **ruff + nbqa** for notebook linting (consistent with ai-kit standards)
4. **papermill** for parameterized execution (industry standard from Netflix)
5. **Custom pre-commit hook** for metadata validation (no existing tool)

**Secret Scanning Decision Rationale** (see `research-secret-scanning.md`):
- **Replaced detect-secrets** due to high false positive rate (465-line baseline file)
- **Hybrid approach (Option 4)** provides multiple layers of protection:
  - **GitHub Secret Scanning**: Zero-maintenance continuous monitoring, validity checks
  - **Gitleaks**: Fast pre-commit blocking, prevents secrets from ever reaching GitHub
- **Benefits**: Defense in depth, eliminates `.secrets.baseline` maintenance, <90% false positive reduction
- **Trade-off**: Dual tool management accepted for stronger security posture

7. **Python CLI + just** for notebook command group (testable, rich UX)
8. **Hierarchical git tags** for compliance (`{category}/{identifier}-{date}`)
9. **5 MB warning, 10 MB block** for notebook size limits
10. **Minimal templates** with required metadata and guidance
11. **Future experiment tracking** integration (defer to ALLiaNCE data stack)

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
   - `just notebook create` interactive flow
   - Pre-commit hook contracts (metadata validation, size check)
   - Integration with nbstripout, Gitleaks, and GitHub Secret Scanning
   - Gitleaks configuration for notebook metadata allowlisting
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

## Hybrid Secret Scanning Implementation (Defense in Depth)

**Approach**: Option 4 from `research-secret-scanning.md` - GitHub Secret Scanning + Gitleaks

### Layer 1: Gitleaks (Pre-commit Blocking)

**Purpose**: Prevent secrets from ever reaching GitHub repository

**Implementation**:
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.18.0
  hooks:
    - id: gitleaks
```

**Configuration** (`.gitleaks.toml`):
```toml
title = "ai-kit gitleaks config"

[allowlist]
description = "Allowlist for notebook metadata"

# Ignore hex strings in notebook metadata (not actual secrets)
[[allowlist.regexes]]
description = "Notebook metadata hex strings"
regex = '''\"hashed_secret\": \"[a-f0-9]{40}\"'''

# Use default Gitleaks rules for all other patterns
```

**Benefits**:
- Fast local validation (<2 seconds for typical notebook)
- Blocks commits before push
- No network dependency
- Developer gets immediate feedback

### Layer 2: GitHub Secret Scanning (Continuous Monitoring)

**Purpose**: Catch secrets that bypass pre-commit hooks, verify validity, monitor history

**Implementation**:
1. Enable in repository settings: `Settings` → `Security` → `Code security and analysis` → `Secret scanning` → `Enable`
2. Optional: Enable push protection if GitHub Advanced Security available
3. Configure alert notifications for security team

**Benefits**:
- Zero maintenance (no baseline files)
- 150+ provider patterns with automatic updates
- Validity checking (verifies if secrets are active)
- Scans entire git history when new patterns added
- Alerts in GitHub Security tab with remediation guidance

### Defense in Depth Rationale

**Why both tools?**

1. **Complementary strengths**:
   - Gitleaks: Fast, local, immediate blocking
   - GitHub: Comprehensive, validity checking, continuous monitoring

2. **Multiple failure points**:
   - Developer bypasses pre-commit → GitHub catches it
   - Gitleaks pattern gap → GitHub's 150+ providers catch it
   - Secret added via web UI → GitHub detects it

3. **Different detection windows**:
   - Gitleaks: Before commit
   - GitHub: After push, continuous history scanning

4. **Acceptable trade-offs**:
   - Dual tool management: Minimal (Gitleaks config is static)
   - Performance: Gitleaks adds <2s to pre-commit
   - Complexity: Both tools have simple configurations

### Migration from detect-secrets

See `MIGRATION_SECRET_SCANNING.md` for detailed steps:
1. Enable GitHub Secret Scanning (5 minutes)
2. Remove detect-secrets from pre-commit and dependencies (10 minutes)
3. Delete `.secrets.baseline` (465 lines eliminated)
4. Add Gitleaks with notebook metadata allowlist (15 minutes)
5. Update documentation (README, CONTRIBUTING, notebooks/README)

**Timeline**: 1 week with validation period

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
