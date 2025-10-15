"""Tests for prompt utilities."""

from unittest.mock import patch

from ai_kit.cli.utils.prompts import (
    prompt_additional_field,
    prompt_author,
    prompt_category,
    prompt_confirmation,
    prompt_notebook_name,
    prompt_purpose,
)


class TestPromptCategory:
    """Test category selection prompt."""

    @patch("questionary.select")
    def test_prompt_category_success(self, mock_select):
        """Test successful category selection."""
        mock_select.return_value.ask.return_value = "exploratory"

        result = prompt_category()

        assert result == "exploratory"
        mock_select.assert_called_once()
        call_args = mock_select.call_args
        assert "Select notebook category" in call_args[0][0]

    @patch("questionary.select")
    def test_prompt_category_cancelled(self, mock_select):
        """Test when user cancels category selection."""
        mock_select.return_value.ask.return_value = None

        result = prompt_category()

        assert result is None

    @patch("questionary.select")
    def test_prompt_category_includes_all_categories(self, mock_select):
        """Test that all categories are included in choices."""
        mock_select.return_value.ask.return_value = "compliance"

        prompt_category()

        call_args = mock_select.call_args
        choices = call_args[1]["choices"]

        # Should have choices for all 5 categories
        assert len(choices) >= 5


class TestPromptNotebookName:
    """Test notebook name prompt."""

    @patch("questionary.text")
    def test_prompt_notebook_name_success(self, mock_text):
        """Test successful notebook name input."""
        mock_text.return_value.ask.return_value = "my-notebook"

        result = prompt_notebook_name()

        assert result == "my-notebook"
        mock_text.assert_called_once()

    @patch("questionary.text")
    def test_prompt_notebook_name_cancelled(self, mock_text):
        """Test when user cancels name input."""
        mock_text.return_value.ask.return_value = None

        result = prompt_notebook_name()

        assert result is None

    @patch("questionary.text")
    def test_prompt_notebook_name_validation(self, mock_text):
        """Test that validation function is provided."""
        mock_text.return_value.ask.return_value = "valid-name"

        prompt_notebook_name()

        call_args = mock_text.call_args
        # Should have a validate parameter
        assert "validate" in call_args[1]


class TestPromptPurpose:
    """Test purpose prompt."""

    @patch("questionary.text")
    def test_prompt_purpose_success(self, mock_text):
        """Test successful purpose input."""
        mock_text.return_value.ask.return_value = "This is a test notebook for validation"

        result = prompt_purpose()

        assert result == "This is a test notebook for validation"
        mock_text.assert_called_once()

    @patch("questionary.text")
    def test_prompt_purpose_multiline(self, mock_text):
        """Test that multiline input is supported."""
        mock_text.return_value.ask.return_value = "Line 1\nLine 2"

        result = prompt_purpose()

        assert "Line 1" in result
        assert "Line 2" in result

    @patch("questionary.text")
    def test_prompt_purpose_validation(self, mock_text):
        """Test that validation function is provided."""
        mock_text.return_value.ask.return_value = "Valid purpose text"

        prompt_purpose()

        call_args = mock_text.call_args
        # Should have a validate parameter for minimum length
        assert "validate" in call_args[1]


class TestPromptAuthor:
    """Test author prompt."""

    @patch("questionary.text")
    def test_prompt_author_with_default(self, mock_text):
        """Test author prompt with default value."""
        mock_text.return_value.ask.return_value = "John Doe"

        result = prompt_author(default="John Doe")

        assert result == "John Doe"
        call_args = mock_text.call_args
        assert call_args[1]["default"] == "John Doe"

    @patch("questionary.text")
    def test_prompt_author_without_default(self, mock_text):
        """Test author prompt without default value."""
        mock_text.return_value.ask.return_value = "Jane Smith"

        result = prompt_author()

        assert result == "Jane Smith"

    @patch("questionary.text")
    def test_prompt_author_uses_default(self, mock_text):
        """Test that default value is used when provided."""
        mock_text.return_value.ask.return_value = "Git User"

        prompt_author(default="Git User")

        call_args = mock_text.call_args
        assert call_args[1]["default"] == "Git User"


class TestPromptAdditionalField:
    """Test additional field prompt."""

    @patch("questionary.text")
    def test_prompt_additional_field_success(self, mock_text):
        """Test successful additional field input."""
        mock_text.return_value.ask.return_value = "v1.0"

        result = prompt_additional_field("model_version")

        assert result == "v1.0"
        mock_text.assert_called_once()

    @patch("questionary.text")
    def test_prompt_additional_field_formats_label(self, mock_text):
        """Test that field name is formatted for display."""
        mock_text.return_value.ask.return_value = "high"

        prompt_additional_field("risk_level")

        call_args = mock_text.call_args
        # Should format risk_level as "Risk Level"
        assert "Risk Level" in call_args[0][0] or "risk_level" in call_args[0][0]

    @patch("questionary.text")
    def test_prompt_additional_field_optional(self, mock_text):
        """Test that additional fields are optional."""
        mock_text.return_value.ask.return_value = ""

        result = prompt_additional_field("optional_field")

        # Empty string should be returned as-is
        assert result == ""


class TestPromptConfirmation:
    """Test confirmation prompt."""

    @patch("questionary.confirm")
    def test_prompt_confirmation_yes(self, mock_confirm):
        """Test confirmation when user says yes."""
        mock_confirm.return_value.ask.return_value = True
        summary = {"Category": "exploratory", "Name": "test-notebook"}

        result = prompt_confirmation(summary)

        assert result is True
        mock_confirm.assert_called_once()

    @patch("questionary.confirm")
    def test_prompt_confirmation_no(self, mock_confirm):
        """Test confirmation when user says no."""
        mock_confirm.return_value.ask.return_value = False
        summary = {"Category": "exploratory", "Name": "test-notebook"}

        result = prompt_confirmation(summary)

        assert result is False

    @patch("questionary.confirm")
    def test_prompt_confirmation_displays_summary(self, mock_confirm):
        """Test that summary is displayed before confirmation."""
        mock_confirm.return_value.ask.return_value = True
        summary = {
            "Category": "exploratory",
            "Path": "notebooks/exploratory/test.ipynb",
            "Purpose": "Test notebook",
            "Author": "Test User",
        }

        prompt_confirmation(summary)

        # Confirmation should be called
        mock_confirm.assert_called_once()

    @patch("questionary.confirm")
    def test_prompt_confirmation_cancelled(self, mock_confirm):
        """Test when user cancels confirmation."""
        mock_confirm.return_value.ask.return_value = None
        summary = {"Category": "exploratory"}

        result = prompt_confirmation(summary)

        # None should be treated as False
        assert result is None or result is False


class TestPromptIntegration:
    """Test integration between prompts."""

    @patch("questionary.select")
    @patch("questionary.text")
    @patch("questionary.confirm")
    def test_full_notebook_creation_flow(self, mock_confirm, mock_text, mock_select):
        """Test full flow of prompts for notebook creation."""
        # Setup mock responses
        mock_select.return_value.ask.return_value = "exploratory"
        mock_text.return_value.ask.side_effect = [
            "test-notebook",  # name
            "This is a test notebook for validation purposes",  # purpose
            "Test User",  # author
        ]
        mock_confirm.return_value.ask.return_value = True

        # Simulate the flow
        category = prompt_category()
        name = prompt_notebook_name()
        purpose = prompt_purpose()
        author = prompt_author()

        summary = {
            "Category": category,
            "Name": name,
            "Purpose": purpose,
            "Author": author,
        }
        confirmed = prompt_confirmation(summary)

        assert category == "exploratory"
        assert name == "test-notebook"
        assert "test notebook" in purpose.lower()
        assert author == "Test User"
        assert confirmed is True
