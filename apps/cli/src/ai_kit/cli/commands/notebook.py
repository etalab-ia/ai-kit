"""Notebook command group."""

import sys
from pathlib import Path

import click

from ai_kit.cli.core.config import CATEGORIES
from ai_kit.cli.core.templates import create_notebook_from_template
from ai_kit.cli.utils.git import get_git_user_name
from ai_kit.cli.utils.output import print_error, print_notebook_created, print_success
from ai_kit.cli.utils.prompts import (
    prompt_additional_field,
    prompt_author,
    prompt_category,
    prompt_confirmation,
    prompt_notebook_name,
    prompt_purpose,
)


@click.group()
def notebook():
    """Manage Jupyter notebooks."""
    pass


@notebook.command()
def create():
    """Create a new notebook from template."""
    try:
        # Prompt for category
        category = prompt_category()
        if not category:
            print_error("No category selected")
            sys.exit(1)

        # Prompt for notebook name
        name = prompt_notebook_name()
        if not name:
            print_error("No notebook name provided")
            sys.exit(1)

        # Prompt for purpose
        purpose = prompt_purpose()
        if not purpose:
            print_error("No purpose provided")
            sys.exit(1)

        # Prompt for author (with git default)
        default_author = get_git_user_name()
        author = prompt_author(default=default_author)
        if not author:
            print_error("No author provided")
            sys.exit(1)

        # Prompt for category-specific metadata
        additional_metadata = {}
        config = CATEGORIES[category]
        if config.additional_metadata:
            for field in config.additional_metadata:
                value = prompt_additional_field(field)
                if value:
                    additional_metadata[field] = value

        # Build summary
        summary = {
            "Category": category,
            "Path": f"notebooks/{category}/{name}.ipynb",
            "Purpose": purpose,
            "Author": author,
        }
        if additional_metadata:
            summary.update(additional_metadata)

        # Confirm creation
        if not prompt_confirmation(summary):
            print_error("Notebook creation cancelled")
            sys.exit(2)

        # Create notebook
        output_path = create_notebook_from_template(
            category=category,
            name=name,
            title=name.replace("-", " ").replace("_", " ").title(),
            purpose=purpose,
            author=author,
            additional_metadata=additional_metadata if additional_metadata else None,
        )

        # Print success
        print_notebook_created(output_path)

    except FileExistsError as e:
        print_error(str(e))
        sys.exit(1)
    except FileNotFoundError as e:
        print_error(str(e))
        print_error("Template files may not be created yet. Run setup first.")
        sys.exit(3)
    except KeyboardInterrupt:
        print_error("\nCancelled by user")
        sys.exit(2)
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        sys.exit(3)


@notebook.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
def validate(path: Path):
    """Validate notebook metadata."""
    from ai_kit.cli.core.validators import validate_notebook_metadata
    from ai_kit.cli.utils.output import print_validation_errors

    result = validate_notebook_metadata(path)

    if result.passed:
        print_success(f"Notebook validation passed: {path}")
    else:
        print_validation_errors(result.errors, result.warnings)
        sys.exit(1)


@notebook.command("list")
def list_notebooks():
    """List notebooks by category."""
    from ai_kit.cli.core.config import get_notebooks_dir

    notebooks_dir = get_notebooks_dir()

    if not notebooks_dir.exists():
        print_error(f"Notebooks directory not found: {notebooks_dir}")
        sys.exit(1)

    for category in CATEGORIES:
        category_dir = notebooks_dir / category
        if category_dir.exists():
            notebook_files = list(category_dir.glob("*.ipynb"))
            if notebook_files:
                print(f"\n{category.upper()}:")
                for nb in notebook_files:
                    print(f"  - {nb.name}")


@notebook.command()
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.confirmation_option(prompt="Are you sure you want to delete this notebook?")
def delete(path: Path):
    """Delete a notebook (with confirmation)."""
    try:
        path.unlink()
        print_success(f"Deleted notebook: {path}")
        print("Note: Git history preserves the notebook if you need to reference it later.")
    except Exception as e:
        print_error(f"Failed to delete notebook: {e}")
        sys.exit(1)


@notebook.command("stats")
def show_stats():
    """Show notebook statistics."""
    from ai_kit.cli.core.config import get_notebooks_dir

    notebooks_dir = get_notebooks_dir()

    if not notebooks_dir.exists():
        print_error(f"Notebooks directory not found: {notebooks_dir}")
        sys.exit(1)

    total = 0
    print("\nNotebook Statistics:\n")

    for category in CATEGORIES:
        category_dir = notebooks_dir / category
        if category_dir.exists():
            notebook_files = list(category_dir.glob("*.ipynb"))
            count = len(notebook_files)
            total += count
            print(f"  {category}: {count}")

    print(f"\nTotal: {total} notebooks")
