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


@notebook.command()
@click.argument("input_notebook", type=click.Path(exists=True, path_type=Path))
@click.argument("output_notebook", type=click.Path(path_type=Path))
@click.option("-p", "--parameter", multiple=True, help="Parameter in key=value format")
@click.option("--kernel", default=None, help="Kernel name (default: python3)")
def run(input_notebook: Path, output_notebook: Path, parameter: tuple, kernel: str):
    """Run notebook with papermill (parameterized execution).

    Example:
        just notebook run input.ipynb output.ipynb -p start_date=2024-01-01
    """
    try:
        import papermill as pm
    except ImportError:
        print_error("papermill is not installed. Install with: uv add ipykernel papermill")
        sys.exit(1)

    # Parse parameters
    params = {}
    for param in parameter:
        if "=" not in param:
            print_error(f"Invalid parameter format: {param}. Use key=value")
            sys.exit(1)
        key, value = param.split("=", 1)
        # Try to parse as number or boolean
        if value.lower() == "true":
            params[key] = True
        elif value.lower() == "false":
            params[key] = False
        elif value.isdigit():
            params[key] = int(value)
        else:
            try:
                params[key] = float(value)
            except ValueError:
                params[key] = value

    print(f"Executing notebook: {input_notebook}")
    if params:
        print(f"Parameters: {params}")

    try:
        pm.execute_notebook(
            str(input_notebook),
            str(output_notebook),
            parameters=params,
            kernel_name=kernel,
        )
        print_success(f"Notebook executed successfully: {output_notebook}")
        print("\nNext steps:")
        print(f"  - Review output: jupyter notebook {output_notebook}")
        print(f"  - Convert to report: just notebook convert {output_notebook} html")
    except Exception as e:
        print_error(f"Failed to execute notebook: {e}")
        sys.exit(1)


@notebook.command()
@click.argument("input_notebook", type=click.Path(exists=True, path_type=Path))
@click.argument("format", type=click.Choice(["html", "pdf", "markdown", "script", "slides"]))
@click.option("-o", "--output", type=click.Path(path_type=Path), help="Output file path")
def convert(input_notebook: Path, format: str, output: Path):
    """Convert notebook to another format with nbconvert.

    Formats:
        html      - HTML report (default)
        pdf       - PDF report (requires pandoc)
        markdown  - Markdown document
        script    - Python script (.py)
        slides    - HTML slides (reveal.js)

    Example:
        just notebook convert output.ipynb html
        just notebook convert output.ipynb pdf -o report.pdf
    """
    try:
        from nbconvert import (
            HTMLExporter,
            MarkdownExporter,
            PDFExporter,
            PythonExporter,
            SlidesExporter,
        )
    except ImportError:
        print_error("nbconvert is not installed. Install with: uv add nbconvert")
        sys.exit(1)

    # Map format to exporter
    exporters = {
        "html": HTMLExporter,
        "pdf": PDFExporter,
        "markdown": MarkdownExporter,
        "script": PythonExporter,
        "slides": SlidesExporter,
    }

    exporter_class = exporters[format]
    exporter = exporter_class()

    print(f"Converting notebook to {format}: {input_notebook}")

    try:
        # Read notebook
        with open(input_notebook) as f:
            import nbformat

            notebook = nbformat.read(f, as_version=4)

        # Convert
        (body, resources) = exporter.from_notebook_node(notebook)

        # Determine output path
        if output:
            output_path = output
        else:
            # Default output path
            extensions = {
                "html": ".html",
                "pdf": ".pdf",
                "markdown": ".md",
                "script": ".py",
                "slides": ".slides.html",
            }
            output_path = input_notebook.with_suffix(extensions[format])

        # Write output
        with open(output_path, "w" if format != "pdf" else "wb") as f:
            if format == "pdf":
                f.write(body)
            else:
                f.write(body)

        print_success(f"Converted to {format}: {output_path}")

        # Format-specific tips
        if format == "html":
            print(f"\nOpen in browser: open {output_path}")
        elif format == "pdf":
            print("\nNote: PDF conversion requires pandoc and LaTeX")
        elif format == "script":
            print(f"\nRun script: python {output_path}")

    except Exception as e:
        print_error(f"Failed to convert notebook: {e}")
        if format == "pdf":
            print("\nPDF conversion requires:")
            print("  - pandoc: brew install pandoc")
            print("  - LaTeX: brew install --cask mactex")
        sys.exit(1)


@notebook.command()
@click.argument("notebook_path", type=click.Path(exists=True, path_type=Path))
@click.option("--destination", prompt="Destination package/app", help="Where code was migrated to")
@click.option("--rationale", prompt="Migration rationale", help="Why this migration was needed")
@click.option(
    "--delete",
    is_flag=True,
    help="Delete notebook after documenting migration (exploratory only)",
)
def migrate(notebook_path: Path, destination: str, rationale: str, delete: bool):
    """Document notebook-to-production migration.

    This command helps track when notebook insights are migrated to production code.
    It captures the git commit SHA and creates a migration record.

    Example:
        just notebook migrate notebooks/exploratory/experiment.ipynb \\
          --destination packages/my-feature \\
          --rationale "Validated approach, ready for production"
    """
    from ai_kit.cli.core.config import CATEGORIES, get_notebooks_dir
    from ai_kit.cli.utils.git import get_current_commit_sha, get_file_last_commit_sha

    # Validate notebook exists and get category
    if not notebook_path.exists():
        print_error(f"Notebook not found: {notebook_path}")
        sys.exit(1)

    # Determine category from path
    notebooks_dir = get_notebooks_dir()
    try:
        relative_path = notebook_path.relative_to(notebooks_dir)
        category = relative_path.parts[0]
    except (ValueError, IndexError):
        print_error(f"Notebook must be in notebooks/ directory: {notebook_path}")
        sys.exit(1)

    if category not in CATEGORIES:
        print_error(f"Invalid category: {category}")
        sys.exit(1)

    # Get git information
    try:
        current_sha = get_current_commit_sha()
        file_sha = get_file_last_commit_sha(notebook_path)
    except Exception as e:
        print_error(f"Failed to get git information: {e}")
        print("Make sure the notebook is committed to git.")
        sys.exit(1)

    # Generate migration record
    from datetime import datetime

    migration_date = datetime.now().strftime("%Y-%m-%d")
    migration_record = f"""# Migration Record: {notebook_path.name}

**Date**: {migration_date}
**Source Notebook**: `{notebook_path.relative_to(Path.cwd())}`
**Category**: {category}
**Destination**: `{destination}`

## Git References

- **Notebook Last Commit**: `{file_sha}`
- **Migration Commit**: `{current_sha}`

## Rationale

{rationale}

## Verification

To review the original notebook:
```bash
git show {file_sha}:{notebook_path.relative_to(Path.cwd())}
```

## Next Steps

- [ ] Code migrated to `{destination}`
- [ ] Tests added for migrated functionality
- [ ] Documentation updated
- [ ] Original notebook {"deleted" if delete else "retained"} (git history preserves it)
"""

    # Create migration records directory
    migration_dir = Path("docs/migrations")
    migration_dir.mkdir(parents=True, exist_ok=True)

    # Write migration record
    record_filename = f"{migration_date}-{notebook_path.stem}.md"
    record_path = migration_dir / record_filename

    with open(record_path, "w") as f:
        f.write(migration_record)

    print_success(f"Migration record created: {record_path}")
    print("\nGit references:")
    print(f"  Notebook commit: {file_sha}")
    print(f"  Current commit: {current_sha}")

    # Handle deletion for exploratory notebooks
    if delete:
        if category != "exploratory":
            print_error(
                f"\nCannot delete {category} notebooks. "
                "Only exploratory notebooks should be deleted after migration."
            )
            print(f"\n{CATEGORIES[category].display_name} notebooks must be retained for:")
            if category == "compliance":
                print("  - Regulatory audit trail")
                print("  - EU AI Act documentation")
            elif category == "evaluations":
                print("  - Model performance history")
                print("  - Baseline comparisons")
            elif category == "tutorials":
                print("  - Learning materials")
                print("  - Documentation reference")
            elif category == "reporting":
                print("  - Recurring report generation")
            sys.exit(1)

        # Confirm deletion
        if click.confirm(
            f"\n⚠️  Delete {notebook_path.name}? (git history will preserve it)",
            default=False,
        ):
            notebook_path.unlink()
            print_success(f"Deleted notebook: {notebook_path}")
            print("\nNext steps:")
            print(f"  1. Review migration record: {record_path}")
            print(f"  2. Commit changes: git add {record_path}")
            print(f"  3. Commit deletion: git rm {notebook_path}")
            print(f"  4. Reference in spec: Link to {record_path} in feature spec")
        else:
            print("\nNotebook retained. Delete manually when ready:")
            print(f"  git rm {notebook_path}")
    else:
        print("\nNext steps:")
        print(f"  1. Review migration record: {record_path}")
        print(f"  2. Commit record: git add {record_path} && git commit")
        print(f"  3. Reference in spec: Link to {record_path} in feature spec")

        if category == "exploratory":
            print("\nNote: Exploratory notebooks can be deleted after migration:")
            print(f"  just notebook migrate {notebook_path} --delete")


@notebook.command()
@click.argument("notebook_path", type=click.Path(exists=True, path_type=Path))
@click.option("--identifier", prompt="Tag identifier", help="Unique identifier for this tag")
@click.option("--message", prompt="Tag message", help="Description of what this tag represents")
@click.option("--push", is_flag=True, help="Push tag to remote after creation")
def tag(notebook_path: Path, identifier: str, message: str, push: bool):
    """Create git tag for compliance/evaluation notebooks.

    Tags follow the format: {category}/{identifier}-{date}

    This is typically used by compliance officers to mark notebooks
    for regulatory audit trails.

    Example:
        just notebook tag notebooks/compliance/model-bias-assessment.ipynb \\
          --identifier model-v1.0-audit \\
          --message "Compliance audit approved by Jane Doe"
    """
    from datetime import datetime

    from ai_kit.cli.core.config import CATEGORIES, get_notebooks_dir
    from ai_kit.cli.utils.git import create_git_tag

    # Validate notebook exists and get category
    if not notebook_path.exists():
        print_error(f"Notebook not found: {notebook_path}")
        sys.exit(1)

    # Determine category from path
    notebooks_dir = get_notebooks_dir()
    try:
        relative_path = notebook_path.relative_to(notebooks_dir)
        category = relative_path.parts[0]
    except (ValueError, IndexError):
        print_error(f"Notebook must be in notebooks/ directory: {notebook_path}")
        sys.exit(1)

    if category not in CATEGORIES:
        print_error(f"Invalid category: {category}")
        sys.exit(1)

    # Validate category is appropriate for tagging
    if category == "exploratory":
        print_error(
            "\nExploratory notebooks should not be tagged. "
            "They are temporary and should be deleted after migration."
        )
        print("\nFor audit trails, use:")
        print("  - compliance: Regulatory documentation")
        print("  - evaluations: Model performance assessments")
        sys.exit(1)

    # Generate tag name
    date_str = datetime.now().strftime("%Y-%m-%d")
    tag_name = f"{category}/{identifier}-{date_str}"

    # Validate tag name format
    if not _validate_tag_name(tag_name):
        print_error(f"Invalid tag name: {tag_name}")
        print("\nTag name must:")
        print("  - Start with category (compliance, evaluations, etc.)")
        print("  - Contain only alphanumeric, hyphens, and slashes")
        print("  - End with date in YYYY-MM-DD format")
        sys.exit(1)

    # Create tag
    print(f"Creating tag: {tag_name}")
    print(f"Message: {message}")

    if create_git_tag(tag_name, message):
        print_success(f"Tag created: {tag_name}")

        if push:
            import subprocess

            try:
                subprocess.run(
                    ["git", "push", "origin", tag_name],
                    check=True,
                    capture_output=True,
                )
                print_success(f"Tag pushed to remote: {tag_name}")
            except subprocess.CalledProcessError as e:
                print_error(f"Failed to push tag: {e}")
                print(f"\nPush manually with: git push origin {tag_name}")
                sys.exit(1)
        else:
            print("\nTo push tag to remote:")
            print(f"  git push origin {tag_name}")

        print("\nTag details:")
        print(f"  Category: {category}")
        print(f"  Identifier: {identifier}")
        print(f"  Date: {date_str}")
        print(f"  Notebook: {notebook_path.relative_to(Path.cwd())}")

        print("\nDiscover tags:")
        print(f"  git tag --list '{category}/*'")
        print("  just notebook tags")
    else:
        print_error(f"Failed to create tag: {tag_name}")
        print("\nPossible reasons:")
        print("  - Tag already exists")
        print("  - Not in a git repository")
        print("  - Uncommitted changes")
        sys.exit(1)


@notebook.command("tags")
@click.option(
    "--category",
    type=click.Choice(["compliance", "evaluations", "tutorials", "reporting"]),
)
def list_tags(category: str):
    """List git tags for notebooks.

    Example:
        just notebook tags
        just notebook tags --category compliance
    """
    from ai_kit.cli.utils.git import list_git_tags

    pattern = f"{category}/*" if category else "*/20*"  # Match date pattern

    tags = list_git_tags(pattern)

    if not tags:
        if category:
            print(f"No tags found for category: {category}")
        else:
            print("No notebook tags found")
        print("\nCreate a tag with:")
        print("  just notebook tag <notebook-path>")
        return

    print(f"\nNotebook Tags{f' ({category})' if category else ''}:\n")

    # Group by category
    from collections import defaultdict

    tags_by_category = defaultdict(list)
    for tag in tags:
        if "/" in tag:
            cat = tag.split("/")[0]
            tags_by_category[cat].append(tag)

    for cat in sorted(tags_by_category.keys()):
        print(f"  {cat}:")
        for tag in sorted(tags_by_category[cat]):
            print(f"    - {tag}")

    print(f"\nTotal: {len(tags)} tags")


def _validate_tag_name(tag_name: str) -> bool:
    """Validate tag name format: category/identifier-YYYY-MM-DD."""
    import re

    pattern = r"^[a-z]+/[a-z0-9-]+-\d{4}-\d{2}-\d{2}$"
    return bool(re.match(pattern, tag_name))
