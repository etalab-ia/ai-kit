# Implementation Plan: Setup Developer Experience & Tooling for ai-kit

**Branch**: `001-setup-developer-experience` | **Date**: 2025-10-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-setup-developer-experience/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This feature establishes the foundational developer experience and tooling infrastructure for ai-kit itself, implementing Constitution Principle IX (Developer Experience & Tooling Consistency). The implementation creates a **hybrid Python-first monorepo** using:

- **Python tooling**: uv (workspace management), ruff (linting/formatting), just (task runner)
- **Node.js tooling**: Volta (Node.js version management with auto-switching), Corepack (pnpm version management), pnpm 10.x+ (package manager)
- **Monorepo orchestration**: Turborepo (task caching and parallel execution)
- **Structure**: `apps/` (deployable applications) and `packages/` (importable libraries) with single shared `.venv`
- **Code quality**: Mandatory pre-commit hooks, strict CI isolation per package

**Key Innovation**: The Volta + Corepack hybrid approach enables automatic Node.js version switching across projects, critical for government developers working on both legacy and modern codebases simultaneously.

## Technical Context

**Language/Version**: Python 3.12+, Node.js 22.x LTS  
**Primary Dependencies**: 
- Python: uv (0.7.x+), ruff (0.14.x+), just (1.43.x+)
- Node.js: Volta (2.0.x+), pnpm (10.x+), Turborepo (2.5.x+)
- Pre-commit framework for git hooks

**Storage**: N/A (infrastructure/tooling feature)  
**Testing**: Configuration validation, CI pipeline tests, integration tests for tooling setup  
**Target Platform**: Cross-platform (macOS, Linux, Windows) - developer workstations and CI/CD environments  
**Project Type**: Monorepo infrastructure (hybrid Python + Node.js tooling)  
**Performance Goals**: 
- Linting/formatting: <30 seconds for typical changes
- CI pipeline: <5 minutes for typical PRs
- Turborepo cache: ≥50% build time reduction for unchanged packages (CI-only via GitHub Actions cache)
- Setup time: <10 minutes for new contributors

**Constraints**: 
- Must support government developers working on multiple projects with different Node.js versions
- Must catch undeclared dependencies via strict package isolation in CI
- Must enforce code quality via mandatory pre-commit hooks
- Must maintain single shared `.venv` for all Python packages

**Scale/Scope**: 
- Initial setup: Repository root + 2-3 example packages (apps/ and packages/)
- Designed to scale to 10+ packages in monorepo
- Support for 5-10 concurrent contributors initially

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with ai-kit constitution principles:

- [x] **EU AI Act Compliance (Principle I)**: N/A - This is infrastructure/tooling setup, not an AI system. No AI risk classification needed.
- [x] **RGAA Accessibility Compliance (Principle II)**: N/A - No UI components in this feature (developer tooling only).
- [x] **Security Homologation (Principle III)**: Partially applicable - Security considerations include: (1) Pre-commit hooks enforce code quality gates, (2) CI pipeline validates dependencies, (3) Open source tooling choices enable security auditing. No separate homologation dossier needed for internal developer tooling.
- [x] **Open Source & Digital Commons (Principle IV)**: ✅ COMPLIANT - All tooling is open source (uv, ruff, just, Volta, pnpm, Turborepo). Repository will be published under open source license. No proprietary tools used.
- [x] **DSFR Design System Compliance (Principle V)**: N/A - No UI components in this feature.
- [x] **ProConnect Authentication (Principle VI)**: N/A - No user-facing authentication in developer tooling.
- [x] **User-Centered Iteration (Principle VII)**: ✅ COMPLIANT - Developer documentation will be tested with new contributors (SC-010). Setup process designed for <10 minute onboarding (SC-001). Feedback loop via contributor experience.
- [x] **Extensibility and Innovation (Principle VIII)**: ✅ COMPLIANT - Monorepo structure supports adding new packages. Turborepo enables experimentation without breaking core. Tool versions pinned but upgradeable. justfile provides extension points for custom tasks.
- [x] **Developer Experience & Tooling (Principle IX)**: ✅ COMPLIANT - **This feature directly implements Principle IX**. Uses all mandated tools: Turborepo, uv, ruff, just, pnpm. Volta + Corepack hybrid approach enhances DX beyond minimum requirements.
- [x] **Python-First Development (Principle X)**: ✅ COMPLIANT - Python is primary language (3.12+). Node.js tooling justified for Turborepo orchestration (industry standard for monorepos). Minimal Node.js usage (configuration only, no application code).
- [x] **French Government AI Stack Integration (Principle XI)**: N/A - Infrastructure feature, no AI service integration needed.
- [x] **Streamlit-to-Production Bridge (Principle XII)**: N/A - No Streamlit usage in this feature.

**Violations Requiring Justification**: None

**Key Compliance Notes**:
- This feature is the **foundation** for Principle IX compliance across all future ai-kit features
- Node.js tooling (Volta, pnpm, Turborepo) is justified as industry-standard monorepo orchestration, complementing Python-first development
- Security considerations addressed through code quality enforcement and dependency validation
- Open source commitment maintained throughout tooling stack

## Project Structure

### Documentation (this feature)

```
specs/001-setup-developer-experience/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (implementation plan)
├── research.md          # Phase 0: Tooling research and best practices
├── quickstart.md        # Phase 1: Developer onboarding guide
├── checklists/
│   └── requirements.md  # Specification quality checklist (completed)
└── tasks.md             # Phase 2: Implementation tasks (/speckit.tasks command)

Note: data-model.md and contracts/ not applicable for infrastructure feature
```

### Source Code (repository root)

```
ai-kit/                          # Repository root
├── .github/
│   └── workflows/
│       ├── ci.yml               # CI pipeline with strict package isolation
│       └── pre-commit.yml       # Pre-commit hook validation
│
├── .specify/                    # Specification framework (existing)
│   ├── memory/
│   │   └── constitution.md      # Updated with pnpm standardization (v1.6.2)
│   ├── scripts/
│   └── templates/
│
├── apps/                        # Deployable applications (NEW)
│   └── .gitkeep                 # Placeholder for future apps
│
├── packages/                    # Importable libraries (NEW)
│   └── .gitkeep                 # Placeholder for future packages
│
├── .venv/                       # Single shared virtual environment (NEW)
│
├── .gitignore                   # Updated for Python + Node.js
├── .pre-commit-config.yaml      # Pre-commit hooks configuration (NEW)
├── pyproject.toml               # Root: uv workspace config, Python 3.12+ (NEW)
├── uv.lock                      # Unified dependency lockfile (NEW)
├── package.json                 # Root: Turborepo + Volta + pnpm config (NEW)
├── pnpm-lock.yaml               # pnpm lockfile (NEW)
├── pnpm-workspace.yaml          # pnpm workspace configuration (NEW)
├── turbo.json                   # Turborepo pipeline configuration (NEW)
├── justfile                     # Task runner commands (NEW)
├── README.md                    # Updated with setup instructions
└── CONTRIBUTING.md              # Developer guide (NEW)
```

**Structure Decision**: **Monorepo with hybrid Python + Node.js tooling**

This structure implements the hybrid uv + Turborepo approach:

1. **Python workspace** (uv):
   - Root `pyproject.toml` defines workspace members in `apps/*` and `packages/*`
   - Single `.venv` at root contains all Python dependencies
   - Each package has its own `pyproject.toml` for dependencies

2. **Node.js workspace** (pnpm + Turborepo):
   - Root `package.json` defines workspaces and Volta/pnpm versions
   - `pnpm-workspace.yaml` mirrors Python workspace structure
   - Each package has minimal `package.json` with task scripts

3. **Separation of concerns**:
   - `apps/`: Deployable applications with entry points (CLI tools, servers)
   - `packages/`: Importable libraries without entry points (core, templates, configs)

4. **Configuration files**:
   - Python: `pyproject.toml` (root + per-package), `uv.lock`
   - Node.js: `package.json` (root + per-package), `pnpm-lock.yaml`, `pnpm-workspace.yaml`
   - Orchestration: `turbo.json`, `justfile`
   - Quality: `.pre-commit-config.yaml`, `.github/workflows/`

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

**Status**: No violations - Constitution Check passed with full compliance.

---

## Phase Completion Status

### ✅ Phase 0: Research & Technical Decisions (COMPLETE)

**Output**: `research.md` - Comprehensive research on tooling decisions

**Key Decisions**:
- Python tooling: uv (0.7.x+), ruff (0.14.x+), just (1.43.x+)
- Node.js tooling: Volta (2.0.x+), Corepack, pnpm (10.x+), Turborepo (2.5.x+)
- Monorepo structure: `apps/` and `packages/` folders
- CI strategy: Strict package isolation in ALL jobs
- Code quality: Mandatory pre-commit hooks

All version requirements verified against latest releases (as of 2025-10-13).

**Turborepo Caching Note**:
- Initial implementation uses GitHub Actions cache (CI-only)
- Achieves SC-004 (≥50% build time reduction) without external dependencies
- Future option: Self-hosted remote cache (open source) for team-wide cache sharing (CI + local dev)
- Self-hosted solution: ducktors/turborepo-remote-cache (MIT licensed, government-compatible)
- Storage options: Local filesystem, AWS S3, Azure Blob, GCS, Minio (full data sovereignty)
- See research.md for detailed caching strategy rationale

### ✅ Phase 1: Design & Documentation (COMPLETE)

**Outputs**:
- `quickstart.md` - Developer onboarding guide (<10 minute setup)
- Project structure defined in plan.md
- Configuration examples documented in research.md

**Notes**:
- `data-model.md` - N/A (infrastructure feature, no data entities)
- `contracts/` - N/A (no API contracts for tooling setup)

### ⏭️ Phase 2: Task Generation (NEXT STEP)

**Command**: `/speckit.tasks`

**Expected Output**: `tasks.md` with implementation tasks based on:
- Priority 1: Python tooling setup
- Priority 2: Monorepo structure and Node.js integration  
- Priority 3: CI/CD pipeline and documentation

---

## Next Steps

1. Run `/speckit.tasks` to generate implementation tasks
2. Begin implementation following task priorities
3. Test setup process with new contributor (validate SC-001: <10 minute setup)
4. Iterate based on feedback
