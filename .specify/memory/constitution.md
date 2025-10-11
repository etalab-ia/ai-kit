<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0
Rationale: MINOR version bump - Added new Principle VII (Developer Experience & Tooling Consistency)

Modified Principles: N/A

Added Sections:
- Principle VII: Developer Experience & Tooling Consistency
  * Monorepo tooling standardization (Turborepo - mandatory, no alternatives)
  * Python ecosystem tooling (uv, ruff, just - mandatory)
  * Hybrid TypeScript/Python architecture guidance

Removed Sections: N/A

Templates Requiring Updates:
- ✅ plan-template.md: Constitution Check section updated to include Principle VII
- ✅ spec-template.md: Already aligned (no changes needed)
- ✅ tasks-template.md: Already aligned (no changes needed)

Follow-up TODOs: None
-->

# ai-kit Constitution

## Core Principles

### I. Python-First Development

ai-kit MUST prioritize Python as the primary development language to align with the expertise of French Government digital service teams. This principle recognizes that:

- Teams recruited for AI/GenAI projects predominantly have Pythonic backgrounds
- Reducing language barriers accelerates delivery and reduces technical debt
- Modern Python frameworks (e.g., Reflex) can deliver production-grade frontend experiences
- Python-first does not mean Python-only; strategic use of other technologies is permitted when justified

**Rationale**: Empowering teams to work within their expertise domain maximizes productivity and reduces the learning curve that has historically caused projects to stall or accumulate technical debt.

### II. Streamlit-to-Production Bridge

ai-kit MUST provide a clear migration path from Streamlit prototypes to production-ready applications. This principle addresses the common pattern where:

- Teams start with Streamlit for rapid stakeholder iteration
- Lack of frontend expertise causes Streamlit UIs to "stick" and become complex
- Cross-cutting concerns (auth, design systems) are retrofitted poorly
- Technical debt accumulates as experimental UIs face real-world demands

**Implementation Requirements**:
- Provide Reflex-based wrappers that can encapsulate Streamlit components
- Offer pre-built integrations for ProConnect authentication
- Include DSFR-compliant UI components and templates
- Enable incremental migration without full rewrites

**Rationale**: By acknowledging and supporting the Streamlit-first workflow, ai-kit reduces friction and provides an escape hatch before technical debt becomes insurmountable.

### III. French Government AI Stack Integration

ai-kit MUST provide first-class integrations with the emerging French Government AI ecosystem, including but not limited to:

- **OpenGateLLM**: Gateway for open-source and proprietary LLMs with RAG, vectorization, and transcription
- **EvalAP**: Evaluation framework with RAG and other AI metrics
- **L'assistant IA**: Chat experiences leveraging OpenGateLLM
- Future government-endorsed AI tools and services

**Requirements**:
- Provide SDK/client libraries for each integrated service
- Include example implementations and quickstart templates
- Document authentication, authorization, and compliance requirements
- Maintain compatibility as these services evolve

**Rationale**: Standardizing on government-approved AI infrastructure ensures compliance, reduces duplication, and enables teams to focus on domain-specific value rather than infrastructure.

### IV. ProConnect Authentication Standard

ai-kit MUST implement ProConnect (https://partenaires.proconnect.gouv.fr/docs/fournisseur-service) as the default authentication mechanism for government digital services.

**Requirements**:
- Provide ready-to-use ProConnect integration modules
- Support both development/testing and production ProConnect environments
- Include session management, token refresh, and logout flows
- Document compliance requirements and security best practices

**Rationale**: ProConnect is the government-mandated authentication system. Providing turnkey integration removes a common blocker and ensures compliance from day one.

### V. DSFR Design System Compliance

ai-kit MUST provide components and templates that comply with the French Government Design System (DSFR - https://www.systeme-de-design.gouv.fr/version-courante/fr).

**Requirements**:
- Offer DSFR-compliant UI components (buttons, forms, navigation, etc.)
- Provide layout templates that follow DSFR guidelines
- Include accessibility (a11y) features as mandated by DSFR
- Support responsive design patterns defined by DSFR
- Enable theming and customization within DSFR constraints

**Rationale**: DSFR compliance is mandatory for French Government digital services. Providing pre-built compliant components accelerates development and ensures consistency across government services.

### VI. Extensibility and Innovation

ai-kit MUST remain extensible to accommodate rapid innovation in the AI space, both within and outside the French Government ecosystem.

**Requirements**:
- Provide clear plugin/extension mechanisms
- Document integration patterns for new AI services
- Avoid tight coupling to specific versions of external services
- Support experimentation without breaking core functionality
- Maintain backward compatibility where feasible

**Rationale**: The AI landscape evolves rapidly. ai-kit must enable teams to adopt new tools and techniques without being constrained by framework limitations.

### VII. Developer Experience & Tooling Consistency

ai-kit MUST standardize on modern, Python-ecosystem-native tooling to minimize cognitive load and maximize developer productivity across teams.

**Monorepo Management**:
- Use **Turborepo** for managing multi-package codebases
- Standardize build, test, and deployment pipelines across all packages
- Enable efficient caching and parallel execution for CI/CD workflows
- Support incremental builds to accelerate development cycles

**Python Tooling Standards**:
- **uv**: Package and dependency management (replaces pip, pip-tools, virtualenv)
- **ruff**: Linting and code formatting (replaces flake8, black, isort)
- **just**: Task runner for common development commands (replaces Makefiles)

**Hybrid Architecture**:
- Python remains the primary language (Principle I)
- TypeScript is permitted for frontend integration points where it provides clear value
- Backend services MUST be Python-based
- Frontend components MAY use TypeScript when integrating with modern frameworks (e.g., Next.js for Reflex interop)
- All TypeScript usage MUST be justified in Constitution Check

**Rationale**: Tool proliferation fragments team knowledge and slows onboarding. Standardizing on modern, fast tools that respect Python-first culture enables teams to focus on domain problems rather than build system archaeology. Monorepo tooling prevents the "multiple disconnected repos" anti-pattern that complicates deployment of services with multiple running processes.

## French Government Integration Requirements

### Mandatory Integrations

All ai-kit projects MUST support:
- ProConnect authentication (Principle IV)
- DSFR design system compliance (Principle V)
- Structured logging compatible with government infrastructure
- Security and privacy standards per French Government guidelines

### Recommended Integrations

ai-kit projects SHOULD integrate with:
- OpenGateLLM for LLM access and RAG capabilities
- EvalAP for AI evaluation and metrics
- Government-approved data storage and processing services
- Centralized monitoring and observability platforms

### Integration Testing

New integrations with government services MUST include:
- Contract tests verifying API compatibility
- Authentication/authorization flow tests
- Error handling and fallback scenarios
- Documentation with example usage

## Development Workflow & Quality Standards

### Rapid Iteration Support

ai-kit MUST support the iterative development workflow common in AI projects:
- Enable quick prototyping with Streamlit or similar tools
- Provide migration paths to production-ready implementations
- Support A/B testing and experimentation
- Enable stakeholder demos at any stage

### Testing Discipline

While recognizing the experimental nature of AI development, ai-kit projects MUST:
- Include integration tests for government service integrations
- Test authentication and authorization flows
- Validate DSFR compliance for UI components
- Document testing approaches for AI/ML components (recognizing non-determinism)

### Documentation Requirements

All ai-kit features MUST include:
- Quickstart guides for common use cases
- Integration examples with government services
- Troubleshooting guides for common issues
- Migration guides (e.g., Streamlit to Reflex)

### Code Quality

ai-kit contributions MUST:
- Follow Python community standards (PEP 8, type hints where appropriate)
- Include docstrings for public APIs
- Provide clear error messages and logging
- Avoid unnecessary complexity (YAGNI principle)

## Governance

### Constitution Authority

This constitution supersedes all other development practices and guidelines for ai-kit. Any conflicts between this constitution and other documentation must be resolved in favor of the constitution.

### Amendment Process

Amendments to this constitution require:
1. Documented rationale explaining the need for change
2. Impact analysis on existing projects and integrations
3. Migration plan for projects affected by breaking changes
4. Approval from ai-kit maintainers
5. Version bump following semantic versioning (see below)

### Versioning Policy

Constitution versions follow semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Backward-incompatible changes to core principles or mandatory requirements
- **MINOR**: New principles, sections, or material expansions of guidance
- **PATCH**: Clarifications, wording improvements, non-semantic refinements

### Compliance Review

All feature specifications and implementation plans MUST include a Constitution Check section verifying compliance with:
- Python-first development (Principle I)
- Streamlit-to-production support if applicable (Principle II)
- Government AI stack integration requirements (Principle III)
- ProConnect authentication (Principle IV)
- DSFR compliance (Principle V)
- Extensibility considerations (Principle VI)
- Developer tooling standards and monorepo architecture (Principle VII)

### Complexity Justification

Any deviation from these principles MUST be documented with:
- Specific technical or business rationale
- Explanation of why compliant alternatives are insufficient
- Plan to return to compliance if possible
- Approval from project stakeholders

**Version**: 1.1.0 | **Ratified**: 2025-10-11 | **Last Amended**: 2025-10-11