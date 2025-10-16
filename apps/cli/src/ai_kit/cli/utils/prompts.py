"""Interactive prompts using questionary."""

import re

import questionary
from questionary import ValidationError, Validator

from ai_kit.cli.core.config import CATEGORIES


class NotebookNameValidator(Validator):
    """Validator for notebook names."""

    def validate(self, document):
        """Validate notebook name."""
        text = document.text
        if not text:
            raise ValidationError(message="Notebook name cannot be empty")

        # Check for invalid characters
        if not re.match(r"^[a-zA-Z0-9_-]+$", text):
            raise ValidationError(
                message="Notebook name can only contain letters, numbers, hyphens, and underscores"
            )


class PurposeValidator(Validator):
    """Validator for purpose field."""

    def validate(self, document):
        """Validate purpose."""
        text = document.text
        if not text or len(text) < 10:
            raise ValidationError(message="Purpose must be at least 10 characters")


def prompt_category() -> str:
    """Prompt user to select a notebook category."""
    choices = []
    for key, config in CATEGORIES.items():
        label = f"{config.display_name} - {config.description}"
        choices.append(questionary.Choice(title=label, value=key))

    return questionary.select(
        "Select notebook category:",
        choices=choices,
    ).ask()


def prompt_notebook_name() -> str:
    """Prompt user for notebook name."""
    return questionary.text(
        "Enter notebook name (without .ipynb extension):",
        validate=NotebookNameValidator,
    ).ask()


def prompt_purpose() -> str:
    """Prompt user for notebook purpose."""
    return questionary.text(
        "What question does this notebook answer? (min 10 characters)",
        validate=PurposeValidator,
        multiline=False,
    ).ask()


def prompt_author(default: str | None = None) -> str:
    """Prompt user for author name."""
    return questionary.text(
        "Author name:",
        default=default or "",
    ).ask()


def prompt_confirmation(summary: dict[str, str]) -> bool:
    """Prompt user to confirm notebook creation."""
    print("\nSummary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print()

    return questionary.confirm("Create notebook?", default=True).ask()


def prompt_additional_field(field_name: str, default: str = "") -> str:
    """Prompt for additional metadata field."""
    formatted_name = field_name.replace("_", " ").title()
    return questionary.text(
        f"{formatted_name}:",
        default=default,
    ).ask()
