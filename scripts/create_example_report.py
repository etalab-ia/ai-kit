"""Create example parameterized reporting notebook."""

from pathlib import Path

import nbformat

# Create example reporting notebook
notebook = nbformat.v4.new_notebook()

# Add kernel metadata
notebook.metadata = {
    "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
    "language_info": {"name": "python", "version": "3.12.0"},
}

# Metadata cell
metadata_cell = nbformat.v4.new_markdown_cell(
    source="""# Weekly Metrics Report

**Category**: reporting
**Purpose**: Generate weekly metrics summary for stakeholders
**Author**: AI-Kit Team
**Created**: 2024-10-15
**Data Sources**:
- Path: `data/metrics.csv` (simulated)
- Version/Date: Weekly refresh
- Access method: Local file
- Size: ~100 KB
- Schema: date (datetime), metric_name (str), value (float)

**Dependencies**:
```
pandas>=2.1.0
matplotlib>=3.8.0
```

**Environment**:
- Python: 3.12+
- Workspace: ai-kit (uv workspace)

**Execution**:
```bash
# Run with papermill
papermill example-report.ipynb output-2024-10-15.ipynb \\
  -p start_date 2024-10-08 \\
  -p end_date 2024-10-15

# Convert to HTML
jupyter nbconvert output-2024-10-15.ipynb --to html
```"""
)

# Parameters cell (tagged for papermill)
parameters_cell = nbformat.v4.new_code_cell(
    source="""# Parameters (papermill will inject values here)
start_date = "2024-10-01"  # Report start date (YYYY-MM-DD)
end_date = "2024-10-07"    # Report end date (YYYY-MM-DD)
output_format = "html"     # Output format: html, pdf, markdown"""
)
parameters_cell.metadata["tags"] = ["parameters"]

# Setup cell
setup_cell = nbformat.v4.new_code_cell(
    source="""import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Configure matplotlib
%matplotlib inline
plt.style.use('seaborn-v0_8-darkgrid')

print(f"Generating report for {start_date} to {end_date}")"""
)

# Data generation cell (simulated data for example)
data_cell = nbformat.v4.new_code_cell(
    source="""# Generate sample data for demonstration
# In production, replace with actual data loading

date_range = pd.date_range(start=start_date, end=end_date, freq='D')
metrics_data = {
    'date': date_range,
    'api_calls': [1000 + i * 50 for i in range(len(date_range))],
    'response_time_ms': [150 + (i % 3) * 10 for i in range(len(date_range))],
    'error_rate': [0.01 + (i % 5) * 0.002 for i in range(len(date_range))]
}

df = pd.DataFrame(metrics_data)
print(f"Loaded {len(df)} days of metrics")
df.head()"""
)

# Analysis cell
analysis_cell = nbformat.v4.new_code_cell(
    source="""# Calculate summary statistics
summary = {
    'Total API Calls': df['api_calls'].sum(),
    'Avg Response Time (ms)': df['response_time_ms'].mean(),
    'Avg Error Rate (%)': df['error_rate'].mean() * 100,
    'Peak API Calls': df['api_calls'].max(),
    'Date of Peak': df.loc[df['api_calls'].idxmax(), 'date'].strftime('%Y-%m-%d')
}

for key, value in summary.items():
    if isinstance(value, float):
        print(f"{key}: {value:.2f}")
    else:
        print(f"{key}: {value}")"""
)

# Visualization cell
viz_cell = nbformat.v4.new_code_cell(
    source="""# Create visualizations
fig, axes = plt.subplots(3, 1, figsize=(12, 10))

# API Calls over time
axes[0].plot(df['date'], df['api_calls'], marker='o', linewidth=2)
axes[0].set_title('API Calls Over Time', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Number of Calls')
axes[0].grid(True, alpha=0.3)

# Response Time over time
axes[1].plot(df['date'], df['response_time_ms'], marker='s', color='orange', linewidth=2)
axes[1].set_title('Response Time Over Time', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Response Time (ms)')
axes[1].grid(True, alpha=0.3)

# Error Rate over time
axes[2].plot(df['date'], df['error_rate'] * 100, marker='^', color='red', linewidth=2)
axes[2].set_title('Error Rate Over Time', fontsize=14, fontweight='bold')
axes[2].set_ylabel('Error Rate (%)')
axes[2].set_xlabel('Date')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.show()"""
)

# Conclusion cell
conclusion_cell = nbformat.v4.new_markdown_cell(
    source="""## Conclusion

This report demonstrates:
- ✅ Parameterized execution with papermill
- ✅ Automated data loading and analysis
- ✅ Visualization generation
- ✅ Summary statistics

**Next Steps**:
1. Replace simulated data with actual data source
2. Add more metrics as needed
3. Schedule automated execution
4. Distribute HTML reports to stakeholders"""
)

# Add all cells to notebook
notebook.cells = [
    metadata_cell,
    parameters_cell,
    setup_cell,
    data_cell,
    analysis_cell,
    viz_cell,
    conclusion_cell,
]

# Write notebook
output_path = Path("notebooks/reporting/example-report.ipynb")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w") as f:
    nbformat.write(notebook, f)

print(f"✓ Created {output_path}")
