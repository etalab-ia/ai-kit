<!--
SYNC IMPACT REPORT
==================
Version Change: 1.7.0 → 1.7.1
Rationale: PATCH version bump - Reorganized principle ordering by moving Specification-Driven Development (formerly XIII) to position XI, renumbering subsequent principles for better logical flow

Modified Principles:
- Principle XI: Now "Specification-Driven Development with SpecKit" (formerly Principle XIII)
- Principle XII: Now "French Government AI Stack Integration" (formerly Principle XI)
- Principle XIII: Now "Streamlit-to-Production Bridge" (formerly Principle XII)

Rationale for Reordering:
- Specification-Driven Development (new XI) logically follows Python-First Development (X) as both are foundational development practices
- French Government AI Stack Integration (new XII) and Streamlit-to-Production Bridge (new XIII) are more specific implementation concerns that build on the foundational principles

Removed Sections: N/A

Templates Requiring Updates:
- ✅ plan-template.md: Updated principle numbers in Constitution Check
- ✅ spec-template.md: Already aligned (no principle-specific references)
- ✅ tasks-template.md: Already aligned (no principle-specific references)

Follow-up TODOs:
- Update feature spec 001-setup-developer-experience to reflect pnpm standardization
- Consider adding security homologation dossier template
- Consider adding risk assessment template aligned with ANSSI requirements
- Consider adding security documentation checklist for homologation
- Consider adding homologation workflow guide
-->

# ai-kit Constitution

## Core Principles

### I. EU AI Act Compliance (NON-NEGOTIABLE)

ai-kit projects MUST comply with the EU Artificial Intelligence Act, the first comprehensive AI regulation by a major regulator, which applies to AI systems placed on the EU market or whose output is used in the EU.

**Risk Classification**:
- **Prohibited AI**: Systems creating unacceptable risk (e.g., social scoring, manipulative AI) are banned
- **High-Risk AI**: Systems listed in Annex III or used as safety components require strict compliance
- **Limited Risk AI**: Transparency obligations (e.g., chatbots must disclose they are AI)
- **Minimal Risk**: Unregulated (e.g., spam filters, AI-enabled games)

**Requirements for High-Risk AI Systems**:
- Establish risk management system throughout the AI system's lifecycle
- Conduct data governance ensuring training/validation/testing datasets are representative, error-free, and complete
- Draw up technical documentation to demonstrate compliance
- Design for automatic record-keeping of events relevant for identifying risks
- Provide instructions for use to enable deployer compliance
- Design for human oversight capabilities
- Achieve appropriate levels of accuracy, robustness, and cybersecurity
- Establish quality management system

**General Purpose AI (GPAI) Requirements**:
- Provide technical documentation and instructions for use
- Comply with EU Copyright Directive
- Publish summary of content used for training
- For GPAI with systemic risk: conduct model evaluations, adversarial testing, track serious incidents, ensure cybersecurity protections

**Provider vs. Deployer Obligations**:
- **Providers** (developers): Bear majority of obligations if placing high-risk AI on EU market
- **Deployers** (users): Have lighter obligations when using high-risk AI in professional capacity
- Both EU and third-country providers/deployers are covered if AI output is used in EU

**Documentation Requirements**:
- Maintain technical documentation demonstrating compliance
- Document risk assessments for systems that may be high-risk
- Keep records of AI system lifecycle events
- Provide transparency about AI capabilities and limitations

**Rationale**: The EU AI Act is becoming a global standard for AI governance, similar to GDPR for data protection. French Government AI services must comply as they operate within the EU. Compliance ensures AI systems are safe, transparent, and respect fundamental rights. Non-compliance can result in significant penalties (up to €35M or 7% of global turnover for prohibited AI). Proactive compliance protects citizens and builds trust in government AI services.

**References**:
- [EU AI Act Official Site](https://artificialintelligenceact.eu/)
- [High-Level Summary](https://artificialintelligenceact.eu/high-level-summary/)
- [AI Act Compliance Checker](https://artificialintelligenceact.eu/assessment/eu-ai-act-compliance-checker/)
- [The AI Act Full Text](https://artificialintelligenceact.eu/the-act/)

### II. RGAA Accessibility Compliance (NON-NEGOTIABLE)

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

### III. Security Homologation (NON-NEGOTIABLE)

ai-kit projects MUST obtain security homologation (homologation de sécurité) before production deployment, as mandated by ANSSI and French government regulations for all public digital services.

**Regulatory Framework**:
- **RGS (Référentiel Général de Sécurité)**: Mandates security homologation for all online public services in France
- **Decree n°2022-513 (April 8, 2022)**: Extends homologation obligation to all information and communication systems for State entities and public establishments
- **Applies to**: State entities, public establishments, local authorities (collectivités territoriales)

**What is Security Homologation**:
Security homologation is a formal decision by an authority (autorité d'homologation) that:
- Certifies that cyber risks related to an information system are clearly identified, treated, and accepted at the highest organizational level
- Authorizes the deployment and maintenance in service of an information system
- Attests that implemented security measures are sufficient to face common cyber risks and specific identified risks
- Takes the form of a written decision (administrative note, signed document, or electronic decision)
- Has a maximum validity period of 3 years

**Homologation Process Requirements**:
- Conduct comprehensive risk assessment of the information system
- Identify and document all cyber risks (confidentiality, integrity, availability, traceability)
- Implement appropriate security measures to mitigate identified risks
- Document residual risks and obtain formal acceptance by homologation authority
- Prepare homologation dossier with technical and organizational security documentation
- Obtain formal written decision from homologation authority before production deployment
- Plan for periodic review and re-homologation (maximum 3 years)

**Consequences of Non-Homologation**:
- An information system without homologation decision is deemed unable to be deployed or maintained in service
- Absence of homologation means the system cannot legally operate in production
- Unfavorable opinion from homologation authority prevents deployment until risks are adequately addressed

**ai-kit Responsibilities**:
- Provide security documentation templates aligned with ANSSI and RGS requirements
- Include security risk assessment tools and methodologies
- Support homologation process workflows (risk identification, treatment, acceptance)
- Maintain comprehensive audit trails and security logs required for homologation dossier
- Enable security monitoring and incident response capabilities
- Document security architecture, measures, and controls for homologation dossier
- Facilitate preparation of homologation documentation throughout development lifecycle

**Integration with Other Principles**:
- Complements EU AI Act compliance (Principle I) for AI-specific security risks
- Builds on Security & Privacy Standards section requirements
- Requires secure ProConnect authentication implementation (Principle VI)
- Supports RGAA accessibility security requirements (Principle II)
- Aligns with open source transparency (Principle IV) for security auditing

**Rationale**: Security homologation is a legal obligation for French Government digital services, mandated by RGS and extended by the 2022 decree. It ensures that cyber risks are properly identified, managed, and accepted at the appropriate authority level before production deployment. Non-compliance prevents legal operation of digital services. ai-kit must facilitate this mandatory governance process from the start of development to enable teams to deploy compliant, secure services.

**References**:
- [ANSSI - L'homologation de sécurité](https://cyber.gouv.fr/lhomologation-de-securite)
- [ANSSI - Guide de l'homologation de sécurité (April 2025)](ressources/guide-homologation-securite-web-04-2025.pdf)
- [RGS - Référentiel Général de Sécurité](https://cyber.gouv.fr/le-referentiel-general-de-securite-rgs)
- [Decree n°2022-513](https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000045570774)

### IV. Open Source & Digital Commons (NON-NEGOTIABLE)

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

### V. DSFR Design System Compliance

ai-kit MUST provide components and templates that comply with the French Government Design System (DSFR - https://www.systeme-de-design.gouv.fr/version-courante/fr).

**Requirements**:
- Offer DSFR-compliant UI components (buttons, forms, navigation, etc.)
- Provide layout templates that follow DSFR guidelines
- Support responsive design patterns defined by DSFR (mobile-first approach)
- Enable theming and customization within DSFR constraints
- Ensure DSFR components inherit RGAA accessibility compliance (Principle II)
- Test UI components across device types (mobile, tablet, desktop)

**Rationale**: DSFR compliance is mandatory for French Government digital services. Providing pre-built compliant components accelerates development and ensures visual consistency across government services. DSFR is built on top of accessibility requirements, making it complementary to Principle II. DSFR's responsive patterns ensure services work across all devices.

### VI. ProConnect Authentication Standard

ai-kit MUST implement ProConnect (https://partenaires.proconnect.gouv.fr/docs/fournisseur-service) as the default authentication mechanism for government digital services.

**Requirements**:

- Provide ready-to-use ProConnect integration modules
- Support both development/testing and production ProConnect environments
- Include session management, token refresh, and logout flows
- Document compliance requirements and security best practices

**Rationale**: ProConnect is the government-mandated authentication system. Providing turnkey integration removes a common blocker and ensures compliance from day one.

### VII. User-Centered Iteration

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

### VIII. Extensibility and Innovation

ai-kit MUST remain extensible to accommodate rapid innovation in the AI space, both within and outside the French Government ecosystem.

**Requirements**:

- Provide clear plugin/extension mechanisms
- Document integration patterns for new AI services
- Avoid tight coupling to specific versions of external services
- Support experimentation without breaking core functionality
- Maintain backward compatibility where feasible

**Rationale**: The AI landscape evolves rapidly. ai-kit must enable teams to adopt new tools and techniques without being constrained by framework limitations.

### IX. Developer Experience & Tooling Consistency

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

**Node.js Tooling Standards**:

- **pnpm**: Package manager for Node.js dependencies and workspace management
- Other package managers (npm, yarn) or runtimes (bun) MAY be used but are not standardized
- pnpm provides efficient disk usage, strict dependency resolution, and native workspace support that complements Turborepo

**Hybrid Architecture**:

- Python remains the primary language (Principle X)
- TypeScript is permitted for frontend integration points where it provides clear value
- Backend services MUST be Python-based
- Frontend components MAY use TypeScript when integrating with modern frameworks (e.g., Next.js for Reflex interop)
- All TypeScript usage MUST be justified in Constitution Check

**Rationale**: Tool proliferation fragments team knowledge and slows onboarding. Standardizing on modern, fast tools that respect Python-first culture enables teams to focus on domain problems rather than build system archaeology. Monorepo tooling prevents the "multiple disconnected repos" anti-pattern that complicates deployment of services with multiple running processes. pnpm's workspace support aligns naturally with uv workspaces and Turborepo, creating a cohesive monorepo experience.

### X. Python-First Development

ai-kit MUST prioritize Python as the primary development language to align with the expertise of French Government digital service teams. This principle recognizes that:

- Teams recruited for AI/GenAI projects predominantly have Pythonic backgrounds
- Reducing language barriers accelerates delivery and reduces technical debt
- Modern Python frameworks (e.g., Reflex) can deliver production-grade frontend experiences
- Python-first does not mean Python-only; strategic use of other technologies is permitted when justified

**Rationale**: Empowering teams to work within their expertise domain maximizes productivity and reduces the learning curve that has historically caused projects to stall or accumulate technical debt.

### XI. Specification-Driven Development with SpecKit

ai-kit MUST serve as a reference implementation and exemplar of specification-driven development using SpecKit methodology. This principle establishes ai-kit as both a product that delivers value AND a demonstration of best practices for structured, traceable software development.

**Core Requirements**:

- All features MUST follow the specification → planning → implementation workflow
- All features MUST use SpecKit templates located in `.specify/templates/`
- All features MUST use SpecKit workflows located in `.windsurf/workflows/`
- Feature development MUST begin with `/speckit.specify` to create a specification
- Implementation planning MUST use `/speckit.plan` to generate design artifacts
- Task generation MUST use `/speckit.tasks` to create actionable work items
- All specifications MUST be stored in `specs/[###-feature-name]/` directories

**SpecKit Workflow Enforcement**:

- **Specification Phase**: Use `/speckit.specify` to create `spec.md` with user stories, requirements, and success criteria
- **Clarification Phase**: Use `/speckit.clarify` to identify and resolve underspecified areas
- **Planning Phase**: Use `/speckit.plan` to generate `plan.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`
- **Task Generation**: Use `/speckit.tasks` to create dependency-ordered `tasks.md` from design artifacts
- **Implementation Phase**: Use `/speckit.implement` to execute tasks systematically
- **Quality Assurance**: Use `/speckit.analyze` for cross-artifact consistency validation
- **Custom Checklists**: Use `/speckit.checklist` for feature-specific quality gates

**Documentation Structure**:

Each feature MUST maintain the following structure in `specs/[###-feature-name]/`:
- `spec.md`: Feature specification (from `/speckit.specify`)
- `plan.md`: Implementation plan (from `/speckit.plan`)
- `research.md`: Technical research and decisions (from `/speckit.plan`)
- `data-model.md`: Entity and relationship definitions (from `/speckit.plan`)
- `contracts/`: API contracts and interfaces (from `/speckit.plan`)
- `quickstart.md`: User-facing getting started guide (from `/speckit.plan`)
- `tasks.md`: Actionable task list (from `/speckit.tasks`)
- `checklists/`: Feature-specific quality checklists (from `/speckit.checklist`)

**Traceability Requirements**:

- Every implementation MUST trace back to a specification
- Every task MUST reference its source user story or requirement
- Every design decision MUST be documented in planning artifacts
- Constitution compliance MUST be verified in `plan.md` Constitution Check section

**Exemplar Responsibilities**:

ai-kit development MUST demonstrate:
- How to write clear, testable specifications
- How to decompose features into independent user stories
- How to plan implementation with proper dependency management
- How to maintain consistency across specification, design, and implementation
- How to use SpecKit workflows effectively in real-world scenarios
- How to balance agility with documentation discipline

**Integration with Other Principles**:

- Supports User-Centered Iteration (Principle VII) through structured user story decomposition
- Enables Security Homologation (Principle III) through comprehensive documentation
- Facilitates EU AI Act Compliance (Principle I) through traceable risk assessments
- Complements Developer Experience (Principle IX) with clear development workflows
- Aligns with Open Source (Principle IV) by making development process transparent and reusable

**Rationale**: Specification-driven development prevents the common failure modes of AI projects: scope creep, undocumented decisions, untraceable requirements, and accumulation of technical debt. By making ai-kit itself an exemplar of SpecKit methodology, we provide concrete, real-world examples that other French Government teams can study and replicate. This principle ensures that ai-kit's development process is as valuable as its code—demonstrating that structured development practices can coexist with rapid AI innovation. Teams adopting ai-kit will learn not just what to build, but how to build it with discipline and traceability.

**References**:
- SpecKit templates: `.specify/templates/`
- SpecKit workflows: `.windsurf/workflows/`
- Example specifications: `specs/001-setup-developer-experience/`

### XII. French Government AI Stack Integration

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

### XIII. Streamlit-to-Production Bridge

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

## French Government Integration Requirements

### Mandatory Integrations

All ai-kit projects MUST support:

- ProConnect authentication (Principle VI)
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

- EU AI Act compliance and risk classification (Principle I)
- RGAA accessibility compliance (Principle II)
- Security homologation preparation and requirements (Principle III)
- Open source licensing and digital commons (Principle IV)
- DSFR design system compliance (Principle V)
- ProConnect authentication (Principle VI)
- User-centered iteration and data-driven development (Principle VII)
- Extensibility considerations (Principle VIII)
- Developer tooling standards and monorepo architecture (Principle IX)
- Python-first development (Principle X)
- Specification-driven development with SpecKit workflows (Principle XI)
- Government AI stack integration requirements (Principle XII)
- Streamlit-to-production support if applicable (Principle XIII)

### Complexity Justification

Any deviation from these principles MUST be documented with:

- Specific technical or business rationale
- Explanation of why compliant alternatives are insufficient
- Plan to return to compliance if possible
- Approval from project stakeholders

**Version**: 1.7.1 | **Ratified**: 2025-10-11 | **Last Amended**: 2025-10-13
