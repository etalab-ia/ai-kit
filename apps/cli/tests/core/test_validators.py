"""Tests for notebook validators."""

import json

import pytest

from ai_kit.cli.core.validators import (
    check_notebook_size,
    extract_metadata_from_markdown,
    validate_notebook_metadata,
)


class TestExtractMetadataFromMarkdown:
    """Test metadata extraction from markdown cells."""

    def test_extract_basic_metadata(self):
        """Test extraction of basic metadata fields."""
        markdown = """
# My Notebook

**Category**: exploratory
**Purpose**: Test notebook for validation
**Author**: Test User
**Created**: 2024-10-15
**Data Sources**:
- data/test.csv
**Dependencies**:
- pandas==2.1.0
"""
        metadata = extract_metadata_from_markdown(markdown)

        assert metadata["category"] == "exploratory"
        assert metadata["purpose"] == "Test notebook for validation"
        assert metadata["author"] == "Test User"
        assert metadata["created"] == "2024-10-15"
        assert metadata["data_sources"] == ["data/test.csv"]
        assert metadata["dependencies"] == ["pandas==2.1.0"]

    def test_extract_multiple_data_sources(self):
        """Test extraction of multiple data sources."""
        markdown = """
**Data Sources**:
- data/source1.csv
- data/source2.csv
- https://example.com/data
"""
        metadata = extract_metadata_from_markdown(markdown)

        assert len(metadata["data_sources"]) == 3
        assert "data/source1.csv" in metadata["data_sources"]
        assert "data/source2.csv" in metadata["data_sources"]
        assert "https://example.com/data" in metadata["data_sources"]

    def test_extract_empty_lists(self):
        """Test extraction when lists are empty."""
        markdown = """
**Category**: exploratory
**Purpose**: Test
**Author**: User
**Created**: 2024-10-15
"""
        metadata = extract_metadata_from_markdown(markdown)

        assert metadata["data_sources"] == []
        assert metadata["dependencies"] == []


class TestValidateNotebookMetadata:
    """Test notebook metadata validation."""

    @pytest.fixture
    def temp_notebook(self, tmp_path):
        """Create a temporary notebook file."""

        def _create_notebook(cells=None, metadata=None):
            if cells is None:
                cells = []
            if metadata is None:
                metadata = {}

            notebook = {
                "cells": cells,
                "metadata": metadata,
                "nbformat": 4,
                "nbformat_minor": 5,
            }

            notebook_path = tmp_path / "test_notebook.ipynb"
            with open(notebook_path, "w") as f:
                json.dump(notebook, f)

            return notebook_path

        return _create_notebook

    def test_valid_notebook(self, temp_notebook):
        """Test validation of a valid notebook."""
        cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": """# Test Notebook

**Category**: exploratory
**Purpose**: This is a test notebook for validation purposes
**Author**: Test User
**Created**: 2024-10-15
**Data Sources**:
- data/test.csv
**Dependencies**:
- pandas==2.1.0
""",
            }
        ]

        notebook_path = temp_notebook(cells=cells)
        # Rename to match category
        new_path = notebook_path.parent / "exploratory" / "test_notebook.ipynb"
        new_path.parent.mkdir(exist_ok=True)
        notebook_path.rename(new_path)

        result = validate_notebook_metadata(new_path)

        assert result.passed is True
        assert len(result.errors) == 0

    def test_missing_file(self, tmp_path):
        """Test validation of non-existent file."""
        notebook_path = tmp_path / "nonexistent.ipynb"

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "FILE_NOT_FOUND"

    def test_invalid_json(self, tmp_path):
        """Test validation of invalid JSON."""
        notebook_path = tmp_path / "invalid.ipynb"
        with open(notebook_path, "w") as f:
            f.write("not valid json")

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert len(result.errors) == 1
        # nbformat raises a generic exception for invalid JSON, caught as READ_ERROR
        assert result.errors[0].code == "READ_ERROR"

    def test_no_cells(self, temp_notebook):
        """Test validation of notebook with no cells."""
        notebook_path = temp_notebook(cells=[])

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert any(e.code == "NO_CELLS" for e in result.errors)

    def test_first_cell_not_markdown(self, temp_notebook):
        """Test validation when first cell is not markdown."""
        cells = [{"cell_type": "code", "metadata": {}, "source": "print('hello')"}]

        notebook_path = temp_notebook(cells=cells)

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert any(e.code == "FIRST_CELL_NOT_MARKDOWN" for e in result.errors)

    def test_missing_required_field(self, temp_notebook):
        """Test validation with missing required field."""
        cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": """# Test Notebook

**Category**: exploratory
**Author**: Test User
**Created**: 2024-10-15
""",
            }
        ]

        notebook_path = temp_notebook(cells=cells)

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert any(e.code == "MISSING_METADATA" and e.field == "purpose" for e in result.errors)

    def test_invalid_category(self, temp_notebook):
        """Test validation with invalid category."""
        cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": """# Test Notebook

**Category**: invalid_category
**Purpose**: Test notebook
**Author**: Test User
**Created**: 2024-10-15
""",
            }
        ]

        notebook_path = temp_notebook(cells=cells)

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert any(e.code == "INVALID_CATEGORY" for e in result.errors)

    def test_category_mismatch(self, temp_notebook):
        """Test validation when category doesn't match directory."""
        cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": """# Test Notebook

**Category**: exploratory
**Purpose**: This is a test notebook for validation purposes
**Author**: Test User
**Created**: 2024-10-15
**Data Sources**:
- data/test.csv
**Dependencies**:
- pandas==2.1.0
""",
            }
        ]

        notebook_path = temp_notebook(cells=cells)
        # Put in wrong directory
        new_path = notebook_path.parent / "tutorials" / "test_notebook.ipynb"
        new_path.parent.mkdir(exist_ok=True)
        notebook_path.rename(new_path)

        result = validate_notebook_metadata(new_path)

        assert result.passed is False
        assert any(e.code == "CATEGORY_MISMATCH" for e in result.errors)

    def test_purpose_too_short(self, temp_notebook):
        """Test validation when purpose is too short."""
        cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": """# Test Notebook

**Category**: exploratory
**Purpose**: Short
**Author**: Test User
**Created**: 2024-10-15
""",
            }
        ]

        notebook_path = temp_notebook(cells=cells)

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert any(e.code == "PURPOSE_TOO_SHORT" for e in result.errors)

    def test_invalid_date_format(self, temp_notebook):
        """Test validation with invalid date format."""
        cells = [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": """# Test Notebook

**Category**: exploratory
**Purpose**: This is a test notebook for validation purposes
**Author**: Test User
**Created**: 15-10-2024
""",
            }
        ]

        notebook_path = temp_notebook(cells=cells)

        result = validate_notebook_metadata(notebook_path)

        assert result.passed is False
        assert any(e.code == "INVALID_DATE" for e in result.errors)


class TestCheckNotebookSize:
    """Test notebook size checking."""

    def test_size_ok(self, tmp_path):
        """Test notebook within size limits."""
        notebook_path = tmp_path / "small.ipynb"
        # Create 1 MB file
        with open(notebook_path, "w") as f:
            f.write("x" * (1024 * 1024))

        result = check_notebook_size(notebook_path, warn_mb=5.0, block_mb=10.0)

        assert result.passed is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 0

    def test_size_warning(self, tmp_path):
        """Test notebook exceeds warning threshold."""
        notebook_path = tmp_path / "medium.ipynb"
        # Create 6 MB file
        with open(notebook_path, "w") as f:
            f.write("x" * (6 * 1024 * 1024))

        result = check_notebook_size(notebook_path, warn_mb=5.0, block_mb=10.0)

        assert result.passed is True
        assert len(result.errors) == 0
        assert len(result.warnings) == 1
        assert result.warnings[0].code == "SIZE_WARNING"

    def test_size_exceeded(self, tmp_path):
        """Test notebook exceeds block threshold."""
        notebook_path = tmp_path / "large.ipynb"
        # Create 11 MB file
        with open(notebook_path, "w") as f:
            f.write("x" * (11 * 1024 * 1024))

        result = check_notebook_size(notebook_path, warn_mb=5.0, block_mb=10.0)

        assert result.passed is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "SIZE_EXCEEDED"

    def test_missing_file(self, tmp_path):
        """Test size check on non-existent file."""
        notebook_path = tmp_path / "nonexistent.ipynb"

        result = check_notebook_size(notebook_path)

        assert result.passed is False
        assert len(result.errors) == 1
        assert result.errors[0].code == "FILE_NOT_FOUND"
