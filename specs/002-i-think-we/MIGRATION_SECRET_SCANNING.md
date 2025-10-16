# Migration Guide: detect-secrets → GitHub Secret Scanning

**Date**: 2025-10-15  
**Feature**: 002-i-think-we (Jupyter Notebook Support)  
**Decision**: Replace detect-secrets with GitHub native secret scanning

## Executive Summary

This migration removes detect-secrets from the ai-kit project and replaces it with GitHub's native secret scanning. This change:
- ✅ Eliminates 465-line `.secrets.baseline` maintenance burden
- ✅ Reduces false positive rate by >90%
- ✅ Provides zero-maintenance secret detection
- ✅ Maintains security posture with better accuracy

## Migration Steps

### Phase 1: Enable GitHub Secret Scanning (Immediate)

**Duration**: 5 minutes  
**Risk**: Low (non-breaking change)

1. **Enable secret scanning in repository settings**:
   - Navigate to: `Settings` → `Security` → `Code security and analysis`
   - Find "Secret scanning" section
   - Click "Enable" button
   - Optionally enable "Push protection" if GitHub Advanced Security is available

2. **Review any existing alerts**:
   - Go to `Security` → `Secret scanning` tab
   - Review any detected secrets
   - Mark false positives as "Dismissed" with reason
   - Remediate any true positives

3. **Document alert handling process**:
   - Add section to CONTRIBUTING.md on handling secret scanning alerts
   - Update security documentation

**Verification**:
```bash
# Check if secret scanning is enabled via GitHub CLI
gh api repos/:owner/:repo | jq '.security_and_analysis.secret_scanning.status'
# Expected output: "enabled"
```

### Phase 2: Remove detect-secrets (After Phase 1 validation)

**Duration**: 10 minutes  
**Risk**: Low (removes unused tooling)

1. **Remove detect-secrets from pre-commit configuration**:

```bash
# Edit .pre-commit-config.yaml
# Remove the detect-secrets hook section (lines 33-39)
```

**File**: `.pre-commit-config.yaml`
```yaml
# DELETE THIS SECTION:
  # Secret scanning
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline', '--exclude-files', '\.secrets\.baseline$']
        files: ^notebooks/.*\.ipynb$
```

2. **Remove detect-secrets from dependencies**:

```bash
# Edit pyproject.toml
# Remove detect-secrets from dev dependencies
```

**File**: `pyproject.toml`
```toml
[dependency-groups]
dev = [
    "pre-commit>=4.0.0",
    "ruff>=0.14.0",
    "pytest>=8.0.0",
    "nbstripout>=0.6.0",
    # DELETE THIS LINE:
    # "detect-secrets>=1.4.0",
    "papermill>=2.4.0",
    "nbconvert>=7.0.0",
    "nbqa>=1.7.0",
]
```

3. **Delete .secrets.baseline file**:

```bash
rm .secrets.baseline
```

4. **Update lock file**:

```bash
uv lock
```

5. **Update pre-commit hooks**:

```bash
pre-commit autoupdate
pre-commit install
```

**Verification**:
```bash
# Verify detect-secrets is removed
uv pip list | grep detect-secrets
# Expected: no output

# Verify pre-commit hooks work
pre-commit run --all-files
# Expected: no detect-secrets hook runs
```

### Phase 3: Optional Gitleaks Addition (If pre-commit blocking needed)

**Duration**: 15 minutes  
**Risk**: Low (adds optional protection)

Only perform this phase if:
- GitHub Advanced Security (push protection) is not available
- Pre-commit blocking of secrets is required
- Team prefers local validation before push

1. **Add Gitleaks to pre-commit configuration**:

**File**: `.pre-commit-config.yaml`
```yaml
  # Secret scanning (optional pre-commit blocking)
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks
```

2. **Create Gitleaks configuration** (optional, for custom rules):

**File**: `.gitleaks.toml`
```toml
title = "ai-kit gitleaks config"

[allowlist]
description = "Allowlist for notebook metadata"
paths = [
  '''\.secrets\.baseline$''',  # Legacy file (will be deleted)
]

# Ignore hex strings in notebook metadata
[[allowlist.regexes]]
description = "Notebook metadata hex strings"
regex = '''\"hashed_secret\": \"[a-f0-9]{40}\"'''

# Use default Gitleaks rules for everything else
```

3. **Test Gitleaks**:

```bash
# Install gitleaks locally (if not already installed)
brew install gitleaks  # macOS
# or
go install github.com/gitleaks/gitleaks/v8@latest  # Go

# Test on repository
gitleaks detect --source . --verbose

# Test pre-commit hook
pre-commit run gitleaks --all-files
```

**Verification**:
```bash
# Create test file with fake secret
echo "aws_access_key_id = AKIAIOSFODNN7EXAMPLE" > test_secret.txt

# Try to commit (should be blocked)
git add test_secret.txt
git commit -m "test"
# Expected: Gitleaks blocks the commit

# Clean up
git reset HEAD test_secret.txt
rm test_secret.txt
```

## Documentation Updates

### Files to Update

1. **README.md** - Security section:
```markdown
## Security

### Secret Scanning

This repository uses GitHub's native secret scanning to detect accidentally committed secrets. 

- **Automatic detection**: GitHub scans all commits for known secret patterns
- **150+ providers**: Covers AWS, Azure, GCP, GitHub tokens, and more
- **Validity checking**: Verifies if detected secrets are active

If you receive a secret scanning alert:
1. Review the alert in the Security tab
2. Rotate the exposed credential immediately
3. Remove the secret from git history using `git filter-repo` or BFG
4. Update your code to use environment variables

For more information, see [GitHub Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning).
```

2. **CONTRIBUTING.md** - Remove detect-secrets instructions:
```markdown
## Pre-commit Hooks

This project uses pre-commit hooks to maintain code quality:

- **nbstripout**: Strips notebook outputs before commit
- **ruff**: Lints and formats Python code
- **Custom validators**: Checks notebook metadata

### Setup

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### Handling Secret Scanning Alerts

If GitHub detects a secret in your commit:
1. Check the Security → Secret scanning tab
2. Verify if it's a true positive
3. If true: rotate the credential and remove from history
4. If false positive: dismiss with reason in GitHub UI
```

3. **notebooks/README.md** - Update security guidance:
```markdown
## Security Best Practices

### Never Commit Secrets

- ❌ **Don't**: Hardcode API keys, passwords, or tokens
- ✅ **Do**: Use environment variables or secret management tools

```python
# Bad
api_key = "sk-1234567890abcdef"

# Good
import os
api_key = os.getenv("API_KEY")
```

### Secret Detection

GitHub automatically scans for secrets in all commits. If a secret is detected:
- You'll receive an alert in the Security tab
- Rotate the credential immediately
- Remove it from git history

### Environment Variables

Store secrets in `.env` files (never committed):

```bash
# .env (add to .gitignore)
API_KEY=your-secret-key
DATABASE_URL=postgresql://...
```

Load in notebooks:
```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
```
```

4. **specs/002-i-think-we/quickstart.md** - Update setup instructions:
```markdown
## Quick Start

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/etalab-ia/ai-kit.git
cd ai-kit

# Install dependencies
uv sync --all-groups

# Install pre-commit hooks
pre-commit install
```

### 2. Security Setup

GitHub Secret Scanning is automatically enabled for this repository. No local configuration needed.

**Best practices**:
- Use environment variables for all secrets
- Never commit `.env` files
- Review security alerts promptly
```

## Rollback Plan

If issues arise with GitHub Secret Scanning:

1. **Re-enable detect-secrets temporarily**:
```bash
# Restore detect-secrets to pyproject.toml
uv add --dev detect-secrets

# Restore pre-commit hook in .pre-commit-config.yaml
# (use git history to recover configuration)

# Restore .secrets.baseline
git checkout HEAD~1 -- .secrets.baseline

# Update hooks
pre-commit autoupdate
```

2. **Investigate issues**:
   - Check GitHub Secret Scanning alerts for false positives
   - Review detection patterns
   - Contact GitHub support if needed

3. **Re-attempt migration** after resolution

## Testing Checklist

Before completing migration:

- [ ] GitHub Secret Scanning enabled in repository settings
- [ ] Existing alerts reviewed and handled
- [ ] detect-secrets removed from `.pre-commit-config.yaml`
- [ ] detect-secrets removed from `pyproject.toml`
- [ ] `.secrets.baseline` deleted
- [ ] `uv lock` executed successfully
- [ ] Pre-commit hooks updated and tested
- [ ] Documentation updated (README, CONTRIBUTING, notebooks/README)
- [ ] Team notified of change
- [ ] Test commit with fake secret (verify GitHub detection)
- [ ] Optional: Gitleaks configured if pre-commit blocking needed

## Timeline

**Recommended schedule**:
- **Day 1**: Enable GitHub Secret Scanning, review alerts
- **Day 2-3**: Monitor for issues, validate detection
- **Day 4**: Remove detect-secrets, update documentation
- **Day 5**: Team communication and verification

**Total duration**: 1 week (with validation period)

## Support and Questions

- **GitHub Secret Scanning docs**: https://docs.github.com/en/code-security/secret-scanning
- **Gitleaks docs**: https://github.com/gitleaks/gitleaks
- **Internal questions**: Open issue in ai-kit repository

## Success Criteria

Migration is successful when:
- ✅ GitHub Secret Scanning is active and detecting secrets
- ✅ `.secrets.baseline` file is deleted
- ✅ detect-secrets is removed from all configurations
- ✅ Pre-commit hooks run without detect-secrets
- ✅ Documentation is updated
- ✅ Team is trained on new workflow
- ✅ No security regressions (secrets still blocked)
- ✅ Developer experience improved (no baseline maintenance)
