"""Configuration management for notebook CLI."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal


@dataclass
class CategoryConfig:
    """Configuration for a notebook category."""

    name: str
    display_name: str
    description: str
    governance_level: Literal["low", "medium", "high"]
    speckit_required: bool
    retention_policy: Literal["delete_after_migration", "retain", "retain_and_tag"]
    template_file: str
    additional_metadata: list[str]


# Category definitions
CATEGORIES: dict[str, CategoryConfig] = {
    "exploratory": CategoryConfig(
        name="exploratory",
        display_name="Exploratory",
        description="Rapid experimentation and hypothesis testing",
        governance_level="low",
        speckit_required=False,
        retention_policy="delete_after_migration",
        template_file="exploratory-template.ipynb",
        additional_metadata=[],
    ),
    "tutorials": CategoryConfig(
        name="tutorials",
        display_name="Tutorials",
        description="Learning materials and examples",
        governance_level="medium",
        speckit_required=True,
        retention_policy="retain",
        template_file="tutorial-template.ipynb",
        additional_metadata=[],
    ),
    "evaluations": CategoryConfig(
        name="evaluations",
        display_name="Evaluations",
        description="Model performance assessment and benchmarking",
        governance_level="medium",
        speckit_required=True,
        retention_policy="retain_and_tag",
        template_file="evaluation-template.ipynb",
        additional_metadata=["model_version", "evaluation_metrics", "baseline_comparison"],
    ),
    "compliance": CategoryConfig(
        name="compliance",
        display_name="Compliance",
        description="EU AI Act and regulatory documentation",
        governance_level="high",
        speckit_required=True,
        retention_policy="retain_and_tag",
        template_file="compliance-template.ipynb",
        additional_metadata=["risk_level", "regulatory_framework", "review_date"],
    ),
    "reporting": CategoryConfig(
        name="reporting",
        display_name="Reporting",
        description="Parameterized stakeholder reports",
        governance_level="medium",
        speckit_required=False,
        retention_policy="retain",
        template_file="reporting-template.ipynb",
        additional_metadata=["parameters", "schedule", "recipients"],
    ),
}


def get_notebooks_dir() -> Path:
    """Get the notebooks directory path."""
    # Find repository root by looking for pyproject.toml with workspace config
    current = Path.cwd()

    # Try current directory first
    if (current / "notebooks").exists():
        return current / "notebooks"

    # Walk up to find repository root
    for parent in [current] + list(current.parents):
        if (parent / "pyproject.toml").exists() and (parent / "notebooks").exists():
            return parent / "notebooks"

    # Fallback to current directory
    return current / "notebooks"


def get_templates_dir() -> Path:
    """Get the templates directory path."""
    return get_notebooks_dir() / "templates"


def get_category_dir(category: str) -> Path:
    """Get the directory path for a specific category."""
    return get_notebooks_dir() / category
