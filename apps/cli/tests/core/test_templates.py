"""Tests for template management."""

import json
from datetime import datetime

import nbformat
import pytest

from ai_kit.cli.core.templates import (
    create_notebook_from_template,
    load_template,
    populate_metadata,
)


class TestLoadTemplate:
    """Test template loading functionality."""

    @pytest.fixture
    def mock_templates_dir(self, tmp_path, monkeypatch):
        """Create a mock templates directory with test templates."""
        # Create repository structure
        notebooks_dir = tmp_path / "notebooks"
        templates_dir = notebooks_dir / "templates"
        templates_dir.mkdir(parents=True)
        (tmp_path / "pyproject.toml").touch()

        # Create a simple test template
        template = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": "# Template Notebook\n\n**Category**: {category}\n",
                },
                {"cell_type": "code", "metadata": {}, "source": "# Code cell\n"},
            ],
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                }
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }

        template_path = templates_dir / "exploratory-template.ipynb"
        with open(template_path, "w") as f:
            json.dump(template, f)

        # Change to repository root
        monkeypatch.chdir(tmp_path)

        return templates_dir

    def test_load_existing_template(self, mock_templates_dir):
        """Test loading an existing template."""
        notebook = load_template("exploratory")

        assert isinstance(notebook, nbformat.NotebookNode)
        assert len(notebook.cells) == 2
        assert notebook.cells[0].cell_type == "markdown"
        assert notebook.cells[1].cell_type == "code"

    def test_load_invalid_category(self, mock_templates_dir):
        """Test loading template with invalid category."""
        with pytest.raises(ValueError, match="Invalid category"):
            load_template("invalid_category")

    def test_load_missing_template(self, mock_templates_dir):
        """Test loading template when file doesn't exist."""
        # Remove the template file
        template_path = mock_templates_dir / "exploratory-template.ipynb"
        template_path.unlink()

        with pytest.raises(FileNotFoundError, match="Template not found"):
            load_template("exploratory")


class TestPopulateMetadata:
    """Test metadata population in templates."""

    @pytest.fixture
    def base_notebook(self):
        """Create a base notebook for testing."""
        return nbformat.v4.new_notebook(
            cells=[
                nbformat.v4.new_markdown_cell(
                    "# {title}\n\n**Category**: {category}\n**Purpose**: {purpose}\n"
                ),
                nbformat.v4.new_code_cell("# Code here"),
            ]
        )

    def test_populate_basic_metadata(self, base_notebook):
        """Test populating basic metadata fields."""
        result = populate_metadata(
            notebook=base_notebook,
            category="exploratory",
            title="Test Notebook",
            purpose="Testing metadata population",
            author="Test User",
        )

        first_cell = result.cells[0].source
        assert "# Test Notebook" in first_cell
        assert "**Category**: exploratory" in first_cell
        assert "**Purpose**: Testing metadata population" in first_cell
        assert "**Author**: Test User" in first_cell
        assert "**Created**:" in first_cell

    def test_populate_with_additional_metadata(self, base_notebook):
        """Test populating with additional metadata fields."""
        additional = {"model_version": "v1.0", "baseline_comparison": "previous-model"}

        result = populate_metadata(
            notebook=base_notebook,
            category="evaluations",
            title="Model Evaluation",
            purpose="Evaluate model performance",
            author="Test User",
            additional_metadata=additional,
        )

        first_cell = result.cells[0].source
        assert "**Model Version**: v1.0" in first_cell
        assert "**Baseline Comparison**: previous-model" in first_cell

    def test_populate_creates_valid_date(self, base_notebook):
        """Test that created date is in valid ISO 8601 format."""
        result = populate_metadata(
            notebook=base_notebook,
            category="exploratory",
            title="Test",
            purpose="Test purpose",
            author="Test User",
        )

        first_cell = result.cells[0].source
        # Extract the date line
        for line in first_cell.split("\n"):
            if line.startswith("**Created**:"):
                date_str = line.split(": ")[1]
                # Should be YYYY-MM-DD format
                datetime.strptime(date_str, "%Y-%m-%d")
                break
        else:
            pytest.fail("Created date not found in metadata")

    def test_populate_includes_data_sources_and_dependencies(self, base_notebook):
        """Test that data sources and dependencies sections are included."""
        result = populate_metadata(
            notebook=base_notebook,
            category="exploratory",
            title="Test",
            purpose="Test purpose",
            author="Test User",
        )

        first_cell = result.cells[0].source
        assert "**Data Sources**:" in first_cell
        assert "**Dependencies**:" in first_cell

    def test_populate_requires_markdown_first_cell(self):
        """Test that populate_metadata requires first cell to be markdown."""
        # Create notebook with code cell first
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell("# Code first")])

        with pytest.raises(ValueError, match="must have a markdown cell as first cell"):
            populate_metadata(
                notebook=notebook,
                category="exploratory",
                title="Test",
                purpose="Test",
                author="Test",
            )

    def test_populate_requires_at_least_one_cell(self):
        """Test that populate_metadata requires at least one cell."""
        notebook = nbformat.v4.new_notebook(cells=[])

        with pytest.raises(ValueError, match="must have a markdown cell as first cell"):
            populate_metadata(
                notebook=notebook,
                category="exploratory",
                title="Test",
                purpose="Test",
                author="Test",
            )


class TestCreateNotebookFromTemplate:
    """Test end-to-end notebook creation from template."""

    @pytest.fixture
    def setup_templates(self, tmp_path, monkeypatch):
        """Set up complete template directory structure."""
        # Create repository structure
        notebooks_dir = tmp_path / "notebooks"
        templates_dir = notebooks_dir / "templates"
        templates_dir.mkdir(parents=True)
        (tmp_path / "pyproject.toml").touch()

        # Create templates for all categories with correct filenames
        template_files = {
            "exploratory": "exploratory-template.ipynb",
            "tutorials": "tutorial-template.ipynb",
            "evaluations": "evaluation-template.ipynb",
            "compliance": "compliance-template.ipynb",
            "reporting": "reporting-template.ipynb",
        }

        for category, filename in template_files.items():
            template = nbformat.v4.new_notebook(
                cells=[
                    nbformat.v4.new_markdown_cell(f"# Template\n\n**Category**: {category}\n"),
                    nbformat.v4.new_code_cell("# Code cell"),
                ]
            )
            template_path = templates_dir / filename
            with open(template_path, "w") as f:
                nbformat.write(template, f)

        # Create category directories
        for category in template_files:
            (notebooks_dir / category).mkdir()

        monkeypatch.chdir(tmp_path)

        return tmp_path

    def test_create_basic_notebook(self, setup_templates):
        """Test creating a basic notebook from template."""
        output_path = create_notebook_from_template(
            category="exploratory",
            name="test-notebook",
            title="Test Notebook",
            purpose="Testing notebook creation",
            author="Test User",
        )

        assert output_path.exists()
        assert output_path.name == "test-notebook.ipynb"
        assert output_path.parent.name == "exploratory"

        # Verify notebook content
        with open(output_path) as f:
            notebook = nbformat.read(f, as_version=4)

        assert len(notebook.cells) >= 1
        first_cell = notebook.cells[0].source
        assert "# Test Notebook" in first_cell
        assert "**Category**: exploratory" in first_cell
        assert "**Purpose**: Testing notebook creation" in first_cell
        assert "**Author**: Test User" in first_cell

    def test_create_notebook_adds_ipynb_extension(self, setup_templates):
        """Test that .ipynb extension is added if missing."""
        output_path = create_notebook_from_template(
            category="exploratory",
            name="test-without-extension",
            title="Test",
            purpose="Testing extension handling",
            author="Test User",
        )

        assert output_path.name == "test-without-extension.ipynb"

    def test_create_notebook_preserves_ipynb_extension(self, setup_templates):
        """Test that existing .ipynb extension is preserved."""
        output_path = create_notebook_from_template(
            category="exploratory",
            name="test-with-extension.ipynb",
            title="Test",
            purpose="Testing extension handling",
            author="Test User",
        )

        assert output_path.name == "test-with-extension.ipynb"
        # Should not have double extension
        assert not output_path.name.endswith(".ipynb.ipynb")

    def test_create_notebook_with_additional_metadata(self, setup_templates):
        """Test creating notebook with additional metadata."""
        output_path = create_notebook_from_template(
            category="evaluations",
            name="model-eval",
            title="Model Evaluation",
            purpose="Evaluate model performance",
            author="Test User",
            additional_metadata={
                "model_version": "v1.0",
                "evaluation_metrics": "accuracy, F1",
                "baseline_comparison": "previous-model",
            },
        )

        with open(output_path) as f:
            notebook = nbformat.read(f, as_version=4)

        first_cell = notebook.cells[0].source
        assert "**Model Version**: v1.0" in first_cell
        assert "**Evaluation Metrics**: accuracy, F1" in first_cell
        assert "**Baseline Comparison**: previous-model" in first_cell

    def test_create_notebook_fails_if_exists(self, setup_templates):
        """Test that creation fails if notebook already exists."""
        # Create first notebook
        create_notebook_from_template(
            category="exploratory",
            name="duplicate-test",
            title="Test",
            purpose="Testing duplicate handling",
            author="Test User",
        )

        # Try to create again with same name
        with pytest.raises(FileExistsError, match="already exists"):
            create_notebook_from_template(
                category="exploratory",
                name="duplicate-test",
                title="Test",
                purpose="Testing duplicate handling",
                author="Test User",
            )

    def test_create_notebook_creates_directory_if_missing(self, setup_templates, tmp_path):
        """Test that category directory is created if it doesn't exist."""
        # Remove the exploratory directory
        exploratory_dir = tmp_path / "notebooks" / "exploratory"
        for file in exploratory_dir.iterdir():
            file.unlink()
        exploratory_dir.rmdir()

        # Should create directory and notebook
        output_path = create_notebook_from_template(
            category="exploratory",
            name="test-new-dir",
            title="Test",
            purpose="Testing directory creation",
            author="Test User",
        )

        assert output_path.exists()
        assert output_path.parent.exists()
        assert output_path.parent.name == "exploratory"

    def test_create_all_category_templates(self, setup_templates):
        """Test creating notebooks from all category templates."""
        categories = ["exploratory", "tutorials", "evaluations", "compliance", "reporting"]

        for category in categories:
            output_path = create_notebook_from_template(
                category=category,
                name=f"test-{category}",
                title=f"Test {category.title()}",
                purpose=f"Testing {category} template",
                author="Test User",
            )

            assert output_path.exists()
            assert output_path.parent.name == category

            # Verify basic structure
            with open(output_path) as f:
                notebook = nbformat.read(f, as_version=4)

            assert len(notebook.cells) >= 1
            assert notebook.cells[0].cell_type == "markdown"
            assert f"**Category**: {category}" in notebook.cells[0].source

    def test_create_notebook_is_valid_json(self, setup_templates):
        """Test that created notebook is valid JSON."""
        output_path = create_notebook_from_template(
            category="exploratory",
            name="test-json",
            title="Test",
            purpose="Testing JSON validity",
            author="Test User",
        )

        # Should be able to parse as JSON
        with open(output_path) as f:
            data = json.load(f)

        assert "cells" in data
        assert "metadata" in data
        assert "nbformat" in data

    def test_create_notebook_is_valid_nbformat(self, setup_templates):
        """Test that created notebook is valid nbformat."""
        output_path = create_notebook_from_template(
            category="exploratory",
            name="test-nbformat",
            title="Test",
            purpose="Testing nbformat validity",
            author="Test User",
        )

        # Should be able to read with nbformat
        with open(output_path) as f:
            notebook = nbformat.read(f, as_version=4)

        # Validate notebook structure
        nbformat.validate(notebook)
