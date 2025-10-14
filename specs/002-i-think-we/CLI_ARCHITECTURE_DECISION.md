# Architecture Decision: Unified ai-kit CLI

**Date**: 2025-10-14  
**Status**: Accepted  
**Decision Maker**: User (Luis)  
**Phase**: Post-clarification, pre-planning update

## Decision

Implement a **unified ai-kit CLI** in `apps/cli/` with extensible command group architecture, rather than a notebook-specific CLI.

## Context

During post-clarification review, the user identified that a narrow notebook-only CLI would limit future extensibility. The ai-kit project will need CLI commands for multiple domains:
- Notebook management (current feature)
- Dataset operations (future)
- Streamlit application lifecycle (future)
- Compliance workflows (future)
- Experiment tracking (future)
- ProConnect configuration (future)

## Options Considered

### Option 1: Notebook-Specific CLI (Original)
```bash
just create-notebook
just list-notebooks
just validate-notebook
```

**Location**: `packages/notebook-tools/`  
**Scope**: Notebook operations only

**Pros**:
- Simpler initial implementation
- Focused scope for current feature

**Cons**:
- Future features would need separate CLIs
- Inconsistent command patterns across ai-kit
- No shared infrastructure (validation, prompts, git ops)
- CLI proliferation problem
- Harder to implement cross-feature workflows

### Option 2: Unified ai-kit CLI (Selected) ✅
```bash
just notebook create
just notebook list
just notebook validate
just dataset download
just streamlit run
just compliance tag
just experiment start
```

**Location**: `apps/cli/`  
**Scope**: All ai-kit operations

**Pros**:
- Single entry point for all ai-kit commands
- Consistent command patterns and UX
- Shared infrastructure (validation, prompts, git, output formatting)
- Extensible architecture for future features
- Enables cross-feature workflows
- Better discoverability (`just --list`)
- Aligns with monorepo philosophy

**Cons**:
- Slightly more complex initial setup (command routing)
- Need to design extensible architecture upfront

## Decision Rationale

**Option 2 (Unified CLI) selected** for the following reasons:

1. **Long-term Architecture**: Prevents CLI proliferation as ai-kit grows
2. **Consistent DX**: Same command patterns across all features
3. **Shared Infrastructure**: Reusable validation, prompts, git operations
4. **Extensibility**: Easy to add new command groups without refactoring
5. **Cross-Feature Workflows**: Enable commands like `just notebook create` + `just dataset download` + `just experiment start`
6. **Discoverability**: Single `just --list` shows all ai-kit capabilities
7. **Monorepo Alignment**: Centralized tooling in `apps/` directory

## Implementation

### Directory Structure

```
apps/cli/
├── pyproject.toml
├── src/
│   └── ai_kit_cli/
│       ├── __init__.py
│       ├── main.py              # Entry point, command routing
│       ├── commands/
│       │   ├── __init__.py
│       │   ├── notebook.py      # Notebook subcommands (current feature)
│       │   ├── dataset.py       # Dataset subcommands (future)
│       │   ├── streamlit.py     # Streamlit subcommands (future)
│       │   ├── compliance.py    # Compliance subcommands (future)
│       │   └── experiment.py    # Experiment subcommands (future)
│       ├── core/
│       │   ├── config.py        # CLI configuration
│       │   ├── validators.py    # Shared validation logic
│       │   └── templates.py     # Template management
│       └── utils/
│           ├── git.py           # Git operations
│           ├── prompts.py       # Interactive prompts
│           └── output.py        # Formatted output
└── tests/
    ├── test_notebook_commands.py
    ├── test_dataset_commands.py
    └── test_streamlit_commands.py
```

### Command Groups

#### Notebook Commands (Current Feature)
- `just notebook create` - Interactive notebook creation
- `just notebook list [category]` - List notebooks by category
- `just notebook validate <path>` - Manual validation
- `just notebook delete <path>` - Safe deletion with git guidance
- `just notebook migrate <path>` - Document production migration
- `just notebook stats` - Repository statistics

#### Future Command Groups
- **Dataset**: `download`, `list`, `validate`
- **Streamlit**: `run`, `deploy`, `test`
- **Compliance**: `tag`, `report`, `audit`
- **Experiment**: `start`, `log`, `compare`
- **ProConnect**: `setup`, `test`, `refresh`

### Justfile Integration

```justfile
# Unified ai-kit CLI commands

# Notebook operations
notebook *ARGS:
    uv run python -m ai_kit_cli.commands.notebook {{ARGS}}

# Future: Dataset operations
dataset *ARGS:
    uv run python -m ai_kit_cli.commands.dataset {{ARGS}}

# Future: Streamlit operations
streamlit *ARGS:
    uv run python -m ai_kit_cli.commands.streamlit {{ARGS}}
```

## Specification Updates

### Clarifications Added
- Q: Should the CLI be notebook-specific or general-purpose for all ai-kit operations?
- A: Unified ai-kit CLI in `apps/cli/` with extensible command structure

### Functional Requirements Added
- **FR-008**: Unified ai-kit CLI application with extensible command structure
- **FR-008a**: `just notebook create` command
- **FR-008b**: `just notebook list [category]` command
- **FR-008c**: `just notebook validate <path>` command
- **FR-008d**: `just notebook delete <path>` command (SHOULD)
- **FR-008e**: `just notebook migrate <path>` command (SHOULD)
- **FR-008f**: `just notebook stats` command (SHOULD)
- **FR-008g**: CLI architecture supports future command groups

### Success Criteria Added
- **SC-013**: List notebooks with metadata via `just notebook list`
- **SC-014**: Manual validation via `just notebook validate`
- **SC-015**: CLI discoverability via `just --list`

### Key Entities Updated
- **ai-kit CLI Application**: Unified CLI with command groups
- **Notebook Command Group**: Collection of notebook subcommands

### Future Considerations Added
- **Unified CLI Extensibility**: Documented anticipated command groups (dataset, streamlit, compliance, experiment, proconnect)

## Migration Impact

### From Original Plan
**Before**: `packages/notebook-tools/` with single `just create-notebook` command  
**After**: `apps/cli/` with `just notebook create` and extensible command structure

### Breaking Changes
None - this is a pre-implementation architectural decision. No existing code to migrate.

### Benefits for Implementation
1. **Cleaner Architecture**: CLI apps belong in `apps/`, not `packages/`
2. **Shared Code**: Validation, prompts, git operations reused across commands
3. **Easier Testing**: Command groups can be tested independently
4. **Future-Proof**: Adding new command groups requires no structural changes

## Risks and Mitigations

### Risk: Over-Engineering
**Mitigation**: Implement only notebook commands initially. Add other groups incrementally as features are developed.

### Risk: Complexity
**Mitigation**: Use established CLI framework (Click or Typer) for command routing and help generation.

### Risk: Maintenance Burden
**Mitigation**: Shared infrastructure reduces duplication. Each command group is independently maintainable.

## Success Metrics

1. **Discoverability**: Developers can find all ai-kit commands via `just --list`
2. **Consistency**: All command groups follow same patterns (subcommands, flags, output)
3. **Extensibility**: New command groups added without refactoring existing code
4. **Performance**: CLI startup time < 1 second
5. **DX**: Developers prefer unified CLI over separate tools

## References

- **Specification**: `specs/002-i-think-we/spec.md`
- **Checklist**: `specs/002-i-think-we/checklists/requirements.md`
- **User Feedback**: "I would like the cli to be more general than the notebooks scope, for instance just dataset download or just run streamlit-app etc... In that case we could put the cli in /apps/cli which is simple and straightforward"

## Next Steps

1. Update implementation plan (`plan.md`) to reflect unified CLI architecture
2. Update research (`research.md`) with CLI framework selection
3. Update data model (`data-model.md`) with CLI command structure
4. Update contracts (`contracts/cli-interface.md`) with all command groups
5. Update quickstart (`quickstart.md`) with unified CLI examples
6. Proceed with `/speckit.tasks` to generate implementation tasks

---

**Conclusion**: The unified ai-kit CLI architecture provides a solid foundation for current notebook management needs while enabling seamless addition of future command groups. This decision aligns with monorepo best practices, improves developer experience, and prevents technical debt from CLI proliferation.
