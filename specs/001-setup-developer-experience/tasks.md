# Implementation Tasks: Setup Developer Experience & Tooling

**Feature**: 001-setup-developer-experience | **Branch**: `001-setup-developer-experience` | **Generated**: 2025-10-13  
**Total Tasks**: 35 tasks across 6 phases | **Estimated Effort**: 12-16 hours

## Overview

Tasks organized by user story for independent implementation and testing. Each phase delivers a complete, testable increment.

**MVP Scope**: User Story 1 (Core Developer Tooling) - Delivers immediate value  
**Parallel Opportunities**: Tasks marked [P] can run in parallel

---

## Phase 1: Setup & Prerequisites

### T001: Update .gitignore for Python + Node.js [P]
**File**: `/.gitignore` | **Story**: Setup  
Add Python patterns (`.venv/`, `__pycache__/`, `*.pyc`, `dist/`, `.pytest_cache/`, `.ruff_cache/`, `uv.lock`) and Node.js patterns (`node_modules/`, `pnpm-lock.yaml`, `.turbo/`, `*.log`)

### T002: Create repository folder structure [P]
**Files**: `/apps/`, `/packages/` | **Story**: Setup  
Create folders with `.gitkeep` and README.md explaining purpose

---

## Phase 2: User Story 1 - Core Developer Tooling (P1)

**Goal**: Enable consistent Python development with uv, ruff, and just

**Test Criteria**: Clone repo → `just setup` <10min → `just lint/format` works → pre-commit hooks run

### T003: Create root pyproject.toml
**File**: `/pyproject.toml` | **Story**: US1  
Configure uv workspace (members=["apps/*", "packages/*"]), ruff (line-length=100, target="py312"), requires-python=">=3.12"

### T004: Create justfile
**File**: `/justfile` | **Story**: US1  
Add commands: setup, sync, lint, format, test, build, clean with descriptions

### T005: Create .pre-commit-config.yaml
**File**: `/.pre-commit-config.yaml` | **Story**: US1  
Configure ruff hooks (lint + format) with fail_fast=true

### T006: Create root package.json
**File**: `/package.json` | **Story**: US1  
Configure Volta (node=22.14.0), packageManager (pnpm@10.14.0), workspaces, Turborepo devDep

### T007: Create pnpm-workspace.yaml
**File**: `/pnpm-workspace.yaml` | **Story**: US1  
Mirror uv workspace: packages=["apps/*", "packages/*"]

### T008: Initialize uv workspace
**Command**: `uv sync --all-packages` | **Story**: US1  
Create `.venv/` at root, generate `uv.lock`, commit lockfile

### T009: Install Node.js dependencies
**Command**: `corepack enable && pnpm install` | **Story**: US1  
Install Turborepo, generate `pnpm-lock.yaml`

### T010: Install pre-commit hooks
**Command**: `pre-commit install` | **Story**: US1  
Install hooks, test with intentional formatting issues

### T011: Test US1 acceptance scenarios
**Story**: US1  
Validate: fresh clone → setup works → lint/format work → `just --list` shows commands → setup time <10min

**Checkpoint**: ✅ US1 Complete - Core tooling functional

---

## Phase 3: User Story 2 - Monorepo Structure (P2)

**Goal**: Multi-package development with shared .venv and Turborepo

**Test Criteria**: Multiple packages share .venv → Turborepo caches → parallel execution → only affected packages rebuild

### T012: Create turbo.json
**File**: `/turbo.json` | **Story**: US2  
Configure pipeline: lint, format, test, build with caching and dependencies

### T013: Create example package (core) [P]
**Directory**: `/packages/core/` | **Story**: US2  
Create pyproject.toml, package.json, src/ai_kit_core/__init__.py, tests/, README.md

### T014: Create example app (cli) [P]
**Directory**: `/apps/cli/` | **Story**: US2  
Create pyproject.toml (depends on core), package.json, src/ai_kit_cli/main.py, tests/, README.md

### T015: Sync workspace with examples
**Command**: `uv sync --all-packages` | **Story**: US2  
Verify both packages in shared .venv, local imports work

### T016: Test Turborepo caching
**Story**: US2  
Run build twice → verify cache hits → modify core → verify only core+cli rebuild

### T017: Test parallel execution
**Story**: US2  
Create third package (templates), run lint → verify parallel execution

### T018: Test US2 acceptance scenarios
**Story**: US2  
Validate: single .venv → add dependency works → caching works → parallel works → selective rebuild works

**Checkpoint**: ✅ US2 Complete - Monorepo functional

---

## Phase 4: User Story 3 - CI/CD Pipeline (P3)

**Goal**: Automate quality checks with same tooling as local

**Test Criteria**: CI runs on PR → lint/format/test execute → Turborepo caching works → failures block merge → strict package isolation

### T019: Create GitHub Actions CI workflow
**File**: `/.github/workflows/ci.yml` | **Story**: US3  
Jobs: lint, format-check, test, build with matrix for packages, strict sync per package (`uv sync --package <name>`)

### T020: Configure Turborepo caching for CI
**File**: `/.github/workflows/ci.yml` | **Story**: US3  
Configure GitHub Actions cache for Turborepo (CI-only optimization). Add `actions/cache@v4` step to cache `.turbo` directory with key based on OS + turbo + git SHA. Add restore-keys for cache fallback. This provides CI-only caching (not shared with local dev). Note: True remote caching via Vercel Remote Cache can be added later if desired for team-wide cache sharing.

### T021: Add pre-commit validation workflow
**File**: `/.github/workflows/pre-commit.yml` | **Story**: US3  
Run `pre-commit run --all-files` on PR

### T022: Test CI with intentional failures
**Story**: US3  
Test: lint violations → format issues → failing tests → undeclared dependencies → verify clear errors

### T023: Test US3 acceptance scenarios
**Story**: US3  
Validate: CI runs → checks execute → caching works → failures block → CI time <5min → strict isolation works

**Checkpoint**: ✅ US3 Complete - CI/CD functional

---

## Phase 5: User Story 4 - Developer Documentation (P3)

**Goal**: Enable self-service onboarding

**Test Criteria**: New contributor follows docs → sets up environment → finds test commands → adds packages → troubleshoots CI

### T024: Update root README.md
**File**: `/README.md` | **Story**: US4  
Add: Getting Started, Quick Setup, Development Workflow, Monorepo Structure, Adding Packages, Troubleshooting

### T025: Create CONTRIBUTING.md
**File**: `/CONTRIBUTING.md` | **Story**: US4  
Add: Environment Setup, Code Quality, Testing, PR Process, Monorepo Guidelines, Common Tasks, Troubleshooting, Getting Help

### T026: Add inline documentation [P]
**Files**: `/pyproject.toml`, `/package.json`, `/turbo.json`, `/justfile` | **Story**: US4  
Add explanatory comments to all config files

### T027: Create CI troubleshooting guide [P]
**File**: `/docs/troubleshooting-ci.md` | **Story**: US4  
Sections: Linting Failures, Formatting, Tests, Undeclared Dependencies, Cache Issues, Environment Differences

### T028: Test US4 acceptance scenarios
**Story**: US4  
Validate: new contributor follows docs → setup works → finds commands → adds packages → troubleshoots CI → collect feedback

**Checkpoint**: ✅ US4 Complete - Documentation comprehensive

---

## Phase 6: Polish & Cross-Cutting Concerns

### T029: Pin all tool versions
**Files**: `/pyproject.toml`, `/package.json`, `/.pre-commit-config.yaml` | **Story**: Polish  
Pin: Python 3.12+, Node 22.14.0, pnpm 10.14.0, Turborepo ^2.5.8, ruff v0.14.0

### T030: Add platform-specific setup [P]
**File**: `/docs/setup-platform-specific.md` | **Story**: Polish  
Guides for: macOS, Linux, Windows, Docker

### T031: Document .venv edge cases [P]
**File**: `/docs/troubleshooting-venv.md` | **Story**: Polish  
Sections: Conflicting Dependencies, Import Errors, Version Conflicts, Corrupted .venv, Platform Issues

### T032: Document Turborepo cache recovery [P]
**File**: `/docs/troubleshooting-turborepo.md` | **Story**: Polish  
Sections: Cache Corruption, Cache Misses, Slow Builds, add `cache-clear` to justfile

### T033: Document dependency updates [P]
**File**: `/docs/updating-dependencies.md` | **Story**: Polish  
Sections: Python Dependencies, Node Dependencies, Tool Versions, Testing, Rollback

### T034: Validate all success criteria
**Story**: Polish  
Verify all 12 SC pass: SC-001 (setup <10min), SC-002 (single .venv), SC-003 (lint <30s), SC-004 (cache ≥50%), SC-005 (100% ruff), SC-006 (CI <5min), SC-007 (no "works on my machine"), SC-008 (catches undeclared deps), SC-009 (just commands), SC-010 (positive feedback), SC-011 (clear structure), SC-012 (auto version switching)

### T035: Final documentation review
**Files**: All docs | **Story**: Polish  
Review all docs for clarity, accuracy, typos, broken links, consistent formatting

**Checkpoint**: ✅ All Complete - Production ready

---

## Dependencies & Execution

### Critical Path
```
[T001, T002] → T003→T004→T005→T006→T007→T008→T009→T010→T011 (US1)
  → T012→[T013,T014]→T015→T016→T017→T018 (US2)
  → T019→T020→T021→T022→T023 (US3)
  → T024→T025→[T026,T027]→T028 (US4)
  → [T029,T030,T031,T032,T033]→T034→T035 (Polish)
```

### Parallel Opportunities
- **US1**: T001 || T002
- **US2**: T013 || T014 (after T012)
- **US4**: T026 || T027 (after T025)
- **Polish**: T030 || T031 || T032 || T033 (after T029)

---

## Implementation Strategy

### MVP (Sprint 1): US1 Only
- Tasks: T001-T011
- Time: 2-3 hours
- Delivers: Consistent Python development environment

### Incremental Delivery
- **Sprint 1**: US1 (T001-T011)
- **Sprint 2**: US2 (T012-T018)
- **Sprint 3**: US3 + US4 (T019-T028)
- **Sprint 4**: Polish (T029-T035)

### Success Metrics
- **Quantitative**: Setup <10min, Lint <30s, CI <5min, Cache ≥50%, 100% ruff compliance
- **Qualitative**: Zero "works on my machine", positive feedback, clear structure, auto version switching

---

## Next Steps

1. Review task list with team
2. Begin Sprint 1 (US1) implementation
3. Test MVP with new contributor
4. Iterate based on feedback
5. Proceed to Sprint 2 (US2)
