"""Template management utilities."""

from datetime import datetime
from pathlib import Path

import nbformat

from ai_kit.cli.core.config import CATEGORIES, get_category_dir, get_templates_dir


def load_template(category: str) -> nbformat.NotebookNode:
    """Load template notebook for a category."""
    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category}")

    config = CATEGORIES[category]
    template_path = get_templates_dir() / config.template_file

    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path, encoding="utf-8") as f:
        return nbformat.read(f, as_version=4)


def populate_metadata(
    notebook: nbformat.NotebookNode,
    category: str,
    title: str,
    purpose: str,
    author: str,
    additional_metadata: dict[str, str] | None = None,
) -> nbformat.NotebookNode:
    """Populate notebook metadata in first cell."""
    if not notebook.cells or notebook.cells[0].cell_type != "markdown":
        raise ValueError("Template must have a markdown cell as first cell")

    # Get current date
    created = datetime.now().strftime("%Y-%m-%d")

    # Build metadata section
    metadata_lines = [
        f"# {title}",
        "",
        f"**Category**: {category}",
        f"**Purpose**: {purpose}",
        f"**Author**: {author}",
        f"**Created**: {created}",
        "**Data Sources**: ",
        "- [List your data sources]",
        "",
        "**Dependencies**:",
        "- [List key dependencies]",
        "",
    ]

    # Add category-specific metadata
    if additional_metadata:
        for key, value in additional_metadata.items():
            formatted_key = key.replace("_", " ").title()
            metadata_lines.append(f"**{formatted_key}**: {value}")
        metadata_lines.append("")

    # Replace first cell content
    notebook.cells[0].source = "\n".join(metadata_lines)

    return notebook


def create_notebook_from_template(
    category: str,
    name: str,
    title: str,
    purpose: str,
    author: str,
    additional_metadata: dict[str, str] | None = None,
) -> Path:
    """Create a new notebook from template."""
    # Load template
    notebook = load_template(category)

    # Populate metadata
    notebook = populate_metadata(notebook, category, title, purpose, author, additional_metadata)

    # Determine output path
    output_dir = get_category_dir(category)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Ensure .ipynb extension
    if not name.endswith(".ipynb"):
        name = f"{name}.ipynb"

    output_path = output_dir / name

    # Check if file exists
    if output_path.exists():
        raise FileExistsError(f"Notebook already exists: {output_path}")

    # Write notebook
    with open(output_path, "w", encoding="utf-8") as f:
        nbformat.write(notebook, f)

    return output_path
