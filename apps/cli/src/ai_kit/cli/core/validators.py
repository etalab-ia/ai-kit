"""Validation logic for notebooks."""

import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path

import nbformat

from ai_kit.cli.core.config import CATEGORIES


@dataclass
class ValidationError:
    """Validation error details."""

    code: str
    message: str
    field: str | None = None
    suggestion: str | None = None


@dataclass
class ValidationResult:
    """Result of notebook validation."""

    notebook_path: Path
    passed: bool
    errors: list[ValidationError]
    warnings: list[ValidationError]


def extract_metadata_from_markdown(markdown_source: str) -> dict[str, str]:
    """Extract metadata from markdown cell using **Key**: value format."""
    metadata = {}

    # Match patterns like **Category**: exploratory
    pattern = r"\*\*([^*]+)\*\*:\s*(.+)"
    for match in re.finditer(pattern, markdown_source, re.MULTILINE):
        key = match.group(1).strip().lower().replace(" ", "_")
        value = match.group(2).strip()
        metadata[key] = value

    # Handle multi-line fields (Data Sources, Dependencies)
    # Look for list items after the field
    data_sources_match = re.search(
        r"\*\*Data Sources\*\*:\s*\n((?:^-\s+.+$\n?)+)", markdown_source, re.MULTILINE
    )
    if data_sources_match:
        sources = [
            line.strip("- ").strip() for line in data_sources_match.group(1).strip().split("\n")
        ]
        metadata["data_sources"] = sources
    else:
        metadata["data_sources"] = []

    dependencies_match = re.search(
        r"\*\*Dependencies\*\*:\s*\n((?:^-\s+.+$\n?)+)", markdown_source, re.MULTILINE
    )
    if dependencies_match:
        deps = [
            line.strip("- ").strip() for line in dependencies_match.group(1).strip().split("\n")
        ]
        metadata["dependencies"] = deps
    else:
        metadata["dependencies"] = []

    return metadata


def validate_notebook_metadata(notebook_path: Path) -> ValidationResult:
    """Validate notebook metadata."""
    errors = []
    warnings = []

    # Check if file exists
    if not notebook_path.exists():
        errors.append(
            ValidationError(
                code="FILE_NOT_FOUND",
                message=f"Notebook not found: {notebook_path}",
                suggestion="Check the file path",
            )
        )
        return ValidationResult(notebook_path, False, errors, warnings)

    # Load notebook
    try:
        with open(notebook_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
    except json.JSONDecodeError:
        errors.append(
            ValidationError(
                code="INVALID_JSON",
                message="Notebook is not valid JSON",
                suggestion="Check notebook file format",
            )
        )
        return ValidationResult(notebook_path, False, errors, warnings)
    except Exception as e:
        errors.append(
            ValidationError(
                code="READ_ERROR",
                message=f"Failed to read notebook: {e}",
                suggestion="Check file permissions",
            )
        )
        return ValidationResult(notebook_path, False, errors, warnings)

    # Check first cell exists and is markdown
    if not nb.cells:
        errors.append(
            ValidationError(
                code="NO_CELLS",
                message="Notebook has no cells",
                suggestion="Add a markdown cell with metadata",
            )
        )
        return ValidationResult(notebook_path, False, errors, warnings)

    first_cell = nb.cells[0]
    if first_cell.cell_type != "markdown":
        errors.append(
            ValidationError(
                code="FIRST_CELL_NOT_MARKDOWN",
                message="First cell must be markdown with metadata",
                suggestion="Add a markdown cell at the beginning with metadata",
            )
        )
        return ValidationResult(notebook_path, False, errors, warnings)

    # Extract metadata
    metadata = extract_metadata_from_markdown(first_cell.source)

    # Required fields
    required_fields = ["category", "purpose", "author", "created"]

    for field in required_fields:
        if field not in metadata or not metadata[field]:
            errors.append(
                ValidationError(
                    code="MISSING_METADATA",
                    message=f"Missing required field: '{field}'",
                    field=field,
                    suggestion=f"Add **{field.replace('_', ' ').title()}**: value to first cell",
                )
            )

    # Validate category matches directory
    if "category" in metadata:
        category = metadata["category"]
        if category not in CATEGORIES:
            errors.append(
                ValidationError(
                    code="INVALID_CATEGORY",
                    message=f"Invalid category: '{category}'",
                    field="category",
                    suggestion=f"Use one of: {', '.join(CATEGORIES.keys())}",
                )
            )
        else:
            # Check if notebook is in correct directory
            expected_dir = category
            actual_dir = notebook_path.parent.name
            if actual_dir != expected_dir:
                errors.append(
                    ValidationError(
                        code="CATEGORY_MISMATCH",
                        message=(
                            f"Category mismatch: metadata says '{category}' "
                            f"but file is in '{actual_dir}/'"
                        ),
                        field="category",
                        suggestion=(
                            f"Move notebook to notebooks/{category}/ or update category metadata"
                        ),
                    ),
                )

    # Validate purpose length
    if "purpose" in metadata and len(metadata["purpose"]) < 10:
        errors.append(
            ValidationError(
                code="PURPOSE_TOO_SHORT",
                message="Purpose must be at least 10 characters",
                field="purpose",
                suggestion="Provide a more detailed description of the notebook's purpose",
            )
        )

    # Validate created date format (basic check)
    if "created" in metadata:
        created = metadata["created"]
        if not re.match(r"\d{4}-\d{2}-\d{2}", created):
            errors.append(
                ValidationError(
                    code="INVALID_DATE",
                    message=f"Invalid date format: '{created}'",
                    field="created",
                    suggestion="Use ISO 8601 format: YYYY-MM-DD",
                )
            )

    passed = len(errors) == 0
    return ValidationResult(notebook_path, passed, errors, warnings)


def check_notebook_size(
    notebook_path: Path, warn_mb: float = 5.0, block_mb: float = 10.0
) -> ValidationResult:
    """Check notebook file size."""
    errors = []
    warnings = []

    if not notebook_path.exists():
        errors.append(
            ValidationError(
                code="FILE_NOT_FOUND",
                message=f"Notebook not found: {notebook_path}",
            )
        )
        return ValidationResult(notebook_path, False, errors, warnings)

    size_bytes = notebook_path.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    if size_mb >= block_mb:
        errors.append(
            ValidationError(
                code="SIZE_EXCEEDED",
                message=f"Notebook size is {size_mb:.1f} MB (exceeds {block_mb} MB limit)",
                suggestion=(
                    "Move data to external files, remove embedded datasets, or use data references"
                ),
            )
        )
    elif size_mb >= warn_mb:
        warnings.append(
            ValidationError(
                code="SIZE_WARNING",
                message=(f"Notebook size is {size_mb:.1f} MB (warning threshold: {warn_mb} MB)"),
                suggestion="Consider externalizing data to prevent repository bloat",
            )
        )

    passed = len(errors) == 0
    return ValidationResult(notebook_path, passed, errors, warnings)


def main():
    """CLI entry point for validators."""
    if len(sys.argv) < 2:
        print(
            "Usage: python -m ai_kit.cli.core.validators "
            "[--check-metadata|--check-size] <notebook_path>"
        )
        sys.exit(1)

    mode = "metadata"
    notebook_path = sys.argv[1]

    if sys.argv[1] in ["--check-metadata", "--check-size"]:
        mode = sys.argv[1].replace("--check-", "")
        notebook_path = sys.argv[2] if len(sys.argv) > 2 else None

    if not notebook_path:
        print("Error: No notebook path provided")
        sys.exit(1)

    # Resolve path - handle both absolute and relative paths
    # When run via pre-commit with uv run --directory apps/cli,
    # we need to resolve relative paths from the git root
    path = Path(notebook_path)

    if not path.is_absolute():
        # Try to find git root by looking for .git directory
        current = Path.cwd()
        git_root = None

        # Walk up the directory tree to find .git
        for parent in [current] + list(current.parents):
            if (parent / ".git").exists():
                git_root = parent
                break

        if git_root:
            # Resolve path relative to git root
            path = git_root / path
        # If not in a git repo, use path as-is (will fail if doesn't exist)

    if mode == "metadata":
        result = validate_notebook_metadata(path)
    elif mode == "size":
        result = check_notebook_size(path)
    else:
        print(f"Unknown mode: {mode}")
        sys.exit(1)

    # Print errors
    if result.errors:
        print(f"\nNotebook validation failed: {path}\n")
        print("Errors:")
        for error in result.errors:
            print(f"  ✗ {error.message}")
            if error.suggestion:
                print(f"    → {error.suggestion}")
        print()

    # Print warnings
    if result.warnings:
        print(f"\n⚠ Warnings for: {path}\n")
        for warning in result.warnings:
            print(f"  ⚠ {warning.message}")
            if warning.suggestion:
                print(f"    → {warning.suggestion}")
        print()

    # Exit with appropriate code
    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
