# Constitution Update Summary - Version 1.10.0

**Date**: 2025-10-16  
**Type**: MINOR version bump (1.9.0 → 1.10.0)  
**Focus**: Risk Classification Refinement for EU AI Act Compliance

## Executive Summary

Updated the ai-kit constitution with concrete guidance on EU AI Act risk classification based on domain expert input on French Government AI use cases. The update provides actionable workflows, decision trees, and mandatory artifacts for High-Risk AI systems.

## Key Changes

### 1. French Government High-Risk Use Cases (New Section in Principle I)

Added two categories of High-Risk AI use cases:

#### **Category A: French State Services (Primary ALLiaNCE Scope)**

Includes both agent-facing services (for State public servants) and citizen-facing services.

1. **Legal Assistance Systems** (Annex III, Point 8)
   - Examples: Conseil d'État legal assistant, employment law response assistants (droit de réponse au travail)
   - Requirements: Human oversight mandatory, full audit trail, transparency about AI limitations
   - ai-kit Responsibilities: Audit logging, human-in-the-loop UI patterns, explainability tools

2. **Social Benefits Eligibility Systems** (Annex III, Point 5(b))
   - Examples: Benefits eligibility calculators, rights information for ayants droit, social aid attribution
   - Requirements: Non-discrimination testing, explainability, human review for denials, appeal mechanisms
   - ai-kit Responsibilities: Bias testing tools, explainability frameworks, human review workflows

3. **Speech-to-Text & Audio Transcription Systems** (Context-Dependent Risk)
   - Examples: OpenGateLLM transcription, meeting minutes, accessibility services
   - **Dual Classification**:
     - **Limited Risk** (most common): Internal meetings, accessibility, documentation
     - **High-Risk**: Administrative decision-making, official proceedings, legal records
   - Includes decision tree for risk determination
   - OpenGateLLM-specific compliance guidance

#### **Category B: Critical Infrastructure & Specialized Sectors (Advisory Scope)**

1. **Food Safety & Supply Chain** (Annex III, Point 2)
   - Example: Food traceability systems
   - Note: ALLiaNCE does not typically incubate; guidance for other administrations

2. **Energy & Critical Infrastructure** (Annex III, Point 2)
   - Energy production, distribution, grid stability systems
   - Note: Requires specialized compliance frameworks beyond ai-kit

3. **Defense & Security Systems** (Annex III, Point 1)
   - Weapons systems, military applications
   - Note: Outside ALLiaNCE scope; specialized defense frameworks apply

### 2. Risk Assessment Workflow (New Section in Principle I)

Added mandatory 5-step risk classification process:

1. **Identify Use Case**: Map to Annex III categories using EU AI Act Compliance Checker
2. **Document Classification**: Record risk level in `spec.md` with rationale
3. **High-Risk Trigger**: Activate compliance workflow if High-Risk
4. **Compliance Validation**: Include in Constitution Check of all design artifacts
5. **Ongoing Monitoring**: Quarterly review for production systems, immediate re-assessment for scope changes

### 3. Transcription Audio Risk Assessment Decision Tree (New)

Added 3-question decision tree for context-dependent transcription systems:

1. Is transcription used to inform administrative decisions?
2. Does it feed into systems determining benefits, legal outcomes, or official records?
3. Is it used for internal collaboration, accessibility, or general documentation?

**Principle**: When in doubt, classify as High-Risk and conduct full compliance assessment.

### 4. High-Risk AI Mandatory Artifacts (New Section in Principle I)

Specified 8 required documentation categories for High-Risk AI systems:

1. **Risk Management Documentation**: Lifecycle assessment, mitigation strategies, residual risk acceptance
2. **Data Governance Plan**: Quality assurance, bias testing, representativeness validation, data provenance
3. **Technical Documentation**: Architecture, model cards, performance metrics, limitations
4. **Human Oversight Design**: Intervention mechanisms, override capabilities, training requirements
5. **Audit Trail System**: Automatic logging, retention policies, audit capabilities
6. **Instructions for Deployers**: Proper use guidance, limitations, oversight requirements
7. **Incident Response Plan**: Failure handling, bias remediation, compliance breach reporting
8. **Context Classification Document**: For context-dependent systems, controls to prevent risk migration

Each artifact includes documentation location guidance (e.g., `plan.md`, `data-model.md`, `contracts/`).

## Template Updates

### ✅ spec-template.md (COMPLETED)

Added mandatory "EU AI Act Risk Classification" section:
- Risk level determination with Annex III reference
- Context-dependent classification table for multi-use-case systems
- High-Risk compliance trigger checklist (8 mandatory artifacts)
- Scope change monitoring requirements

### ✅ plan-template.md (COMPLETED)

Updated "Constitution Check" section:
- Detailed EU AI Act sub-checklist (6 validation points)
- New "High-Risk AI Mandatory Artifacts Checklist" section
- Documentation location guidance for each artifact type
- Compliance status tracking and gap identification

### ⚠️ tasks-template.md (PENDING)

To be updated with High-Risk AI task categories:
- Risk management documentation tasks
- Data governance and bias testing tasks
- Audit trail implementation tasks
- Human oversight UI/UX tasks
- Deployer instructions documentation tasks

## Impact on Existing Projects

### Immediate Actions Required

1. **All Projects**: Review and classify AI risk level using new workflow
2. **High-Risk Projects**: Verify all 8 mandatory artifacts are planned/documented
3. **Transcription Projects**: Use decision tree to classify each use case
4. **Existing Specs**: Add "EU AI Act Risk Classification" section to `spec.md`

### Follow-Up TODOs

1. Create **OpenGateLLM Compliance Guide** documenting transcription risk classification
2. Update existing feature specs to include EU AI Act risk classification
3. Create example High-Risk AI project demonstrating mandatory artifacts
4. Develop bias testing and explainability tool templates for ai-kit
5. Create audit logging and human oversight UI pattern library

## Compliance Benefits

1. **Legal Protection**: Clear documentation of risk assessment and compliance measures
2. **Homologation Alignment**: Mandatory artifacts align with ANSSI homologation dossier requirements
3. **Traceability**: Integration with SpecKit ensures all compliance decisions are documented
4. **Actionable Guidance**: Concrete examples from ALLiaNCE incubations make compliance practical
5. **Scope Management**: Clear boundaries prevent Limited Risk systems from drifting into High-Risk territory

## Suggested Commit Message

```
docs: amend constitution to v1.10.0 (EU AI Act risk classification refinement)

- Add French Government High-Risk Use Cases with ALLiaNCE examples
- Add Risk Assessment Workflow with 5-step process
- Add Transcription Audio Risk Assessment Decision Tree
- Add High-Risk AI Mandatory Artifacts specification
- Update spec-template.md with EU AI Act Risk Classification section
- Update plan-template.md with High-Risk AI compliance checklist

Based on domain expert input on EU AI Act compliance for French Government
digital services. Provides concrete guidance for legal assistance, social
benefits, and transcription systems common in ALLiaNCE incubations.

BREAKING: All new features MUST include EU AI Act risk classification in spec.md
```

## Next Steps for Review

1. **Expert Review**: Share this summary with your EU AI Act domain expert for validation
2. **Refinement**: Gather feedback on:
   - Completeness of use case categories
   - Accuracy of risk classifications
   - Practicality of mandatory artifacts
   - Clarity of decision trees
3. **Iteration**: Update constitution based on expert feedback if needed
4. **Communication**: Share updated constitution with ALLiaNCE teams
5. **Training**: Consider workshop on new risk assessment workflow

## Questions for Expert Follow-Up

1. Are there additional High-Risk use cases in Category A we should document?
2. Is the transcription risk classification decision tree accurate and complete?
3. Are the 8 mandatory artifacts sufficient for EU AI Act compliance?
4. Should we add specific guidance for other OpenGateLLM features (RAG, vectorization)?
5. Are there specific Annex III points we should emphasize more?

---

**Constitution Version**: 1.10.0  
**Ratified**: 2025-10-11  
**Last Amended**: 2025-10-16  
**Full Constitution**: `.specify/memory/constitution.md`
