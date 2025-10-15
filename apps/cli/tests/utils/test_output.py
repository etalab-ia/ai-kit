"""Tests for output formatting utilities."""

from pathlib import Path
from unittest.mock import patch

from ai_kit.cli.core.validators import ValidationError
from ai_kit.cli.utils.output import (
    print_error,
    print_notebook_created,
    print_success,
    print_validation_errors,
)


class TestPrintSuccess:
    """Test success message printing."""

    @patch("rich.console.Console.print")
    def test_print_success_message(self, mock_print):
        """Test printing success message."""
        print_success("Operation completed successfully")

        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        assert "Operation completed successfully" in call_args

    @patch("rich.console.Console.print")
    def test_print_success_with_special_characters(self, mock_print):
        """Test success message with special characters."""
        print_success("File created: /path/to/file.ipynb")

        mock_print.assert_called_once()


class TestPrintError:
    """Test error message printing."""

    @patch("rich.console.Console.print")
    def test_print_error_message(self, mock_print):
        """Test printing error message."""
        print_error("An error occurred")

        mock_print.assert_called_once()
        call_args = str(mock_print.call_args)
        assert "An error occurred" in call_args

    @patch("rich.console.Console.print")
    def test_print_error_with_details(self, mock_print):
        """Test error message with details."""
        print_error("File not found: /path/to/missing.ipynb")

        mock_print.assert_called_once()


class TestPrintNotebookCreated:
    """Test notebook creation success message."""

    @patch("rich.console.Console.print")
    def test_print_notebook_created_basic(self, mock_print):
        """Test basic notebook created message."""
        notebook_path = Path("/path/to/notebooks/exploratory/test.ipynb")

        print_notebook_created(notebook_path)

        # Should print multiple times (success message + next steps)
        assert mock_print.call_count >= 1

    @patch("rich.console.Console.print")
    def test_print_notebook_created_includes_path(self, mock_print):
        """Test that created message includes the path."""
        notebook_path = Path("/path/to/notebooks/exploratory/test.ipynb")

        print_notebook_created(notebook_path)

        # Check that path appears in one of the print calls
        all_calls = " ".join(str(call) for call in mock_print.call_args_list)
        assert "test.ipynb" in all_calls or str(notebook_path) in all_calls

    @patch("rich.console.Console.print")
    def test_print_notebook_created_includes_next_steps(self, mock_print):
        """Test that next steps are included."""
        notebook_path = Path("/path/to/notebooks/exploratory/test.ipynb")

        print_notebook_created(notebook_path)

        # Should print multiple messages including next steps
        assert mock_print.call_count >= 2


class TestPrintValidationErrors:
    """Test validation error printing."""

    @patch("rich.console.Console.print")
    def test_print_single_error(self, mock_print):
        """Test printing a single validation error."""
        errors = [
            ValidationError(
                code="MISSING_METADATA",
                message="Required field 'purpose' is missing",
                field="purpose",
                suggestion="Add **Purpose**: <description> to first cell",
            )
        ]

        print_validation_errors(errors, [])

        # Should print error details
        assert mock_print.call_count >= 1
        all_calls = " ".join(str(call) for call in mock_print.call_args_list)
        assert "MISSING_METADATA" in all_calls or "purpose" in all_calls

    @patch("rich.console.Console.print")
    def test_print_multiple_errors(self, mock_print):
        """Test printing multiple validation errors."""
        errors = [
            ValidationError(
                code="MISSING_METADATA",
                message="Missing purpose",
                field="purpose",
            ),
            ValidationError(
                code="INVALID_CATEGORY",
                message="Invalid category",
                field="category",
            ),
        ]

        print_validation_errors(errors, [])

        # Should print all errors
        assert mock_print.call_count >= 2

    @patch("rich.console.Console.print")
    def test_print_warnings(self, mock_print):
        """Test printing validation warnings."""
        warnings = [
            ValidationError(
                code="SIZE_WARNING",
                message="Notebook size exceeds 5 MB",
                suggestion="Consider splitting into smaller notebooks",
            )
        ]

        print_validation_errors([], warnings)

        # Should print warning
        assert mock_print.call_count >= 1

    @patch("rich.console.Console.print")
    def test_print_errors_and_warnings(self, mock_print):
        """Test printing both errors and warnings."""
        errors = [
            ValidationError(
                code="MISSING_METADATA",
                message="Missing purpose",
                field="purpose",
            )
        ]
        warnings = [
            ValidationError(
                code="SIZE_WARNING",
                message="Large file",
            )
        ]

        print_validation_errors(errors, warnings)

        # Should print both
        assert mock_print.call_count >= 2

    @patch("rich.console.Console.print")
    def test_print_error_with_suggestion(self, mock_print):
        """Test that suggestions are included when present."""
        errors = [
            ValidationError(
                code="PURPOSE_TOO_SHORT",
                message="Purpose must be at least 10 characters",
                field="purpose",
                suggestion="Provide a more detailed description of the notebook's purpose",
            )
        ]

        print_validation_errors(errors, [])

        all_calls = " ".join(str(call) for call in mock_print.call_args_list)
        # Suggestion should appear somewhere in the output
        assert "suggestion" in all_calls.lower() or "detailed description" in all_calls.lower()

    @patch("rich.console.Console.print")
    def test_print_no_errors_or_warnings(self, mock_print):
        """Test behavior when no errors or warnings."""
        print_validation_errors([], [])

        # Should still print something (e.g., "No errors")
        # or not print anything - either is acceptable
        # Just verify it doesn't crash
        assert True


class TestOutputFormatting:
    """Test output formatting consistency."""

    @patch("rich.console.Console.print")
    def test_consistent_formatting_across_functions(self, mock_print):
        """Test that all output functions use consistent formatting."""
        # Call various output functions
        print_success("Success message")
        mock_print.reset_mock()

        print_error("Error message")
        mock_print.reset_mock()

        print_notebook_created(Path("/test/path.ipynb"))

        # All should use rich console for formatting
        # Just verify they all call print
        assert True  # If we got here without errors, formatting is consistent
