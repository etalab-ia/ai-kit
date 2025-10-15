"""Integration tests for notebook commands."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import nbformat
import pytest
from click.testing import CliRunner

from ai_kit.cli.main import cli


class TestNotebookCreateCommand:
    """Test notebook create command."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def mock_environment(self, tmp_path, monkeypatch):
        """Set up mock environment for testing."""
        # Create repository structure
        notebooks_dir = tmp_path / "notebooks"
        templates_dir = notebooks_dir / "templates"
        templates_dir.mkdir(parents=True)
        (tmp_path / "pyproject.toml").touch()

        # Create templates
        for category in ["exploratory", "tutorials", "evaluations", "compliance", "reporting"]:
            template = nbformat.v4.new_notebook(
                cells=[
                    nbformat.v4.new_markdown_cell("# Template\n\n**Category**: {category}\n"),
                    nbformat.v4.new_code_cell("# Code cell"),
                ]
            )
            filename = f"{category}-template.ipynb" if category != "tutorials" else "tutorial-template.ipynb"
            template_path = templates_dir / filename
            with open(template_path, "w") as f:
                nbformat.write(template, f)

            # Create category directory
            (notebooks_dir / category).mkdir()

        monkeypatch.chdir(tmp_path)
        return tmp_path

    @patch("ai_kit.cli.commands.notebook.prompt_category")
    @patch("ai_kit.cli.commands.notebook.prompt_notebook_name")
    @patch("ai_kit.cli.commands.notebook.prompt_purpose")
    @patch("ai_kit.cli.commands.notebook.prompt_author")
    @patch("ai_kit.cli.commands.notebook.prompt_confirmation")
    def test_create_command_success(
        self,
        mock_confirm,
        mock_author,
        mock_purpose,
        mock_name,
        mock_category,
        runner,
        mock_environment,
    ):
        """Test successful notebook creation."""
        # Setup mocks
        mock_category.return_value = "exploratory"
        mock_name.return_value = "test-notebook"
        mock_purpose.return_value = "This is a test notebook"
        mock_author.return_value = "Test User"
        mock_confirm.return_value = True

        result = runner.invoke(cli, ["notebook", "create"])

        assert result.exit_code == 0
        # Verify notebook was created
        notebook_path = mock_environment / "notebooks" / "exploratory" / "test-notebook.ipynb"
        assert notebook_path.exists()

    @patch("ai_kit.cli.commands.notebook.prompt_category")
    def test_create_command_cancelled_at_category(self, mock_category, runner, mock_environment):
        """Test creation cancelled at category selection."""
        mock_category.return_value = None

        result = runner.invoke(cli, ["notebook", "create"])

        assert result.exit_code == 1
        assert "No category selected" in result.output

    @patch("ai_kit.cli.commands.notebook.prompt_category")
    @patch("ai_kit.cli.commands.notebook.prompt_notebook_name")
    @patch("ai_kit.cli.commands.notebook.prompt_purpose")
    @patch("ai_kit.cli.commands.notebook.prompt_author")
    @patch("ai_kit.cli.commands.notebook.prompt_confirmation")
    def test_create_command_cancelled_at_confirmation(
        self,
        mock_confirm,
        mock_author,
        mock_purpose,
        mock_name,
        mock_category,
        runner,
        mock_environment,
    ):
        """Test creation cancelled at confirmation."""
        mock_category.return_value = "exploratory"
        mock_name.return_value = "test-notebook"
        mock_purpose.return_value = "Test purpose"
        mock_author.return_value = "Test User"
        mock_confirm.return_value = False

        result = runner.invoke(cli, ["notebook", "create"])

        assert result.exit_code == 2
        assert "cancelled" in result.output.lower()


class TestNotebookListCommand:
    """Test notebook list command."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def mock_notebooks(self, tmp_path, monkeypatch):
        """Create mock notebooks for testing."""
        notebooks_dir = tmp_path / "notebooks"
        (tmp_path / "pyproject.toml").touch()

        # Create notebooks in different categories
        for category in ["exploratory", "evaluations", "compliance"]:
            category_dir = notebooks_dir / category
            category_dir.mkdir(parents=True)
            
            # Create a test notebook
            notebook = nbformat.v4.new_notebook()
            notebook_path = category_dir / f"test-{category}.ipynb"
            with open(notebook_path, "w") as f:
                nbformat.write(notebook, f)

        monkeypatch.chdir(tmp_path)
        return tmp_path

    def test_list_command_shows_notebooks(self, runner, mock_notebooks):
        """Test that list command shows notebooks."""
        result = runner.invoke(cli, ["notebook", "list"])

        assert result.exit_code == 0
        assert "EXPLORATORY" in result.output or "exploratory" in result.output
        assert "test-exploratory.ipynb" in result.output

    def test_list_command_empty_categories(self, runner, tmp_path, monkeypatch):
        """Test list command with no notebooks."""
        notebooks_dir = tmp_path / "notebooks"
        notebooks_dir.mkdir()
        (tmp_path / "pyproject.toml").touch()
        
        for category in ["exploratory", "tutorials"]:
            (notebooks_dir / category).mkdir()

        monkeypatch.chdir(tmp_path)

        result = runner.invoke(cli, ["notebook", "list"])

        # Should complete without error even if empty
        assert result.exit_code == 0


class TestNotebookValidateCommand:
    """Test notebook validate command."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_validate_command_valid_notebook(self, runner, tmp_path):
        """Test validating a valid notebook."""
        # Create a valid notebook
        notebook_dir = tmp_path / "exploratory"
        notebook_dir.mkdir(parents=True)
        
        notebook = nbformat.v4.new_notebook(
            cells=[
                nbformat.v4.new_markdown_cell("""# Test Notebook

**Category**: exploratory
**Purpose**: This is a test notebook for validation
**Author**: Test User
**Created**: 2024-10-15
**Data Sources**:
- data/test.csv
**Dependencies**:
- pandas==2.1.0
""")
            ]
        )
        
        notebook_path = notebook_dir / "test.ipynb"
        with open(notebook_path, "w") as f:
            nbformat.write(notebook, f)

        result = runner.invoke(cli, ["notebook", "validate", str(notebook_path)])

        assert result.exit_code == 0
        assert "passed" in result.output.lower()

    def test_validate_command_invalid_notebook(self, runner, tmp_path):
        """Test validating an invalid notebook."""
        # Create an invalid notebook (missing metadata)
        notebook_dir = tmp_path / "exploratory"
        notebook_dir.mkdir(parents=True)
        
        notebook = nbformat.v4.new_notebook(
            cells=[nbformat.v4.new_code_cell("print('hello')")]
        )
        
        notebook_path = notebook_dir / "invalid.ipynb"
        with open(notebook_path, "w") as f:
            nbformat.write(notebook, f)

        result = runner.invoke(cli, ["notebook", "validate", str(notebook_path)])

        assert result.exit_code == 1


class TestNotebookStatsCommand:
    """Test notebook stats command."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_stats_command_shows_counts(self, runner, tmp_path, monkeypatch):
        """Test that stats command shows notebook counts."""
        notebooks_dir = tmp_path / "notebooks"
        (tmp_path / "pyproject.toml").touch()

        # Create notebooks
        for category in ["exploratory", "evaluations"]:
            category_dir = notebooks_dir / category
            category_dir.mkdir(parents=True)
            
            for i in range(2):
                notebook = nbformat.v4.new_notebook()
                notebook_path = category_dir / f"test-{i}.ipynb"
                with open(notebook_path, "w") as f:
                    nbformat.write(notebook, f)

        monkeypatch.chdir(tmp_path)

        result = runner.invoke(cli, ["notebook", "stats"])

        assert result.exit_code == 0
        assert "exploratory: 2" in result.output
        assert "evaluations: 2" in result.output
        assert "Total: 4" in result.output


class TestNotebookDeleteCommand:
    """Test notebook delete command."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    def test_delete_command_with_confirmation(self, runner, tmp_path):
        """Test deleting notebook with confirmation."""
        # Create a notebook
        notebook_path = tmp_path / "test.ipynb"
        notebook = nbformat.v4.new_notebook()
        with open(notebook_path, "w") as f:
            nbformat.write(notebook, f)

        # Confirm deletion
        result = runner.invoke(cli, ["notebook", "delete", str(notebook_path)], input="y\n")

        assert result.exit_code == 0
        assert not notebook_path.exists()

    def test_delete_command_cancelled(self, runner, tmp_path):
        """Test cancelling notebook deletion."""
        # Create a notebook
        notebook_path = tmp_path / "test.ipynb"
        notebook = nbformat.v4.new_notebook()
        with open(notebook_path, "w") as f:
            nbformat.write(notebook, f)

        # Cancel deletion
        result = runner.invoke(cli, ["notebook", "delete", str(notebook_path)], input="n\n")

        # Should be cancelled (exit code 1 for abort)
        assert notebook_path.exists()


class TestNotebookCommandIntegration:
    """Test integration between notebook commands."""

    @pytest.fixture
    def runner(self):
        """Create CLI test runner."""
        return CliRunner()

    @pytest.fixture
    def setup_environment(self, tmp_path, monkeypatch):
        """Set up complete test environment."""
        notebooks_dir = tmp_path / "notebooks"
        templates_dir = notebooks_dir / "templates"
        templates_dir.mkdir(parents=True)
        (tmp_path / "pyproject.toml").touch()

        # Create templates
        for category in ["exploratory", "tutorials"]:
            template = nbformat.v4.new_notebook(
                cells=[nbformat.v4.new_markdown_cell("# Template\n\n**Category**: {category}\n")]
            )
            filename = f"{category}-template.ipynb" if category != "tutorials" else "tutorial-template.ipynb"
            with open(templates_dir / filename, "w") as f:
                nbformat.write(template, f)

            (notebooks_dir / category).mkdir()

        monkeypatch.chdir(tmp_path)
        return tmp_path

    @patch("ai_kit.cli.commands.notebook.prompt_category")
    @patch("ai_kit.cli.commands.notebook.prompt_notebook_name")
    @patch("ai_kit.cli.commands.notebook.prompt_purpose")
    @patch("ai_kit.cli.commands.notebook.prompt_author")
    @patch("ai_kit.cli.commands.notebook.prompt_confirmation")
    def test_create_list_validate_workflow(
        self,
        mock_confirm,
        mock_author,
        mock_purpose,
        mock_name,
        mock_category,
        runner,
        setup_environment,
    ):
        """Test complete workflow: create, list, validate."""
        # Setup mocks for creation
        mock_category.return_value = "exploratory"
        mock_name.return_value = "integration-test"
        mock_purpose.return_value = "Testing complete workflow integration"
        mock_author.return_value = "Test User"
        mock_confirm.return_value = True

        # Create notebook
        create_result = runner.invoke(cli, ["notebook", "create"])
        assert create_result.exit_code == 0

        # List notebooks
        list_result = runner.invoke(cli, ["notebook", "list"])
        assert list_result.exit_code == 0
        assert "integration-test.ipynb" in list_result.output

        # Validate notebook
        notebook_path = setup_environment / "notebooks" / "exploratory" / "integration-test.ipynb"
        validate_result = runner.invoke(cli, ["notebook", "validate", str(notebook_path)])
        assert validate_result.exit_code == 0

        # Check stats
        stats_result = runner.invoke(cli, ["notebook", "stats"])
        assert stats_result.exit_code == 0
        assert "Total: 1" in stats_result.output
