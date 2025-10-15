"""Tests for configuration module."""

from ai_kit.cli.core.config import (
    CATEGORIES,
    CategoryConfig,
    get_category_dir,
    get_notebooks_dir,
    get_templates_dir,
)


class TestCategoryConfig:
    """Test category configuration."""

    def test_all_categories_defined(self):
        """Test that all expected categories are defined."""
        expected_categories = {
            "exploratory",
            "tutorials",
            "evaluations",
            "compliance",
            "reporting",
        }

        assert set(CATEGORIES.keys()) == expected_categories

    def test_category_structure(self):
        """Test that each category has required fields."""
        for category_name, config in CATEGORIES.items():
            assert isinstance(config, CategoryConfig)
            assert config.name == category_name
            assert config.display_name
            assert config.description
            assert config.governance_level in ["low", "medium", "high"]
            assert isinstance(config.speckit_required, bool)
            assert config.retention_policy in [
                "delete_after_migration",
                "retain",
                "retain_and_tag",
            ]
            assert config.template_file.endswith(".ipynb")
            assert isinstance(config.additional_metadata, list)

    def test_exploratory_config(self):
        """Test exploratory category configuration."""
        config = CATEGORIES["exploratory"]

        assert config.display_name == "Exploratory"
        assert config.governance_level == "low"
        assert config.speckit_required is False
        assert config.retention_policy == "delete_after_migration"
        assert config.template_file == "exploratory-template.ipynb"
        assert config.additional_metadata == []

    def test_compliance_config(self):
        """Test compliance category configuration."""
        config = CATEGORIES["compliance"]

        assert config.display_name == "Compliance"
        assert config.governance_level == "high"
        assert config.speckit_required is True
        assert config.retention_policy == "retain_and_tag"
        assert config.template_file == "compliance-template.ipynb"
        assert "risk_level" in config.additional_metadata
        assert "regulatory_framework" in config.additional_metadata
        assert "review_date" in config.additional_metadata

    def test_evaluations_config(self):
        """Test evaluations category configuration."""
        config = CATEGORIES["evaluations"]

        assert config.display_name == "Evaluations"
        assert config.governance_level == "medium"
        assert config.speckit_required is True
        assert config.retention_policy == "retain_and_tag"
        assert "model_version" in config.additional_metadata
        assert "evaluation_metrics" in config.additional_metadata


class TestPathFunctions:
    """Test path resolution functions."""

    def test_get_notebooks_dir_from_root(self, tmp_path, monkeypatch):
        """Test getting notebooks directory from repository root."""
        # Create mock repository structure
        notebooks_dir = tmp_path / "notebooks"
        notebooks_dir.mkdir()
        (tmp_path / "pyproject.toml").touch()

        # Change to repository root
        monkeypatch.chdir(tmp_path)

        result = get_notebooks_dir()

        assert result == notebooks_dir

    def test_get_notebooks_dir_from_subdirectory(self, tmp_path, monkeypatch):
        """Test getting notebooks directory from subdirectory."""
        # Create mock repository structure
        notebooks_dir = tmp_path / "notebooks"
        notebooks_dir.mkdir()
        (tmp_path / "pyproject.toml").touch()

        # Create subdirectory and change to it
        subdir = tmp_path / "apps" / "cli"
        subdir.mkdir(parents=True)
        monkeypatch.chdir(subdir)

        result = get_notebooks_dir()

        assert result == notebooks_dir

    def test_get_templates_dir(self, tmp_path, monkeypatch):
        """Test getting templates directory."""
        # Create mock repository structure
        notebooks_dir = tmp_path / "notebooks"
        notebooks_dir.mkdir()
        templates_dir = notebooks_dir / "templates"
        templates_dir.mkdir()
        (tmp_path / "pyproject.toml").touch()

        monkeypatch.chdir(tmp_path)

        result = get_templates_dir()

        assert result == templates_dir

    def test_get_category_dir(self, tmp_path, monkeypatch):
        """Test getting category directory."""
        # Create mock repository structure
        notebooks_dir = tmp_path / "notebooks"
        notebooks_dir.mkdir()
        exploratory_dir = notebooks_dir / "exploratory"
        exploratory_dir.mkdir()
        (tmp_path / "pyproject.toml").touch()

        monkeypatch.chdir(tmp_path)

        result = get_category_dir("exploratory")

        assert result == exploratory_dir

    def test_get_notebooks_dir_fallback(self, tmp_path, monkeypatch):
        """Test fallback when notebooks directory not found."""
        # No notebooks directory, no pyproject.toml
        monkeypatch.chdir(tmp_path)

        result = get_notebooks_dir()

        # Should return current directory / notebooks
        assert result == tmp_path / "notebooks"
