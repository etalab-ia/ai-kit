# Feature Specification: [FEATURE NAME]

**Feature Branch**: `[###-feature-name]`  
**Created**: [DATE]  
**Status**: Draft  
**Input**: User description: "$ARGUMENTS"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - [Brief Title] (Priority: P1)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently - e.g., "Can be fully tested by [specific action] and delivers [specific value]"]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]
2. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 2 - [Brief Title] (Priority: P2)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

### User Story 3 - [Brief Title] (Priority: P3)

[Describe this user journey in plain language]

**Why this priority**: [Explain the value and why it has this priority level]

**Independent Test**: [Describe how this can be tested independently]

**Acceptance Scenarios**:

1. **Given** [initial state], **When** [action], **Then** [expected outcome]

---

[Add more user stories as needed, each with an assigned priority]

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- What happens when [boundary condition]?
- How does system handle [error scenario]?

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: System MUST [specific capability, e.g., "allow users to create accounts"]
- **FR-002**: System MUST [specific capability, e.g., "validate email addresses"]  
- **FR-003**: Users MUST be able to [key interaction, e.g., "reset their password"]
- **FR-004**: System MUST [data requirement, e.g., "persist user preferences"]
- **FR-005**: System MUST [behavior, e.g., "log all security events"]

*Example of marking unclear requirements:*

- **FR-006**: System MUST authenticate users via [NEEDS CLARIFICATION: auth method not specified - email/password, SSO, OAuth?]
- **FR-007**: System MUST retain user data for [NEEDS CLARIFICATION: retention period not specified]

### Key Entities *(include if feature involves data)*

- **[Entity 1]**: [What it represents, key attributes without implementation]
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]

## EU AI Act Risk Classification *(mandatory)*

<!--
  ACTION REQUIRED: Classify this feature's AI risk level according to EU AI Act.
  Review Constitution Principle I "French Government High-Risk Use Cases" and "Risk Assessment Workflow".
  Use decision trees for context-dependent systems (e.g., transcription).
-->

### Risk Level Determination

**Classification**: [Prohibited / High-Risk / Limited Risk / Minimal Risk]

**Annex III Reference** (if High-Risk): [e.g., "Annex III, Point 8 - Legal assistance systems"]

**Rationale**: 
[Explain why this classification applies. Reference specific use cases, decision-making impact, and citizen rights implications.]

### Context-Dependent Classification (if applicable)

<!--
  For systems like transcription that have different risk levels depending on use case.
  Document ALL intended use cases and their individual risk levels.
-->

| Use Case | Risk Level | Rationale | Compliance Requirements |
|----------|-----------|-----------|------------------------|
| [Use case 1] | [Risk level] | [Why this level] | [Specific requirements] |
| [Use case 2] | [Risk level] | [Why this level] | [Specific requirements] |

### High-Risk AI Compliance Trigger (if applicable)

<!--
  If this feature is classified as High-Risk, document the mandatory compliance workflow activation.
-->

**High-Risk Compliance Activated**: [Yes / No]

**If Yes, the following mandatory artifacts MUST be produced**:
- [ ] Risk Management Documentation (in `plan.md` and `docs/risk-management/`)
- [ ] Data Governance Plan (in `data-model.md`)
- [ ] Technical Documentation with model cards (in `plan.md`, `research.md`)
- [ ] Human Oversight Design (in `contracts/`)
- [ ] Audit Trail System (in `contracts/`)
- [ ] Instructions for Deployers (in `quickstart.md`)
- [ ] Incident Response Plan (in operational docs)
- [ ] Context Classification Document (if context-dependent)

**Scope Change Monitoring**: 
[Describe how the team will monitor for scope changes that could elevate risk classification]
