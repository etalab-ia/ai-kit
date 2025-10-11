<!--
SYNC IMPACT REPORT
==================
Version Change: 1.1.0 → 1.4.0
Rationale: MINOR version bump - Elevated accessibility to standalone Principle V (RGAA), added Principle IX (Open Source & Digital Commons), added Principle X (User-Centered Iteration), added device-agnostic UX requirements

Modified Principles:
- Principle V: Split DSFR into two principles - RGAA Accessibility (new V) and DSFR Design System (now VI)
- Former Principle V (DSFR) → now Principle VI (DSFR, with RGAA reference)
- Former Principle VI (Extensibility) → now Principle VII
- Former Principle VII (Developer Tooling) → now Principle VIII

Added Sections:
- Principle V: RGAA Accessibility Compliance (NON-NEGOTIABLE)
  * 106 RGAA 4 criteria compliance
  * Accessible-by-default components
  * Automated accessibility testing
  * Legal mandate and penalties
  * Assistive technology support
  * Device-agnostic UX requirement (mobile, tablet, desktop)
- Principle IX: Open Source & Digital Commons (NON-NEGOTIABLE)
  * Mandatory open source licensing (MIT, Apache 2.0, or EUPL)
  * Public repositories on government platforms
  * Privilege open source and sovereign solutions
  * Community contribution and reusability
  * Aligned with DINUM digital strategy and beta.gouv standards
- Principle X: User-Centered Iteration
  * User research before building features
  * MVP-first approach with alpha → beta → production progression
  * Continuous validation with analytics and telemetry
  * Data-driven decisions based on actual usage patterns
  * Addresses "sticky Streamlit UI" problem

Modified Sections:
- Principle V (RGAA): Added device-agnostic UX mandate
- Principle VI (DSFR): Now explicitly references Principle V for accessibility inheritance and emphasizes responsive design

Removed Sections: N/A

Templates Requiring Updates:
- ✅ plan-template.md: Constitution Check section updated with new principle numbering
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

### V. RGAA Accessibility Compliance (NON-NEGOTIABLE)

ai-kit MUST ensure all digital services comply with RGAA 4 (Référentiel Général d'Amélioration de l'Accessibilité - https://accessibilite.numerique.gouv.fr/), the French Government accessibility standard.

**Requirements**:

- All UI components MUST meet RGAA 4 criteria (106 accessibility criteria based on WCAG)
- Provide accessible-by-default components and patterns
- Include automated accessibility testing in CI/CD pipelines
- Document accessibility features and ARIA patterns for each component
- Support assistive technologies (screen readers, keyboard navigation, etc.)
- Provide accessibility audit tools and guidance for teams
- Maintain accessibility declarations as required by law
- Ensure device-agnostic UX: services MUST work on mobile, tablet, and desktop unless explicitly justified

**Legal Context**:

- RGAA compliance is legally mandated for French Government digital services
- Non-compliance can result in legal penalties and service rejection
- Accessibility is a fundamental right, not an optional feature

**Rationale**: Accessibility ensures digital services are usable by all citizens, including those with disabilities. RGAA compliance is both a legal obligation and a moral imperative. Making accessibility a core principle ensures it's considered from day one, not retrofitted later. Device-agnostic design is part of accessibility—citizens access services from whatever device they have available.

### VI. DSFR Design System Compliance

ai-kit MUST provide components and templates that comply with the French Government Design System (DSFR - https://www.systeme-de-design.gouv.fr/version-courante/fr).

**Requirements**:
- Offer DSFR-compliant UI components (buttons, forms, navigation, etc.)
- Provide layout templates that follow DSFR guidelines
- Support responsive design patterns defined by DSFR (mobile-first approach)
- Enable theming and customization within DSFR constraints
- Ensure DSFR components inherit RGAA accessibility compliance (Principle V)
- Test UI components across device types (mobile, tablet, desktop)

**Rationale**: DSFR compliance is mandatory for French Government digital services. Providing pre-built compliant components accelerates development and ensures visual consistency across government services. DSFR is built on top of accessibility requirements, making it complementary to Principle V. DSFR's responsive patterns ensure services work across all devices.

### VII. Extensibility and Innovation

ai-kit MUST remain extensible to accommodate rapid innovation in the AI space, both within and outside the French Government ecosystem.

**Requirements**:

- Provide clear plugin/extension mechanisms
- Document integration patterns for new AI services
- Avoid tight coupling to specific versions of external services
- Support experimentation without breaking core functionality
- Maintain backward compatibility where feasible

**Rationale**: The AI landscape evolves rapidly. ai-kit must enable teams to adopt new tools and techniques without being constrained by framework limitations.

### VIII. Developer Experience & Tooling Consistency

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

### IX. Open Source & Digital Commons (NON-NEGOTIABLE)

ai-kit projects MUST produce open source code and privilege open source solutions and digital commons over proprietary alternatives, in accordance with the French Government's digital strategy.

**Requirements**:
- All ai-kit code MUST be published under an open source license (preferably MIT, Apache 2.0, or EUPL)
- Project repositories MUST be public on government-approved platforms (e.g., GitHub, GitLab)
- Privilege open source dependencies and tools over proprietary alternatives
- Privilege sovereign (French/European) solutions when choosing external services
- Document code clearly to enable reuse by other government teams
- Contribute improvements back to upstream open source projects when possible
- Publish reusable components as standalone libraries for the community

**Exceptions**:
- Security-sensitive configuration (credentials, API keys) MUST NOT be published
- Proprietary solutions MAY be used only when:
  - No suitable open source alternative exists
  - The proprietary solution is legally mandated
  - Exception is documented and justified in Constitution Check

**Rationale**: Open source ensures technical autonomy, avoids vendor lock-in, enables cost-sharing across administrations, leverages collective expertise, and ensures transparency and reusability of public solutions. This aligns with DINUM's digital strategy and the beta.gouv.fr quality standards. Open source is not just a technical choice—it's a democratic principle for public services.

**References**:
- [DINUM Digital Strategy](https://www.numerique.gouv.fr/numerique-etat/)
- [Pôle open source et communs numériques](https://code.gouv.fr/fr/)
- [Beta.gouv Quality Standards](https://doc.incubateur.net/communaute/gerer-son-produit/readme-doc-incubateur-net/qualite-logicielle/l-open-source-et-les-communs-numeriques-sont-privilegies)

### X. User-Centered Iteration

ai-kit projects MUST adopt iterative, user-centered development practices to ensure services meet real user needs rather than assumptions.

**User Research Requirements**:
- Conduct user research before building features (interviews, observations, surveys)
- Identify and validate user needs with actual users, not stakeholders alone
- Document user personas and journey maps for key workflows
- Test prototypes with representative users before full implementation

**Iterative Development**:
- Release minimum viable products (MVPs) early for user feedback
- Follow alpha → beta → production progression with user testing at each stage
- Iterate based on real user feedback, not internal assumptions
- Be willing to pivot or discard features that don't meet validated user needs

**Continuous Validation**:
- Implement analytics and telemetry to understand actual usage patterns
- Monitor user behavior post-launch to identify pain points
- Conduct regular usability testing with real users
- Use A/B testing for significant UX decisions when appropriate
- Collect and act on user feedback through multiple channels

**Data-Driven Decisions**:
- Base design and feature decisions on usage data, not hunches
- Track key metrics: task completion rates, error rates, user satisfaction
- Make analytics built-in, always-on, and accessible to the team
- Use data to prioritize improvements and validate hypotheses

**Rationale**: The "sticky Streamlit UI" problem occurs when teams skip user research and iteration, building based on assumptions. Mandating user-centered practices prevents technical debt accumulation and ensures AI services actually solve user problems. This is especially critical for government services where users may be less tech-savvy or using services under stress.

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

## Security & Privacy Standards

### Data Protection & Privacy

All ai-kit projects MUST comply with French and European data protection regulations:

**GDPR Compliance**:

- Implement data minimization: collect only necessary data
- Provide clear privacy notices and consent mechanisms
- Enable user data access, correction, and deletion rights (RGPD rights)
- Document data processing activities and legal bases
- Implement data retention policies with automatic deletion

**AI-Specific Privacy**:

- Document what data is used for AI model training vs. inference
- Implement mechanisms to prevent sensitive data leakage in AI outputs
- Provide transparency about AI decision-making processes
- Enable human review for high-stakes AI decisions
- Audit AI systems for bias and fairness regularly

### Security Requirements

**Authentication & Authorization**:

- Use ProConnect for user authentication (Principle IV)
- Implement role-based access control (RBAC) for internal users
- Follow principle of least privilege for service accounts
- Rotate credentials and API keys regularly
- Use secure session management with appropriate timeouts

**Data Security**:

- Encrypt data at rest and in transit (TLS 1.3+)
- Use government-approved encryption standards
- Implement secure key management practices
- Sanitize and validate all user inputs
- Protect against common vulnerabilities (OWASP Top 10)

**AI Security**:

- Implement rate limiting to prevent abuse of AI endpoints
- Validate and sanitize prompts to prevent injection attacks
- Monitor for adversarial inputs and model manipulation attempts
- Implement output filtering to prevent harmful content generation
- Document AI model provenance and supply chain security

**Audit & Compliance**:

- Maintain comprehensive audit logs for security-relevant events
- Implement log retention per government requirements
- Enable security monitoring and alerting
- Conduct regular security assessments and penetration testing
- Document incident response procedures

### Transparency & Explainability

For AI-powered features:

- Provide clear explanations of how AI decisions are made
- Disclose when users are interacting with AI vs. humans
- Document AI model limitations and known failure modes
- Enable users to understand and challenge AI decisions
- Maintain transparency about data sources and training methods

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
- RGAA accessibility compliance (Principle V)
- DSFR design system compliance (Principle VI)
- Extensibility considerations (Principle VII)
- Developer tooling standards and monorepo architecture (Principle VIII)
- Open source licensing and digital commons (Principle IX)
- User-centered iteration and data-driven development (Principle X)

### Complexity Justification

Any deviation from these principles MUST be documented with:

- Specific technical or business rationale
- Explanation of why compliant alternatives are insufficient
- Plan to return to compliance if possible
- Approval from project stakeholders

**Version**: 1.4.0 | **Ratified**: 2025-10-11 | **Last Amended**: 2025-10-11
