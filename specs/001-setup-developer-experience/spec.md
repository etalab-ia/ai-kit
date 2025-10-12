# Feature Specification: Setup Developer Experience & Tooling for ai-kit

**Feature Branch**: `001-setup-developer-experience`  
**Created**: 2025-10-12  
**Status**: Draft  
**Input**: User description: "I'd like to address principle IX so that we can setup the developer experience and tooling we expect of users of ai-kit for ai-kit itself."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Core Developer Tooling Setup (Priority: P1)

As an ai-kit core contributor, I need the repository configured with standardized Python tooling (uv, ruff, just) so that I can develop, test, and maintain the codebase efficiently following the same standards we mandate for ai-kit users.

**Why this priority**: This is foundational - without proper tooling, all subsequent development work will be inconsistent and inefficient. It establishes the baseline developer experience that makes all other work possible.

**Independent Test**: Can be fully tested by cloning the repository, running setup commands, and verifying that linting, formatting, and task execution work correctly. Delivers immediate value by enabling consistent development practices.

**Acceptance Scenarios**:

1. **Given** a fresh clone of the ai-kit repository, **When** a developer runs the setup command, **Then** uv installs all dependencies and creates a working development environment
2. **Given** the development environment is set up, **When** a developer runs the lint command, **Then** ruff checks all Python code for style violations and reports results
3. **Given** code with formatting issues, **When** a developer runs the format command, **Then** ruff automatically fixes formatting to match project standards
4. **Given** the repository is configured, **When** a developer runs `just --list`, **Then** all available development tasks are displayed with descriptions

---

### User Story 2 - Monorepo Structure with Turborepo (Priority: P2)

As an ai-kit core contributor, I need the repository organized as a Python-first monorepo with Turborepo orchestration so that I can manage multiple packages (libraries, templates, tools) with a single shared virtual environment while benefiting from efficient caching and parallel execution.

**Why this priority**: ai-kit will contain multiple packages (core library, templates, CLI tools, etc.). Setting up monorepo infrastructure early prevents the "multiple disconnected repos" anti-pattern and enables efficient CI/CD. The hybrid approach (uv workspaces + Turborepo) combines Python-native dependency management with powerful task orchestration.

**Independent Test**: Can be tested by creating multiple packages in the `apps/` and `packages/` folders, making changes, and verifying that: (1) all Python packages share a single `.venv` managed by uv, and (2) Turborepo correctly caches builds and runs tasks in parallel. Delivers value by enabling multi-package development with Python-first tooling.

**Acceptance Scenarios**:

1. **Given** the monorepo structure is configured with `apps/` and `packages/` folders, **When** a developer runs the sync command, **Then** uv creates a single shared `.venv` at the repository root containing all package dependencies
2. **Given** Python packages are configured as uv workspaces, **When** a developer adds a new dependency to one package, **Then** the shared `.venv` is updated and the dependency is available to that package only
3. **Given** each Python package has a `package.json` with task scripts, **When** a developer runs a build command via Turborepo, **Then** Turborepo executes builds in dependency order with caching
4. **Given** a package has been built previously, **When** a developer rebuilds without changes, **Then** Turborepo uses cached results and skips unnecessary work
5. **Given** multiple packages need testing, **When** a developer runs tests via Turborepo, **Then** Turborepo executes tests in parallel across packages
6. **Given** a change to one package, **When** a developer rebuilds, **Then** only affected packages and their dependents are rebuilt

---

### User Story 3 - CI/CD Pipeline Integration (Priority: P3)

As an ai-kit core contributor, I need CI/CD pipelines configured to use the same tooling (uv, ruff, just, Turborepo) so that automated checks match local development and catch issues before merge.

**Why this priority**: Ensures consistency between local and CI environments, prevents "works on my machine" issues, and automates quality gates.

**Independent Test**: Can be tested by pushing code changes and verifying that CI runs linting, formatting checks, tests, and builds using the configured tooling. Delivers value by automating quality assurance.

**Acceptance Scenarios**:

1. **Given** a pull request is opened, **When** CI runs, **Then** ruff linting and formatting checks execute and report violations
2. **Given** code passes linting, **When** CI continues, **Then** all tests execute using uv-managed dependencies
3. **Given** tests pass, **When** CI builds packages, **Then** Turborepo caching reduces build time compared to clean builds
4. **Given** any check fails, **When** CI completes, **Then** the pull request is blocked from merging with clear error messages

---

### User Story 4 - Developer Documentation (Priority: P3)

As a new ai-kit contributor, I need clear documentation on how to set up my development environment and use the tooling so that I can start contributing quickly without tribal knowledge.

**Why this priority**: Reduces onboarding friction and ensures all contributors follow the same practices. Lower priority than tooling setup itself but critical for team scalability.

**Independent Test**: Can be tested by having a new contributor follow the documentation from scratch and successfully complete their first contribution. Delivers value by enabling self-service onboarding.

**Acceptance Scenarios**:

1. **Given** a new contributor reads the setup documentation, **When** they follow the steps, **Then** they have a working development environment without asking for help
2. **Given** a contributor wants to run tests, **When** they check the documentation, **Then** they find clear commands for running tests locally
3. **Given** a contributor wants to add a new package, **When** they check the documentation, **Then** they find instructions for creating packages in the monorepo structure
4. **Given** CI fails on a pull request, **When** a contributor checks the documentation, **Then** they find troubleshooting steps for common CI issues

---

### Edge Cases

- What happens when a developer has an older version of Python installed that doesn't meet minimum requirements?
- How does the system handle conflicts between globally installed tools (pip, virtualenv) and uv?
- What happens when Turborepo cache becomes corrupted or outdated?
- How does the system handle platform-specific differences (macOS vs Linux vs Windows)?
- What happens when a developer tries to use incompatible versions of dependencies?
- How does CI handle transient network failures when installing dependencies?
- What happens when a developer tries to import a package that's available in the shared `.venv` but not declared as a dependency?
- How does the system handle Python packages that have both Python and Node.js dependencies (e.g., for Reflex integration)?
- What happens when uv workspace configuration conflicts with Turborepo workspace configuration?

## Requirements *(mandatory)*

### Functional Requirements

**Python Tooling (Priority: Setup First)**
- **FR-001**: Repository MUST use uv for Python package and dependency management with workspace support
- **FR-002**: Repository MUST maintain a single shared `.venv` at the repository root for all Python packages
- **FR-003**: Repository MUST use ruff for linting and code formatting with a shared configuration
- **FR-004**: Repository MUST use just as the task runner with documented commands for common development tasks
- **FR-005**: Repository MUST specify minimum Python version requirements in root `pyproject.toml`

**Monorepo Structure (Priority: Setup After Python Tooling)**
- **FR-006**: Repository MUST follow the `apps/` and `packages/` folder structure
- **FR-007**: `apps/` folder MUST contain deployable applications with entry points (CLI tools, servers, etc.)
- **FR-008**: `packages/` folder MUST contain importable libraries without entry points (core, templates, configs, etc.)
- **FR-009**: Each Python package MUST have a `pyproject.toml` declaring its dependencies
- **FR-010**: Each Python package MUST have a minimal `package.json` with task scripts for Turborepo integration

**Turborepo Integration**
- **FR-011**: Repository MUST be configured as a Turborepo monorepo with `turbo.json` pipeline configuration
- **FR-012**: Turborepo MUST be configured with caching for builds, tests, and linting tasks
- **FR-013**: Turborepo MUST support parallel execution of independent tasks across packages
- **FR-014**: Each Python package's `package.json` MUST define scripts that delegate to Python tools (ruff, pytest, uv)

**Code Quality**
- **FR-015**: All Python code MUST pass ruff linting checks before merge
- **FR-016**: All Python code MUST be formatted with ruff using project-standard configuration
- **FR-017**: Repository MUST include pre-commit hooks for linting and formatting (optional for developers but recommended)

**CI/CD**
- **FR-018**: CI pipeline MUST use the same tooling versions as local development (uv, ruff, just, Turborepo)
- **FR-019**: CI pipeline MUST execute linting, formatting checks, tests, and builds on every pull request
- **FR-020**: CI MUST fail fast on linting or formatting violations before running expensive tests
- **FR-021**: CI MUST sync only the specific package being tested to catch undeclared dependencies

**Documentation**
- **FR-022**: Developer documentation MUST include setup instructions for the hybrid uv + Turborepo structure
- **FR-023**: Developer documentation MUST explain the `apps/` vs `packages/` distinction
- **FR-024**: Developer documentation MUST include common commands and troubleshooting guides
- **FR-025**: Repository MUST include a justfile with commands for: setup, sync, lint, format, test, build, clean

### Key Entities

- **Development Environment**: The local setup on a contributor's machine, including Python version, uv installation, Node.js (for Turborepo), and cloned repository with a single shared `.venv`
- **App**: A deployable application in the `apps/` folder with entry points (e.g., CLI tool, API server) that can be run independently
- **Package**: A shared library in the `packages/` folder without entry points (e.g., core library, templates, configs) that is imported by apps or other packages
- **Workspace**: A uv workspace member defined in the root `pyproject.toml` that represents either an app or package
- **Task**: A development operation (lint, format, test, build) that can be executed via just (high-level) or Turborepo (orchestration)
- **CI Pipeline**: Automated workflow that runs on pull requests to validate code quality and functionality using the same tooling as local development
- **Configuration Files**: Files that define tooling behavior:
  - `pyproject.toml` (root): uv workspace configuration, Python version, shared dependencies
  - `pyproject.toml` (per-package): Package-specific dependencies and metadata
  - `package.json` (root): Turborepo workspace configuration
  - `package.json` (per-package): Task scripts for Turborepo orchestration
  - `turbo.json`: Turborepo pipeline configuration with caching rules
  - `justfile`: High-level developer commands

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: New contributors can set up a working development environment in under 10 minutes following documentation
- **SC-002**: Repository maintains a single shared `.venv` at the root containing all package dependencies
- **SC-003**: Linting and formatting checks complete in under 30 seconds for typical code changes
- **SC-004**: Turborepo cache reduces CI build time by at least 50% for unchanged packages
- **SC-005**: 100% of Python code passes ruff linting and formatting checks
- **SC-006**: CI pipeline completes all checks (lint, format, test, build) in under 5 minutes for typical pull requests
- **SC-007**: Zero "works on my machine" issues due to environment differences between local and CI
- **SC-008**: CI catches undeclared dependencies by syncing only the package being tested
- **SC-009**: All common development tasks (setup, sync, lint, format, test) are executable via single just commands
- **SC-010**: Developer documentation receives positive feedback from at least 3 new contributors during onboarding
- **SC-011**: Repository structure clearly separates deployable apps from importable packages
