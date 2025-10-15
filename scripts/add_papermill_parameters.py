"""Add papermill parameters section to reporting template."""

from pathlib import Path

import nbformat


def add_papermill_parameters():
    """Add papermill parameters cell to reporting template."""
    template_path = Path("notebooks/templates/reporting-template.ipynb")

    with open(template_path) as f:
        notebook = nbformat.read(f, as_version=4)

    # Create parameters cell (should be after metadata cell)
    parameters_cell = nbformat.v4.new_code_cell(
        source="""# Parameters (papermill will inject values here)
# These are default values - override with papermill -p flag

start_date = "2024-01-01"  # Report start date (YYYY-MM-DD)
end_date = "2024-12-31"    # Report end date (YYYY-MM-DD)
output_format = "html"     # Output format: html, pdf, markdown
include_charts = True      # Include visualizations
recipients = []            # Email recipients (if automated)"""
    )

    # Add tag for papermill
    parameters_cell.metadata["tags"] = ["parameters"]

    # Insert after first cell (metadata cell)
    notebook.cells.insert(1, parameters_cell)

    # Add a cell explaining papermill usage
    usage_cell = nbformat.v4.new_markdown_cell(
        source="""## Parameterized Execution

This notebook is designed for automated execution with [papermill](https://papermill.readthedocs.io/).

**Run manually**:
```bash
jupyter notebook reporting-template.ipynb
```

**Run with papermill**:
```bash
# Execute with custom parameters
papermill reporting-template.ipynb output-2024-q4.ipynb \\
  -p start_date 2024-10-01 \\
  -p end_date 2024-12-31 \\
  -p output_format html

# Convert to HTML report
jupyter nbconvert output-2024-q4.ipynb --to html
```

**Automation example**:
```bash
# Weekly report generation
just notebook execute reporting/weekly-report.ipynb \\
  -p start_date $(date -d '7 days ago' +%Y-%m-%d) \\
  -p end_date $(date +%Y-%m-%d)
```"""
    )

    notebook.cells.insert(2, usage_cell)

    # Write updated notebook
    with open(template_path, "w") as f:
        nbformat.write(notebook, f)

    print(f"✓ Added papermill parameters to {template_path.name}")


if __name__ == "__main__":
    add_papermill_parameters()
