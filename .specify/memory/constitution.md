<!--
SYNC IMPACT REPORT
==================
Version Change: 1.9.0 → 1.10.0
Rationale: MINOR version bump - Expanded Principle I (EU AI Act Compliance) with French Government High-Risk Use Cases section, Risk Assessment Workflow, and High-Risk AI Mandatory Artifacts. This provides concrete guidance for ALLiaNCE incubations based on domain expert input on EU AI Act compliance.

Modified Sections:
- Principle I: EU AI Act Compliance (NON-NEGOTIABLE)
  * Added "French Government High-Risk Use Cases" section with two categories:
    - Category A (Primary ALLiaNCE Scope): French State services (agent-facing + citizen-facing) - Legal assistance, social benefits eligibility, speech-to-text transcription
    - Category B (Advisory Scope): Food safety, energy/critical infrastructure, defense systems
  * Clarified ai-kit scope: French State services (l'État), not territorial collectivities or hospitals
  * Added concrete examples from ALLiaNCE incubations: Conseil d'État assistant, employment law assistants, OpenGateLLM transcription
  * Added "Risk Assessment Workflow" with 5-step process for risk classification
  * Added "Transcription Audio Risk Assessment Decision Tree" for context-dependent systems
  * Added "High-Risk AI Mandatory Artifacts" section specifying required documentation:
    - Risk Management Documentation
    - Data Governance Plan
    - Technical Documentation (model cards, performance metrics)
    - Human Oversight Design
    - Audit Trail System
    - Instructions for Deployers
    - Incident Response Plan
    - Context Classification Document (for dual-risk systems)
  * Clarified ai-kit responsibilities for each High-Risk category (audit logging, bias testing, explainability tools)
  * Added OpenGateLLM-specific guidance for transcription compliance

Added Sections: N/A (expanded existing Principle I)

Removed Sections: N/A

Templates Requiring Updates:
- ✅ .specify/templates/spec-template.md - COMPLETED: Added "EU AI Act Risk Classification" section with:
  * Risk level determination (Prohibited/High-Risk/Limited/Minimal)
  * Annex III reference if High-Risk
  * Context-dependent classification table for multi-use-case systems
  * High-Risk compliance trigger checklist
  * Scope change monitoring requirements
- ✅ .specify/templates/plan-template.md - COMPLETED: Updated "Constitution Check" and added:
  * Detailed EU AI Act risk classification validation sub-checklist
  * "High-Risk AI Mandatory Artifacts Checklist" section with 8 artifact categories
  * Documentation location guidance for each artifact type
  * Compliance status tracking and gap identification
- ⚠️ .specify/templates/tasks-template.md - Add task categories for High-Risk AI compliance:
  * Risk management documentation tasks
  * Data governance and bias testing tasks
  * Audit trail implementation tasks
  * Human oversight UI/UX tasks
  * Deployer instructions documentation tasks

Follow-up TODOs:
- Create OpenGateLLM Compliance Guide documenting transcription risk classification
- Update existing feature specs to include EU AI Act risk classification
- Create example High-Risk AI project demonstrating mandatory artifacts
- Develop bias testing and explainability tool templates for ai-kit
- Create audit logging and human oversight UI pattern library
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

**French Government High-Risk Use Cases**:

The following use cases are common in French Government AI services and typically fall under **High-Risk AI** classification per EU AI Act Annex III:

**A. French State Services (Primary ALLiaNCE Scope)**:

Includes both agent-facing services for State public servants (agents publics d'État) and citizen-facing public services.

- **Legal Assistance Systems** (Annex III, Point 8):
  - AI systems assisting judicial or administrative authorities in legal research, interpretation, or case analysis
  - Examples: Conseil d'État legal assistant, employment law response assistants (droit de réponse au travail)
  - **Critical Requirements**: Human oversight mandatory, decisions must remain with human authorities, full audit trail of AI recommendations, transparency about AI limitations in legal reasoning
  - **Deployer Obligation**: Legal professionals must validate all AI-generated legal analysis before use
  - **ai-kit Responsibilities**: Provide audit logging, human-in-the-loop UI patterns, explainability tools for legal reasoning

- **Social Benefits Eligibility Systems** (Annex III, Point 5(b)):
  - AI systems evaluating eligibility for public assistance, benefits, or social services
  - AI systems providing guidance on citizen entitlements and rights (ayants droit)
  - Examples: Benefits eligibility calculators, rights information assistants, social aid attribution systems
  - **Critical Requirements**: Non-discrimination testing, explainability of eligibility decisions, human review for denials, clear appeal mechanisms, representative training data across socio-economic groups
  - **Deployer Obligation**: Social workers must verify AI eligibility determinations, especially for denials
  - **ai-kit Responsibilities**: Provide bias testing tools, explainability frameworks, human review workflows, appeal tracking systems

- **Speech-to-Text & Audio Transcription Systems** (Context-Dependent Risk):
  - AI systems for automatic transcription of speech to text
  - Examples: OpenGateLLM transcription functionality, meeting minutes automation, accessibility services

  **Risk Classification (Context-Dependent)**:

  - **Limited Risk** (Most Common):
    - General transcription for internal meetings, notes, documentation
    - Accessibility services (subtitling, assistive technologies)
    - Public information dissemination
    - **Requirements**: Transparency obligations (disclose AI use), accuracy standards, privacy protections

  - **High-Risk** (Administrative/Legal Contexts):
    - Transcription feeding into administrative decision-making processes
    - Transcription of official proceedings (judicial, regulatory hearings)
    - Transcription used as evidence or official record in benefits eligibility, legal determinations
    - **Requirements**: Full High-Risk AI compliance (risk management, data governance, human oversight, audit trails, technical documentation)

  **Critical Requirements (All Contexts)**:
  - Accuracy standards appropriate to use case (higher for administrative/legal contexts)
  - Human review mandatory for High-Risk contexts (official records, legal proceedings)
  - Privacy protections for recorded speech data (GDPR compliance)
  - Clear disclosure when AI transcription is used
  - Data retention and deletion policies
  - No speaker identification/biometric analysis without explicit legal basis

  **OpenGateLLM Integration**:
  - ai-kit MUST provide risk assessment guidance for OpenGateLLM transcription use cases
  - Teams MUST classify their transcription use case (Limited vs. High-Risk) in `spec.md`
  - High-Risk transcription projects MUST activate full compliance workflow
  - Document transcription accuracy requirements and validation procedures in `plan.md`

**B. Critical Infrastructure & Specialized Sectors (Advisory Scope)**:

The following High-Risk categories are less common in ALLiaNCE incubations but may be encountered when advising other administrations:

- **Food Safety & Supply Chain** (Annex III, Point 2):
  - AI systems managing food safety components (e.g., food traceability)
  - AI systems controlling critical food supply chain operations
  - **Ministries Concerned**: Agriculture, Economy
  - **Note**: ALLiaNCE does not typically incubate these systems but may provide ai-kit guidance to responsible administrations

- **Energy & Critical Infrastructure** (Annex III, Point 2):
  - AI systems managing energy production, distribution, or grid stability
  - AI systems controlling critical infrastructure safety components
  - **Ministries Concerned**: Ecological Transition, Economy
  - **Note**: ALLiaNCE does not typically incubate these systems but may provide ai-kit guidance to responsible administrations

- **Defense & Security Systems** (Annex III, Point 1):
  - AI systems for weapons systems, military applications, or defense infrastructure
  - **Ministries Concerned**: Armed Forces (Armées), Interior (Intérieur)
  - **Note**: Outside ALLiaNCE scope; specialized defense AI frameworks apply

**Scope Clarification**:
- ai-kit is primarily designed for **French State digital services** (Category A), serving both:
  - **Agent-facing services**: Tools and systems for State public servants (agents publics d'État)
  - **Citizen-facing services**: Public-facing digital services for citizens
- Primary mission concerns the State (l'État), not territorial collectivities (collectivités territoriales) or hospitals
- Category B systems (critical infrastructure) require specialized compliance frameworks beyond ai-kit's scope
- Teams working on Category B systems should consult sector-specific AI regulations and ANSSI guidance
- ai-kit MAY provide foundational compliance tools but is NOT sufficient alone for critical infrastructure AI

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

**Risk Assessment Workflow**:

All ai-kit projects MUST conduct risk classification assessment at project inception:

1. **Identify Use Case**: Map project to Annex III categories using EU AI Act Compliance Checker
   - Review "French Government High-Risk Use Cases" section above for common patterns
   - Special attention: Context-dependent systems (e.g., transcription) require use case analysis
   - Use decision trees provided below for common dual-risk scenarios

2. **Document Classification**: Record risk level (Prohibited/High-Risk/Limited/Minimal) in `spec.md`
   - Include rationale for classification
   - For context-dependent systems, document all intended use cases and their individual risk levels
   - Reference specific Annex III points that apply

3. **High-Risk Trigger**: If High-Risk, activate mandatory compliance workflow:
   - Establish risk management system (document in `plan.md`)
   - Define data governance requirements (document in `data-model.md`)
   - Plan human oversight mechanisms (document in `contracts/`)
   - Prepare technical documentation for homologation dossier
   - Define accuracy, robustness, and cybersecurity targets
   - Plan for quality management system

4. **Compliance Validation**: Include risk classification in Constitution Check section of all design artifacts
   - Verify classification remains accurate as system evolves
   - Document any scope changes that affect risk level

5. **Ongoing Monitoring**: Re-assess risk classification when system capabilities or use cases evolve
   - Quarterly review for production systems
   - Immediate re-assessment if new features or use cases added
   - Document classification changes and trigger compliance updates if moving to higher risk category

**Transcription Audio Risk Assessment Decision Tree**:

For speech-to-text and audio transcription systems, use this decision tree to determine risk level:

1. **Is the transcription used to inform administrative decisions?**
   - YES → Likely High-Risk, continue to Q2
   - NO → Likely Limited Risk, verify with Q3

2. **Does the transcription feed into systems that determine:**
   - Citizen eligibility for benefits/services?
   - Legal or regulatory outcomes?
   - Official administrative records?
   - YES to any → **High-Risk AI** (Annex III, Point 5 or 8)
   - NO to all → Continue to Q3

3. **Is the transcription used for:**
   - Internal team collaboration?
   - Accessibility/subtitling?
   - General documentation?
   - YES → **Limited Risk AI** (transparency obligations only)

**When in doubt**: Classify as High-Risk and conduct full compliance assessment. It is safer to over-comply than under-comply.

**High-Risk AI Mandatory Artifacts**:

For High-Risk AI systems, ai-kit projects MUST produce the following documentation and deliverables:

- **Risk Management Documentation**:
  - Lifecycle risk assessment (inception, development, deployment, maintenance phases)
  - Risk mitigation strategies with implementation details
  - Residual risk acceptance documentation
  - Document in `plan.md` and maintain in `docs/risk-management/`

- **Data Governance Plan**:
  - Training/validation/testing data quality assurance procedures
  - Bias testing methodology and results
  - Representativeness validation across relevant population segments
  - Data provenance and lineage documentation
  - Document in `data-model.md` and maintain datasets documentation

- **Technical Documentation**:
  - System architecture and component descriptions
  - Model cards (for ML models): architecture, training data, performance metrics, limitations
  - Performance benchmarks and accuracy targets
  - Known limitations and failure modes
  - Document in `plan.md`, `research.md`, and technical specifications

- **Human Oversight Design**:
  - Mechanisms for human intervention in AI decision process
  - Override capabilities and escalation procedures
  - Training requirements for human overseers
  - Document in `contracts/` and UI/UX specifications

- **Audit Trail System**:
  - Automatic logging of AI decisions, inputs, outputs, and human interventions
  - Log retention policies compliant with legal requirements
  - Audit query and reporting capabilities
  - Document in `contracts/` and implementation specifications

- **Instructions for Deployers**:
  - Clear guidance on proper use and limitations
  - Human oversight requirements and procedures
  - Monitoring and maintenance recommendations
  - Incident response procedures
  - Document in `quickstart.md` and operational documentation

- **Incident Response Plan**:
  - Procedures for handling AI failures or unexpected behaviors
  - Bias incident detection and remediation
  - Compliance breach reporting procedures
  - Document in operational documentation and `plan.md`

- **Context Classification Document** (for context-dependent systems):
  - All intended use cases and contexts
  - Risk classification for each context
  - Controls to prevent Limited Risk system from being used in High-Risk context
  - Monitoring to detect scope creep into High-Risk territory
  - Document in `spec.md` and operational procedures

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

### XIII. Jupyter Notebook Discipline

ai-kit projects MUST maintain Jupyter notebooks in a top-level `notebooks/` directory with clear governance to balance exploratory data science workflows with security, reproducibility, and compliance requirements.

**Notebook Categories**:

Notebooks MUST be organized by purpose to clarify their role in the development lifecycle. Projects should define categories based on their needs, but MUST distinguish between:

- **Exploratory work**: Rapid experimentation and hypothesis testing
  - Not subject to SpecKit workflow requirements
  - May contain incomplete or experimental code
  - MUST NOT contain production credentials or sensitive data
  - Should be cleaned up or archived when insights are productionized

- **Learning materials**: Tutorials, examples, and educational content
  - Subject to documentation quality standards
  - MUST be reproducible and well-documented
  - Should be referenced in feature specifications and quickstart guides
  - Serve as living documentation for complex workflows

- **Production-informing work**: Notebooks that inform production decisions
  - Model evaluation, performance benchmarking, compliance reporting, stakeholder reports
  - MUST be reproducible and version-controlled
  - MUST document data sources, model versions, and evaluation criteria
  - Subject to EU AI Act documentation requirements for high-risk AI systems
  - May be parameterized for automated execution

- **Reference materials**: Templates and starter notebooks
  - Provide pre-structured notebooks with required metadata
  - Include security guidelines and category-specific requirements
  - Help enforce quality standards from the start

- **Archive**: Completed work preserved for audit trail
  - Retains historical record of decisions and migrations
  - Links to production code when applicable
  - Essential for compliance and regulatory review

**Category Selection**: Projects MUST provide clear guidance (e.g., decision tree) to help users select the appropriate category based on notebook purpose, audience, frequency, and governance requirements.

**Security Requirements (NON-NEGOTIABLE)**:

- Notebooks MUST NOT contain hardcoded credentials, API keys, or sensitive data
- Use environment variables or secure configuration management for secrets
- Implement `nbstripout` or equivalent to remove notebook outputs before commit
- Add `notebooks/**/*.ipynb` output patterns to `.gitignore` (keep source, ignore execution artifacts)
- Conduct security review before publishing notebooks to public repositories
- Document data sources and ensure compliance with GDPR and data protection regulations

**Quality Standards**:

- **Reproducibility**: Notebooks MUST include dependency specifications (requirements.txt, environment.yml, or uv workspace)
- **Documentation**: Each notebook MUST include:
  - Purpose and context (what question does this answer?)
  - Author and date
  - Data sources and versions
  - Expected runtime and resource requirements
  - Known limitations or assumptions
- **Version Control**: Notebooks MUST be committed with outputs stripped (use `nbstripout` pre-commit hook)
- **Code Quality**: Notebook code SHOULD follow Python standards (ruff linting where practical)
- **Cell Organization**: Use markdown cells to structure narrative, avoid monolithic code cells

**Integration with SpecKit Workflow**:

- **Exploratory work**: Not required to follow SpecKit workflow, but insights MUST be captured in specifications when productionized
- **Learning materials**: Should be referenced in feature specifications (spec.md) and quickstart guides
- **Production-informing work**: MUST be documented in `plan.md` research section and referenced in compliance documentation

**EU AI Act Compliance**:

For high-risk AI systems, production-informing notebooks MUST:

- Document model training data characteristics (representativeness, quality, completeness)
- Record model evaluation metrics and validation results
- Capture risk assessment findings and mitigation strategies
- Provide audit trail for model selection and hyperparameter tuning decisions
- Support technical documentation requirements for homologation dossier

**Tooling Standards**:

- **nbstripout**: Pre-commit hook to remove outputs before commit
- **nbconvert**: Convert notebooks to scripts or documentation formats
- **papermill**: Parameterize and execute notebooks programmatically for reproducible reporting
- **ruff**: Lint notebook code cells (via `nbqa` or similar)
- **uv**: Manage notebook dependencies within monorepo workspace

**Migration to Production**:

When notebook insights become production features:

1. Extract reusable code into `packages/` or `apps/` with proper testing
2. Document the notebook-to-production migration in feature specification
3. Archive exploratory notebooks to reduce clutter while preserving audit trail
4. Retain production-informing notebooks (especially compliance and evaluation) for regulatory review
5. Follow Principle XI (Specification-Driven Development) for production implementation

**Rationale**: Jupyter notebooks are essential for AI/ML experimentation and data science workflows, but without governance they become security risks, compliance liabilities, and sources of technical debt. This principle acknowledges the exploratory nature of notebooks while establishing guardrails that prevent common pitfalls: credential leakage, irreproducible results, and undocumented model decisions. By categorizing notebooks and integrating them with SpecKit workflow, we enable rapid innovation while maintaining traceability for compliance and production migration.

**References**:
- [Jupyter Project](https://jupyter.org/)
- [nbstripout](https://github.com/kynan/nbstripout)
- [Papermill](https://papermill.readthedocs.io/)
- [nbqa](https://github.com/nbQA-dev/nbQA)

### XIV. Streamlit-to-Production Bridge

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

### XV. Package Naming Consistency

ai-kit projects MUST use consistent package naming that frames all code under the `ai_kit` namespace to ensure clear ownership, prevent naming conflicts, and maintain architectural coherence across the monorepo.

**Package Structure Requirements**:

- All Python packages MUST be organized under the `ai_kit` namespace
- Applications in `apps/` MUST use structure: `apps/<app-name>/src/ai_kit/<app-name>/`
- Packages in `packages/` MUST use structure: `packages/<package-name>/src/ai_kit/<package-name>/`
- Example: CLI application → `apps/cli/src/ai_kit/cli/` (NOT `apps/cli/src/ai_kit_cli/`)
- Example: Notebook tools → `packages/notebook-tools/src/ai_kit/notebook_tools/` (NOT `packages/notebook-tools/src/notebook_tools/`)

**Import Consistency**:

- All imports MUST use the `ai_kit` namespace: `from ai_kit.cli import commands`
- Subpackages MUST be importable as: `from ai_kit.cli.commands import notebook`
- Avoid flat namespaces like `ai_kit_cli` that break namespace hierarchy

**Rationale for `ai_kit` Namespace**:

- **Clear Ownership**: All code is visibly part of the ai-kit project
- **Namespace Protection**: Prevents conflicts with external packages (e.g., `cli` is too generic, `ai_kit.cli` is specific)
- **Architectural Coherence**: Reinforces that all apps and packages are part of a unified system
- **Import Clarity**: Developers immediately recognize ai-kit code in imports
- **Monorepo Best Practice**: Aligns with Python namespace package conventions for multi-package repositories

**Exceptions**:

- Third-party integrations MAY use their own namespaces when wrapping external services
- Standalone tools intended for external distribution MAY use different namespaces if justified in Constitution Check

**Rationale**: Consistent package naming is fundamental to maintainability in monorepos. The `ai_kit` namespace ensures that all code is clearly identified as part of the ai-kit project, prevents naming collisions, and creates a coherent import structure. This principle prevents the common anti-pattern of inconsistent naming (e.g., `ai_kit_cli`, `notebook_tools`, `reflex_components`) that fragments the codebase and confuses developers about package relationships. By establishing this standard early, we ensure that as ai-kit grows, all packages remain architecturally aligned and easily discoverable.

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
- Jupyter notebook discipline and governance if applicable (Principle XIII)
- Streamlit-to-production support if applicable (Principle XIV)
- Package naming consistency under ai_kit namespace (Principle XV)

### Complexity Justification

Any deviation from these principles MUST be documented with:

- Specific technical or business rationale
- Explanation of why compliant alternatives are insufficient
- Plan to return to compliance if possible
- Approval from project stakeholders

**Version**: 1.10.0 | **Ratified**: 2025-10-11 | **Last Amended**: 2025-10-16
