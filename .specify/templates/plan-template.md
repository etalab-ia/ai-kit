# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: [e.g., Python 3.11, Swift 5.9, Rust 1.75 or NEEDS CLARIFICATION]  
**Primary Dependencies**: [e.g., FastAPI, UIKit, LLVM or NEEDS CLARIFICATION]  
**Storage**: [if applicable, e.g., PostgreSQL, CoreData, files or N/A]  
**Testing**: [e.g., pytest, XCTest, cargo test or NEEDS CLARIFICATION]  
**Target Platform**: [e.g., Linux server, iOS 15+, WASM or NEEDS CLARIFICATION]
**Project Type**: [single/web/mobile - determines source structure]  
**Performance Goals**: [domain-specific, e.g., 1000 req/s, 10k lines/sec, 60 fps or NEEDS CLARIFICATION]  
**Constraints**: [domain-specific, e.g., <200ms p95, <100MB memory, offline-capable or NEEDS CLARIFICATION]  
**Scale/Scope**: [domain-specific, e.g., 10k users, 1M LOC, 50 screens or NEEDS CLARIFICATION]

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with ai-kit constitution principles:

- [ ] **EU AI Act Compliance (Principle I)**: Has the AI system been classified according to EU AI Act risk categories? Are requirements for high-risk AI systems addressed (risk management, data governance, documentation, human oversight)?
- [ ] **RGAA Accessibility Compliance (Principle II)**: Do all UI components meet RGAA 4 criteria? Is automated accessibility testing included? Does the UX work on mobile, tablet, and desktop?
- [ ] **Security Homologation (Principle III)**: Is security risk assessment planned? Are homologation dossier requirements addressed? Is the homologation authority identified? Are security measures documented for RGS compliance?
- [ ] **Open Source & Digital Commons (Principle IV)**: Is the code published under an open source license? Are open source and sovereign solutions privileged over proprietary alternatives?
- [ ] **DSFR Design System Compliance (Principle V)**: Do UI components comply with DSFR guidelines? Are responsive design patterns implemented?
- [ ] **ProConnect Authentication (Principle VI)**: Is ProConnect authentication implemented for user-facing features?
- [ ] **User-Centered Iteration (Principle VII)**: Is user research planned? Are there plans for MVP release, user testing, and iteration? Will analytics be implemented?
- [ ] **Extensibility and Innovation (Principle VIII)**: Is the implementation extensible? Does it avoid tight coupling to specific service versions?
- [ ] **Developer Experience & Tooling (Principle IX)**: Does the project use Turborepo, uv, ruff, just, and pnpm? Is TypeScript usage (if any) justified for frontend integration points?
- [ ] **Python-First Development (Principle X)**: Is Python the primary language? Are non-Python components justified?
- [ ] **Specification-Driven Development (Principle XI)**: Does this feature follow the SpecKit workflow (specify → plan → tasks → implement)? Are all design artifacts present in specs/[###-feature-name]/? Is traceability maintained from spec to implementation?
- [ ] **French Government AI Stack Integration (Principle XII)**: Does the feature integrate with OpenGateLLM, EvalAP, or other government AI services where applicable?
- [ ] **Streamlit-to-Production Bridge (Principle XIII)**: If using Streamlit, is there a migration path to Reflex? Are ProConnect and DSFR integrations planned?

**Violations Requiring Justification**: [List any principle violations with rationale, or state "None"]

## Project Structure

### Documentation (this feature)

```
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
