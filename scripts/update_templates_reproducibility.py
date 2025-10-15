"""Update notebook templates with enhanced reproducibility documentation."""

import json
from pathlib import Path

# Template updates for reproducibility
ENHANCED_METADATA = {
    "exploratory": {
        "data_sources_text": """**Data Sources**:
- Path: `data/your-dataset.csv`
- Version/Date: YYYY-MM-DD
- Access method: Local file / API / Database
- Size: ~X MB
- Schema: Describe key columns""",
        "dependencies_text": """**Dependencies**:
```
# Add to pyproject.toml or requirements.txt
pandas>=2.1.0
matplotlib>=3.8.0
seaborn>=0.13.0
```

**Environment**:
- Python: 3.12+
- Workspace: ai-kit (uv workspace)""",
    },
    "tutorial": {
        "data_sources_text": """**Data Sources**:
- Example datasets: Describe where learners can access data
- Public datasets: Links to download locations
- Generated data: Scripts to create sample data""",
        "dependencies_text": """**Dependencies**:
```
# Required packages for this tutorial
package-name>=version
```

**Prerequisites**:
- Python 3.12+
- Basic knowledge of: [list topics]""",
    },
    "evaluation": {
        "data_sources_text": """**Data Sources**:
- Training data: Path and version
- Validation data: Path and version
- Test data: Path and version
- Baseline results: Path to comparison data""",
        "dependencies_text": """**Dependencies**:
```
# Model evaluation dependencies
scikit-learn>=1.3.0
numpy>=1.24.0
pandas>=2.1.0
```

**Model Requirements**:
- Model file: Path to saved model
- Model version: Semantic version
- Training commit: Git SHA of training code""",
    },
    "compliance": {
        "data_sources_text": """**Data Sources**:
- Training dataset: Path, version, characteristics
- Validation dataset: Path, version
- Bias assessment data: Path to demographic data
- Performance logs: Path to model outputs""",
        "dependencies_text": """**Dependencies**:
```
# Compliance analysis tools
pandas>=2.1.0
numpy>=1.24.0
matplotlib>=3.8.0
```

**Regulatory Context**:
- Framework: EU AI Act
- Risk level: [high/limited/minimal]
- Review date: YYYY-MM-DD""",
    },
    "reporting": {
        "data_sources_text": """**Data Sources**:
- Primary data: Path and refresh schedule
- Reference data: Path to lookup tables
- Historical data: Path to time series
- API endpoints: URLs and authentication method""",
        "dependencies_text": """**Dependencies**:
```
# Reporting dependencies
papermill>=2.4.0  # For parameterized execution
pandas>=2.1.0
matplotlib>=3.8.0
```

**Execution**:
```bash
# Run with papermill
papermill input.ipynb output.ipynb -p start_date 2024-01-01 -p end_date 2024-12-31
```""",
    },
}


def update_template(template_path: Path, category: str) -> None:
    """Update a template with enhanced reproducibility documentation."""
    with open(template_path) as f:
        notebook = json.load(f)

    # Find the first markdown cell
    for cell in notebook["cells"]:
        if cell["cell_type"] == "markdown":
            source = "".join(cell["source"]) if isinstance(cell["source"], list) else cell["source"]

            # Update data sources section
            if "**Data Sources**:" in source and category in ENHANCED_METADATA:
                source = source.replace(
                    "**Data Sources**: \n- [List your data sources]",
                    ENHANCED_METADATA[category]["data_sources_text"],
                )
                source = source.replace(
                    "**Data Sources**:\n- [List your data sources]",
                    ENHANCED_METADATA[category]["data_sources_text"],
                )

            # Update dependencies section
            if "**Dependencies**:" in source and category in ENHANCED_METADATA:
                source = source.replace(
                    "**Dependencies**:\n- [List key dependencies]",
                    ENHANCED_METADATA[category]["dependencies_text"],
                )

            # Convert back to list format
            cell["source"] = source.split("\n")
            break

    # Write updated notebook
    with open(template_path, "w") as f:
        json.dump(notebook, f, indent=1)

    print(f"✓ Updated {template_path.name}")


def main():
    """Update all templates."""
    templates_dir = Path("notebooks/templates")

    templates = {
        "exploratory": "exploratory-template.ipynb",
        "tutorial": "tutorial-template.ipynb",
        "evaluation": "evaluation-template.ipynb",
        "compliance": "compliance-template.ipynb",
        "reporting": "reporting-template.ipynb",
    }

    for category, filename in templates.items():
        template_path = templates_dir / filename
        if template_path.exists():
            update_template(template_path, category)
        else:
            print(f"✗ Template not found: {template_path}")


if __name__ == "__main__":
    main()
