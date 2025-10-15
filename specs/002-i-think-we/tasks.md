# Tasks: Jupyter Notebook Support

**Input**: Design documents from `/specs/002-i-think-we/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Not explicitly requested in specification - focusing on implementation tasks

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions
- **Monorepo infrastructure**: `apps/cli/`, `notebooks/`, `packages/`, `.pre-commit-config.yaml`, `justfile`
- All paths relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for unified ai-kit CLI

- [x] T001 Create `apps/cli/` directory structure with `src/ai_kit/cli/` package (per Constitution Principle XV - unified ai_kit namespace)
- [x] T002 Create `apps/cli/pyproject.toml` with dependencies (click/typer, questionary, rich, nbformat, ruamel.yaml)
- [x] T003 [P] Create `notebooks/` directory structure with 6 categories (exploratory, tutorials, evaluations, compliance, reporting, templates)
- [x] T004 [P] Add `.gitkeep` files to each notebook category directory
- [x] T005 [P] Create `docs/notebooks/` directory for governance documentation
- [x] T006 Configure `apps/cli/` as uv workspace package in root `pyproject.toml`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core CLI infrastructure and shared utilities that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create `apps/cli/src/ai_kit/cli/__init__.py` with version info and namespace package configuration
- [x] T008 Create `apps/cli/src/ai_kit/cli/main.py` with CLI entry point and command routing
- [x] T009 [P] Create `apps/cli/src/ai_kit/cli/core/config.py` for CLI configuration management
- [x] T010 [P] Create `apps/cli/src/ai_kit/cli/core/validators.py` for shared validation logic
- [x] T011 [P] Create `apps/cli/src/ai_kit/cli/core/templates.py` for template management utilities
- [x] T012 [P] Create `apps/cli/src/ai_kit/cli/utils/git.py` for git operations (tags, history, status)
- [x] T013 [P] Create `apps/cli/src/ai_kit/cli/utils/prompts.py` for interactive prompts (questionary wrappers)
- [x] T014 [P] Create `apps/cli/src/ai_kit/cli/utils/output.py` for formatted output (rich console)
- [x] T015 Create `apps/cli/src/ai_kit/cli/commands/__init__.py` for command group registration
- [x] T016 Add `notebook` command group registration to `justfile` (routes to `apps/cli/`)
- [x] T017 [P] Create test structure in `apps/cli/tests/` mirroring source layout (commands/, core/, utils/ subdirectories) with pytest configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Security-Compliant Notebook Creation (Priority: P1) 🎯 MVP

**Goal**: Enable developers to create and commit notebooks without credential leakage or compliance violations

**Independent Test**: Create notebook with test credentials, commit it, verify outputs stripped and credentials blocked

### Implementation for User Story 1

- [x] T018 [P] [US1] Add `nbstripout` to root `pyproject.toml` dev dependencies
- [x] T019 [P] [US1] Add `detect-secrets` to root `pyproject.toml` dev dependencies  
- [x] T020 [US1] Configure `nbstripout` hook in `.pre-commit-config.yaml` for `notebooks/**/*.ipynb`
- [x] T021 [US1] Configure `detect-secrets` hook in `.pre-commit-config.yaml` with `.secrets.baseline`
- [x] T022 [US1] Create `.secrets.baseline` file with `detect-secrets scan --baseline .secrets.baseline`
- [x] T023 [P] [US1] Implement notebook size check validator in `apps/cli/src/ai_kit/cli/core/validators.py` (warn at 5 MB, block at 10 MB per FR-006a, support CLI mode with `--check-size` flag for pre-commit hooks)
- [x] T024 [P] [US1] Implement metadata validation logic in `apps/cli/src/ai_kit/cli/core/validators.py` (check required fields: purpose, author, category per FR-013, support CLI mode with `--check-metadata` flag for pre-commit hooks)
- [x] T025 [US1] Create custom pre-commit hook for metadata validation in `.pre-commit-config.yaml` (Python script using `repos: local` hook type, entry point: `python -m ai_kit.cli.core.validators --check-metadata`, validates required fields per category)
- [x] T026 [US1] Create custom pre-commit hook for size check in `.pre-commit-config.yaml` (Python script using `repos: local` hook type, entry point: `python -m ai_kit.cli.core.validators --check-size`, warns at 5MB, blocks at 10MB)
- [x] T027 [P] [US1] Update `.gitignore` with notebook execution artifacts patterns (`.ipynb_checkpoints/`, `**/*-checkpoint.ipynb`)
- [x] T028 [US1] Create `docs/notebooks/governance.md` with security requirements and best practices
- [x] T029 [US1] Test pre-commit hooks with sample notebook containing credentials (verify block)
- [x] T030 [US1] Test pre-commit hooks with sample notebook with outputs (verify strip)

**Checkpoint**: Security enforcement is active - notebooks cannot be committed with credentials or outputs

---

## Phase 4: User Story 2 - Organized Notebook Categories (Priority: P2)

**Goal**: Enable team members to understand where to place notebooks based on purpose and governance requirements

**Independent Test**: Create notebooks in each category, verify correct governance rules enforced

### Implementation for User Story 2

- [x] T031 [P] [US2] Create exploratory template in `notebooks/templates/exploratory-template.ipynb` with metadata structure
- [x] T032 [P] [US2] Create tutorial template in `notebooks/templates/tutorial-template.ipynb` with documentation standards
- [x] T033 [P] [US2] Create evaluation template in `notebooks/templates/evaluation-template.ipynb` with metrics documentation
- [x] T034 [P] [US2] Create compliance template in `notebooks/templates/compliance-template.ipynb` with EU AI Act checklist
- [x] T035 [P] [US2] Create reporting template in `notebooks/templates/reporting-template.ipynb` with papermill parameters
- [x] T036 [US2] Implement category configuration in `apps/cli/src/ai_kit/cli/core/config.py` (6 categories: exploratory, tutorials, evaluations, compliance, reporting, templates with governance levels)
- [x] T037 [US2] Implement template loading logic in `apps/cli/src/ai_kit/cli/core/templates.py` (copy from notebooks/templates/ and populate metadata)
- [x] T038 [US2] Implement category-specific metadata validation in `apps/cli/src/ai_kit/cli/core/validators.py` (different required fields per category)
- [x] T039 [US2] Update metadata validation hook to check category matches directory location
- [x] T040 [US2] Create `docs/notebooks/governance.md` section on category selection decision tree
- [x] T041 [US2] Test metadata validation with notebooks in wrong directories (verify error)
- [x] T042 [US2] Test metadata validation with missing required fields per category (verify error)

**Checkpoint**: All 6 categories have templates and validation rules - notebooks properly organized

---

## Phase 5: User Story 2 (continued) - Notebook Creation CLI Command

**Goal**: Provide `just notebook create` command for guided notebook creation

**Independent Test**: Run `just notebook create`, follow prompts, verify notebook created with correct metadata

### Implementation for User Story 2 (CLI)

- [x] T043 [US2] Create `apps/cli/src/ai_kit/cli/commands/notebook.py` with command group structure (imports: from ai_kit.cli.core import config, validators, templates)
- [x] T044 [US2] Implement `create` subcommand in `notebook.py` with interactive prompts (category, name, purpose, author) using questionary for UX
- [x] T045 [US2] Implement category selection prompt with descriptions using `questionary.select()`
- [x] T046 [US2] Implement notebook name validation (no spaces, valid filename)
- [x] T047 [US2] Implement purpose prompt with minimum length validation (10 characters)
- [x] T048 [US2] Implement author prompt with git config default
- [x] T049 [US2] Implement category-specific prompts (model version for evaluations, risk level for compliance, etc.)
- [x] T050 [US2] Implement template copying and metadata population logic
- [x] T051 [US2] Implement confirmation prompt with summary display
- [x] T052 [US2] Implement success message with next steps guidance
- [x] T053 [US2] Add error handling for file exists, template not found, invalid input
- [x] T054 [US2] Register `notebook create` command in `apps/cli/src/ai_kit/cli/main.py`
- [x] T055 [US2] Update `justfile` with `notebook` command that routes to CLI
- [x] T056 [US2] Test `just notebook create` end-to-end with each category
- [x] T057 [US2] Test error cases (duplicate name, invalid category, missing template)

**Checkpoint**: Developers can create notebooks via `just notebook create` with proper metadata

---

## Phase 6: User Story 3 - Reproducible Notebook Execution (Priority: P3)

**Goal**: Enable team members to run each other's notebooks and get same results

**Independent Test**: One developer creates notebook with dependencies, another clones repo and executes successfully

### Implementation for User Story 3

- [x] T058 [P] [US3] Add `papermill` to root `pyproject.toml` dev dependencies for parameterized execution
- [x] T059 [P] [US3] Add `nbconvert` to root `pyproject.toml` dev dependencies for format conversion
- [x] T060 [P] [US3] Add `nbqa` to root `pyproject.toml` dev dependencies for ruff linting
- [x] T061 [US3] Configure ruff linting for notebooks via nbqa in `.pre-commit-config.yaml` (optional, non-blocking)
- [x] T062 [US3] Update templates with dependency documentation section (requirements.txt, uv workspace)
- [x] T063 [US3] Update templates with data source documentation section (paths, versions, access methods)
- [x] T064 [US3] Update reporting template with papermill parameter examples
- [x] T065 [US3] Create `docs/notebooks/governance.md` section on reproducibility best practices
- [x] T066 [US3] Create example parameterized reporting notebook in `notebooks/reporting/example-report.ipynb`
- [x] T067 [US3] Test papermill execution with example reporting notebook
- [x] T068 [US3] Test nbconvert to script format with example notebook

**Checkpoint**: Notebooks are reproducible with documented dependencies and parameterization support

---

## Phase 7: User Story 4 - Notebook-to-Production Migration (Priority: P4)

**Goal**: Enable developers to migrate validated notebook code to production with proper documentation

**Independent Test**: Create exploratory notebook, extract to package, document migration, delete notebook (git history preserves)

### Implementation for User Story 4

- [x] T069 [US4] Implement `migrate` subcommand in `apps/cli/src/ai_kit/cli/commands/notebook.py` (document migration from notebook to production code per FR-026)
- [x] T070 [US4] Implement migration documentation prompt (destination package/app, rationale)
- [x] T071 [US4] Implement git commit SHA capture for exploratory notebooks before deletion
- [x] T072 [US4] Implement migration record generation (markdown format with git references)
- [x] T073 [US4] Implement guidance for exploratory notebook deletion vs. compliance/evaluation retention
- [x] T074 [US4] Create `docs/notebooks/migration-guide.md` with notebook-to-production patterns
- [x] T075 [US4] Update templates with migration documentation section
- [x] T076 [US4] Test `just notebook migrate` with exploratory notebook (verify git SHA captured)
- [x] T077 [US4] Test migration documentation generation (verify markdown format correct)

**Checkpoint**: Notebook-to-production migration is documented with git audit trail

---

## Phase 8: User Story 4 (continued) - Git Tagging for Compliance

**Goal**: Enable compliance officers to tag notebooks for regulatory review

**Independent Test**: Compliance officer reviews notebook, creates git tag, tag is discoverable for audit

### Implementation for User Story 4 (Git Tagging)

- [x] T078 [US4] Implement git tag creation utilities in `apps/cli/src/ai_kit/cli/utils/git.py` (hierarchical format: category/identifier-date per FR-027)
- [x] T079 [US4] Implement tag naming convention validation (category/identifier-date format)
- [x] T080 [US4] Implement tag discovery utilities (list tags by category)
- [x] T081 [US4] Create `docs/notebooks/compliance-officer-guide.md` with git tagging workflow
- [x] T082 [US4] Document tag naming conventions in compliance officer guide
- [x] T083 [US4] Document tag discovery commands in compliance officer guide
- [x] T084 [US4] Create example compliance notebook in `notebooks/compliance/example-audit.ipynb`
- [x] T085 [US4] Test git tag creation for compliance notebook (verify format correct)
- [x] T086 [US4] Test git tag discovery (verify tags listed by category)

**Checkpoint**: Compliance officers can tag notebooks for audit trail

---

## Phase 9: User Story 5 - EU AI Act Compliance Documentation (Priority: P5)

**Goal**: Enable compliance officers to generate technical documentation for high-risk AI systems

**Independent Test**: Create production-adjacent notebook with model evaluation, verify all EU AI Act elements present

### Implementation for User Story 5

- [x] T087 [US5] Update compliance template with EU AI Act documentation checklist
- [x] T088 [US5] Update compliance template with training data characteristics section
- [x] T089 [US5] Update compliance template with risk assessment findings section
- [x] T090 [US5] Update compliance template with model selection audit trail section
- [x] T091 [US5] Update evaluation template with EU AI Act evaluation metrics requirements
- [x] T092 [US5] Update evaluation template with validation methodology documentation
- [x] T093 [US5] Create `docs/notebooks/governance.md` section on EU AI Act compliance requirements
- [x] T094 [US5] Create example compliance notebook for high-risk AI system in `notebooks/compliance/example-high-risk-ai.ipynb`
- [x] T095 [US5] Create example evaluation notebook with EU AI Act metrics in `notebooks/evaluations/example-model-eval.ipynb`
- [x] T096 [US5] Test compliance notebook against EU AI Act checklist (verify all elements present)

**Checkpoint**: Compliance notebooks support EU AI Act technical documentation requirements

---

## Phase 10: Additional CLI Commands (SHOULD requirements)

**Goal**: Provide additional CLI commands for better developer experience

**Independent Test**: Each command works independently and provides useful output

### Implementation for Additional Commands

- [x] T097 [P] Implement `list` subcommand in `apps/cli/src/ai_kit/cli/commands/notebook.py` (list notebooks by category per FR-008a)
- [x] T098 [P] Implement `validate` subcommand in `apps/cli/src/ai_kit/cli/commands/notebook.py` (manual validation per FR-008b)
- [x] T099 [P] Implement `delete` subcommand in `apps/cli/src/ai_kit/cli/commands/notebook.py` (safe deletion with confirmation per FR-008d)
- [x] T100 [P] Implement `stats` subcommand in `apps/cli/src/ai_kit/cli/commands/notebook.py` (repository statistics per FR-008f)
- [x] T101 Implement notebook metadata parsing for `list` command (show purpose, author, last modified)
- [x] T102 Implement validation result formatting for `validate` command (same as pre-commit hooks)
- [x] T103 Implement git history preservation guidance for `delete` command
- [x] T104 Implement statistics aggregation for `stats` command (count by category, sizes, dates)
- [x] T105 [P] Test `just notebook list` with multiple notebooks in each category
- [x] T106 [P] Test `just notebook validate` with valid and invalid notebooks
- [x] T107 [P] Test `just notebook delete` with confirmation flow
- [x] T108 [P] Test `just notebook stats` with populated notebook directories

**Checkpoint**: All CLI commands functional and provide good developer experience

---

## Phase 11: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, testing, and improvements that affect multiple user stories

- [x] T109 [P] Complete `docs/notebooks/governance.md` with all sections (security, categories, reproducibility, migration, compliance, edge cases from spec.md L109-119)
- [x] T110 [P] Complete `docs/notebooks/compliance-officer-guide.md` with git tagging workflow and examples
- [x] T111 [P] Complete `docs/notebooks/migration-guide.md` with notebook-to-production patterns and edge case handling
- [x] T112 [P] Create `README.md` in `notebooks/` directory with quick start guide
- [x] T113 [P] Create `README.md` in `apps/cli/` directory with development guide
- [x] T114 [P] Add CLI command help text and examples to all subcommands
- [x] T115 [P] Add unit tests for validators in `apps/cli/tests/core/test_validators.py`
- [x] T116 [P] Add unit tests for template management in `apps/cli/tests/core/test_templates.py`
- [x] T117 [P] Add unit tests for configuration in `apps/cli/tests/core/test_config.py`
- [x] T118 [P] Add unit tests for git utilities in `apps/cli/tests/utils/test_git.py`
- [x] T119 [P] Add unit tests for prompts in `apps/cli/tests/utils/test_prompts.py`
- [x] T120 [P] Add unit tests for output formatting in `apps/cli/tests/utils/test_output.py`
- [x] T121 [P] Add integration tests for notebook commands in `apps/cli/tests/commands/test_notebook.py`
- [x] T122 Update root `README.md` with notebook support section and link to `docs/notebooks/governance.md`
- [x] T123 Update `quickstart.md` in specs directory with final validation steps
- [x] T124 Run full pre-commit hook suite on all template notebooks (verify pass)
- [x] T125 Run `just notebook create` for each category and commit (verify full workflow)
- [x] T126 Performance optimization: CLI startup time < 1 second (measured with `time just notebook --help` on cold start, average of 5 runs, excluding first run for cache warmup)
- [x] T127 Security review: Verify no credentials in templates or documentation
- [x] T128 Accessibility review: Verify CLI output is screen-reader friendly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - US1 (Security) → US2 (Categories) → US2 (CLI) → US3 (Reproducibility) → US4 (Migration) → US4 (Tagging) → US5 (Compliance)
  - Sequential dependencies due to shared infrastructure (templates, validators, CLI commands)
- **Additional Commands (Phase 10)**: Depends on US2 (CLI) completion
- **Polish (Phase 11)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1 - Security)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2 - Categories)**: Depends on US1 (needs security hooks in place)
- **User Story 2 (CLI)**: Depends on US2 (Categories) (needs templates and validators)
- **User Story 3 (P3 - Reproducibility)**: Depends on US2 (needs templates to update)
- **User Story 4 (P4 - Migration)**: Depends on US2 (CLI) (extends CLI commands)
- **User Story 4 (Tagging)**: Depends on US4 (Migration) (same story, sequential parts)
- **User Story 5 (P5 - Compliance)**: Depends on US2 (needs templates to update)

### Within Each User Story

- Pre-commit hooks before CLI commands (security first)
- Templates before CLI create command (need templates to copy)
- Validators before commands (need validation logic)
- Core implementation before additional commands
- Story complete before moving to next priority

### Parallel Opportunities

- Phase 1: T003, T004, T005 can run in parallel (different directories)
- Phase 2: T009-T014 can run in parallel (different files)
- Phase 3: T018, T019, T023, T024, T027 can run in parallel (different files)
- Phase 4: T031-T035 can run in parallel (different template files)
- Phase 6: T058-T060 can run in parallel (different dependencies)
- Phase 10: T097-T100, T105-T108 can run in parallel (different subcommands)
- Phase 11: T109-T118 can run in parallel (different documentation/test files)

---

## Parallel Example: User Story 2 (Templates)

```bash
# Launch all template creation tasks together:
Task T031: "Create exploratory template in notebooks/templates/exploratory-template.ipynb"
Task T032: "Create tutorial template in notebooks/templates/tutorial-template.ipynb"
Task T033: "Create evaluation template in notebooks/templates/evaluation-template.ipynb"
Task T034: "Create compliance template in notebooks/templates/compliance-template.ipynb"
Task T035: "Create reporting template in notebooks/templates/reporting-template.ipynb"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T017) - CRITICAL
3. Complete Phase 3: User Story 1 - Security (T018-T030)
4. Complete Phase 4: User Story 2 - Categories (T031-T042)
5. Complete Phase 5: User Story 2 - CLI (T043-T057)
6. **STOP and VALIDATE**: Test notebook creation and security enforcement
7. Deploy/demo if ready

**MVP Delivers**:
- ✅ Secure notebook creation (no credentials, outputs stripped)
- ✅ 6 organized categories with templates
- ✅ `just notebook create` command for guided creation
- ✅ Pre-commit hooks enforce governance

### Incremental Delivery

1. MVP (US1 + US2) → Test independently → Deploy/Demo
2. Add US3 (Reproducibility) → Test independently → Deploy/Demo
3. Add US4 (Migration + Tagging) → Test independently → Deploy/Demo
4. Add US5 (EU AI Act Compliance) → Test independently → Deploy/Demo
5. Add Additional Commands → Test independently → Deploy/Demo
6. Polish → Final validation → Production ready

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T017)
2. Developer A: User Story 1 (Security) (T018-T030)
3. Once US1 done:
   - Developer A: User Story 2 (Categories) (T031-T042)
   - Developer B: Start preparing User Story 3 dependencies
4. Once US2 done:
   - Developer A: User Story 2 (CLI) (T043-T057)
   - Developer B: User Story 3 (Reproducibility) (T058-T068)
5. Continue with US4, US5, Additional Commands in parallel where possible

---

## Notes

- [P] tasks = different files, no dependencies - can run in parallel
- [Story] label maps task to specific user story for traceability (US1-US5)
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Pre-commit hooks are critical path - test thoroughly
- CLI commands build incrementally - start with `create`, add others later
- Templates are foundation for good metadata - invest time in quality
- Documentation is essential for compliance officers and developers
- Unified CLI architecture enables future extensions (dataset, streamlit, compliance, experiment commands)

---

## Total Task Count: 128 tasks

**By User Story**:
- Setup: 6 tasks
- Foundational: 11 tasks
- US1 (Security): 13 tasks
- US2 (Categories): 12 tasks
- US2 (CLI): 15 tasks
- US3 (Reproducibility): 11 tasks
- US4 (Migration): 9 tasks
- US4 (Tagging): 9 tasks
- US5 (Compliance): 10 tasks
- Additional Commands: 12 tasks
- Polish: 20 tasks (includes 7 test tasks + 3 additional tasks)

**MVP Scope (US1 + US2)**: 57 tasks (Setup + Foundational + US1 + US2)
**Full Feature**: 128 tasks

**Estimated Effort**:
- MVP: 2-3 weeks (1 developer)
- Full Feature: 4-6 weeks (1 developer)
- With parallel team: 2-3 weeks for full feature
