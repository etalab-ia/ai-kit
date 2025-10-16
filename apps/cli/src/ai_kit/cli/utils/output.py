"""Formatted output using rich."""

from pathlib import Path

from rich.console import Console

console = Console()


def print_success(message: str):
    """Print success message."""
    console.print(f"✓ {message}", style="green")


def print_error(message: str):
    """Print error message."""
    console.print(f"✗ {message}", style="red")


def print_warning(message: str):
    """Print warning message."""
    console.print(f"⚠ {message}", style="yellow")


def print_info(message: str):
    """Print info message."""
    console.print(message, style="blue")


def print_notebook_created(notebook_path: Path):
    """Print success message for notebook creation."""
    print_success(f"Created notebook: {notebook_path}")
    print_success("Metadata populated")
    print_success("Ready to edit")

    console.print("\nNext steps:", style="bold")
    console.print(f"1. Open notebook: jupyter lab {notebook_path}")
    console.print("2. Add your code and analysis")
    console.print(f"3. Commit with: git add {notebook_path} && git commit")


def print_validation_errors(errors: list, warnings: list):
    """Print validation errors and warnings."""
    if errors:
        console.print("\nErrors:", style="bold red")
        for error in errors:
            print_error(error.message)
            if error.suggestion:
                console.print(f"  → {error.suggestion}", style="dim")

    if warnings:
        console.print("\nWarnings:", style="bold yellow")
        for warning in warnings:
            print_warning(warning.message)
            if warning.suggestion:
                console.print(f"  → {warning.suggestion}", style="dim")
