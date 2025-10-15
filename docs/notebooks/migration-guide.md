# Notebook-to-Production Migration Guide

**Last Updated**: 2025-10-15

## Overview

This guide describes patterns for migrating validated notebook code to production packages in the ai-kit monorepo.

## Migration Philosophy

Notebooks are for **exploration and validation**. Production code requires:
- Proper testing
- Error handling
- Documentation
- Maintainability
- Performance optimization

## Migration Workflow

### 1. Validate in Notebook

Before migration, ensure:
- [ ] Code works correctly
- [ ] Results are reproducible
- [ ] Approach is validated
- [ ] Edge cases identified

### 2. Extract Core Logic

Identify reusable components:
- Functions that process data
- Model inference logic
- Utility functions
- Configuration patterns

### 3. Create Production Package

```bash
# Create package structure
mkdir -p packages/my-feature/src/my_feature
mkdir -p packages/my-feature/tests

# Create package files
touch packages/my-feature/pyproject.toml
touch packages/my-feature/README.md
touch packages/my-feature/src/my_feature/__init__.py
```

### 4. Implement with Best Practices

**Notebook code** (exploratory):
```python
# Quick and dirty exploration
df = pd.read_csv('data.csv')
result = df[df['value'] > 10].groupby('category').mean()
print(result)
```

**Production code** (robust):
```python
from pathlib import Path
from typing import Optional
import pandas as pd

def analyze_categories(
    data_path: Path,
    threshold: float = 10.0,
    category_col: str = "category",
    value_col: str = "value"
) -> pd.DataFrame:
    """
    Analyze categories above threshold.
    
    Args:
        data_path: Path to CSV data file
        threshold: Minimum value threshold
        category_col: Name of category column
        value_col: Name of value column
        
    Returns:
        DataFrame with mean values by category
        
    Raises:
        FileNotFoundError: If data file doesn't exist
        ValueError: If required columns missing
    """
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found: {data_path}")
    
    df = pd.read_csv(data_path)
    
    required_cols = {category_col, value_col}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_cols - set(df.columns)}")
    
    filtered = df[df[value_col] > threshold]
    result = filtered.groupby(category_col)[value_col].mean()
    
    return result.to_frame(name=f"mean_{value_col}")
```

### 5. Add Tests

```python
# packages/my-feature/tests/test_analysis.py
import pytest
import pandas as pd
from pathlib import Path
from my_feature.analysis import analyze_categories

def test_analyze_categories_basic(tmp_path):
    """Test basic category analysis."""
    # Create test data
    data_path = tmp_path / "test.csv"
    df = pd.DataFrame({
        "category": ["A", "A", "B", "B"],
        "value": [5, 15, 8, 20]
    })
    df.to_csv(data_path, index=False)
    
    # Run analysis
    result = analyze_categories(data_path, threshold=10.0)
    
    # Verify results
    assert len(result) == 2
    assert result.loc["A", "mean_value"] == 15.0
    assert result.loc["B", "mean_value"] == 20.0

def test_analyze_categories_missing_file():
    """Test error handling for missing file."""
    with pytest.raises(FileNotFoundError):
        analyze_categories(Path("nonexistent.csv"))

def test_analyze_categories_missing_columns(tmp_path):
    """Test error handling for missing columns."""
    data_path = tmp_path / "test.csv"
    df = pd.DataFrame({"wrong_col": [1, 2, 3]})
    df.to_csv(data_path, index=False)
    
    with pytest.raises(ValueError, match="Missing required columns"):
        analyze_categories(data_path)
```

### 6. Document Migration

In feature spec or plan.md:

```markdown
## Implementation Notes

Insights from exploratory notebook `notebooks/exploratory/customer-analysis.ipynb`
(commit SHA: abc123def456) were migrated to `packages/customer-analysis/`.

### Key Findings from Notebook
- K-means clustering with k=5 provided best silhouette score (0.72)
- Feature scaling critical for performance
- PCA reduced dimensions from 20 to 5 without significant information loss

### Production Implementation
- Extracted clustering logic to `customer_analysis.cluster`
- Added configuration for k parameter
- Implemented error handling for edge cases
- Added comprehensive test suite (95% coverage)

### Migration Date
2024-10-15

### Notebook Deletion
Exploratory notebook deleted after migration (git history preserves at commit abc123def456)
```

### 7. Delete Exploratory Notebook

```bash
# Capture commit SHA first
git log -1 --format="%H" notebooks/exploratory/customer-analysis.ipynb

# Delete notebook
git rm notebooks/exploratory/customer-analysis.ipynb
git commit -m "Migrate customer analysis to production

Insights from notebooks/exploratory/customer-analysis.ipynb migrated to
packages/customer-analysis/. See packages/customer-analysis/README.md
for details.

Original notebook preserved in git history at commit abc123def456"
```

## Migration Patterns

### Pattern 1: Data Processing Pipeline

**Notebook exploration**:
```python
# Exploratory data cleaning
df = pd.read_csv('raw_data.csv')
df = df.dropna()
df['date'] = pd.to_datetime(df['date'])
df = df[df['value'] > 0]
```

**Production package**:
```python
# packages/data-pipeline/src/data_pipeline/cleaning.py
from typing import List
import pandas as pd

class DataCleaner:
    """Clean and validate raw data."""
    
    def __init__(self, required_columns: List[str]):
        self.required_columns = required_columns
    
    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean dataframe with validation."""
        self._validate_columns(df)
        df = self._remove_nulls(df)
        df = self._parse_dates(df)
        df = self._filter_positive_values(df)
        return df
    
    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing = set(self.required_columns) - set(df.columns)
        if missing:
            raise ValueError(f"Missing columns: {missing}")
    
    # ... additional methods
```

### Pattern 2: Model Inference

**Notebook exploration**:
```python
# Quick model testing
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)
result = response.choices[0].message.content
```

**Production package**:
```python
# packages/llm-client/src/llm_client/inference.py
from typing import List, Dict, Optional
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

class LLMClient:
    """Production LLM client with error handling and logging."""
    
    def __init__(self, api_key: str, model: str = "gpt-4", timeout: int = 30):
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.timeout = timeout
    
    def generate(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate completion with error handling.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
            
        Raises:
            ValueError: If messages format invalid
            TimeoutError: If request times out
            APIError: If API returns error
        """
        self._validate_messages(messages)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                timeout=self.timeout
            )
            
            result = response.choices[0].message.content
            logger.info(f"Generated {len(result)} characters")
            return result
            
        except TimeoutError as e:
            logger.error(f"Request timeout: {e}")
            raise
        except Exception as e:
            logger.error(f"API error: {e}")
            raise
    
    def _validate_messages(self, messages: List[Dict[str, str]]) -> None:
        """Validate message format."""
        if not messages:
            raise ValueError("Messages cannot be empty")
        
        for msg in messages:
            if "role" not in msg or "content" not in msg:
                raise ValueError("Each message must have 'role' and 'content'")
```

### Pattern 3: Configuration Management

**Notebook exploration**:
```python
# Hardcoded config
MODEL = "gpt-4"
TEMPERATURE = 0.7
MAX_TOKENS = 1000
```

**Production package**:
```python
# packages/config/src/config/llm.py
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMConfig:
    """LLM configuration."""
    model: str = "gpt-4"
    temperature: float = 0.7
    max_tokens: Optional[int] = 1000
    timeout: int = 30
    
    def __post_init__(self):
        """Validate configuration."""
        if not 0 <= self.temperature <= 2:
            raise ValueError("Temperature must be between 0 and 2")
        if self.max_tokens is not None and self.max_tokens < 1:
            raise ValueError("max_tokens must be positive")
        if self.timeout < 1:
            raise ValueError("timeout must be positive")

# Load from environment or config file
def load_config() -> LLMConfig:
    """Load configuration from environment."""
    import os
    return LLMConfig(
        model=os.getenv("LLM_MODEL", "gpt-4"),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "1000")),
    )
```

## Edge Cases and Considerations

### Notebook-Specific Code

Some notebook code should **not** be migrated:

- Visualization for exploration (use proper viz library in production)
- Interactive widgets (not needed in production)
- Print statements for debugging (use logging instead)
- Inline data (externalize to files)

### When NOT to Migrate

Keep in notebook if:
- One-time analysis (not reusable)
- Highly experimental (not validated)
- Visualization-focused (for reports)
- Tutorial/documentation (teaching tool)

### Gradual Migration

For large notebooks:

1. **Phase 1**: Extract core utilities
2. **Phase 2**: Extract data processing
3. **Phase 3**: Extract model logic
4. **Phase 4**: Delete notebook

Each phase can be a separate PR.

## Checklist

Before deleting exploratory notebook:

- [ ] Core logic extracted to package
- [ ] Tests added (>80% coverage recommended)
- [ ] Documentation written
- [ ] Migration documented in spec/plan
- [ ] Commit SHA captured
- [ ] Package integrated into monorepo
- [ ] CI/CD passing

## Questions?

- **Migration strategy**: Consult with team lead
- **Testing requirements**: See testing guidelines
- **Package structure**: Follow monorepo conventions
- **Documentation**: Use docstring standards
