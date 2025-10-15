# Secret Scanning Research: Alternatives to detect-secrets

**Date**: 2025-10-15  
**Context**: Feature 002 (Jupyter Notebook Support) - Replacing detect-secrets with more effective solution

## Problem Statement

The current implementation uses `detect-secrets` for secret scanning in notebooks, which has several limitations:

### Issues with detect-secrets

1. **High False Positive Rate**: The `.secrets.baseline` file contains 465 lines with 50+ flagged "secrets" across notebook files, most of which are false positives (hex strings from notebook metadata, not actual secrets)
2. **Maintenance Burden**: Requires manual baseline file management and updates whenever legitimate high-entropy strings are added
3. **Poor Developer Experience**: Developers must constantly update baseline file, creating friction in the workflow
4. **Limited Context Awareness**: Cannot distinguish between actual secrets and legitimate high-entropy data (model IDs, hashes, etc.)
5. **Notebook-Specific Issues**: Jupyter notebooks contain many hex strings in metadata that trigger false positives

## Alternative Solutions

### Option 1: GitHub Native Secret Scanning (Recommended)

**Overview**: GitHub provides free secret scanning for all public repositories with push protection available for GitHub Advanced Security customers.

**Advantages**:
- ✅ **Zero maintenance**: No baseline files to manage
- ✅ **High accuracy**: Partners with 150+ providers for pattern detection
- ✅ **Free for public repos**: Secret scanning alerts available at no cost
- ✅ **Validity checking**: Verifies if detected secrets are actually valid/active
- ✅ **No local setup**: Works automatically in GitHub without pre-commit hooks
- ✅ **Better UX**: Clear alerts in GitHub UI with remediation guidance
- ✅ **Continuous monitoring**: Scans entire git history when new patterns are added

**Limitations**:
- ⚠️ **Push protection requires GitHub Advanced Security**: Free tier only provides alerts after push
- ⚠️ **Cloud-only**: Requires GitHub hosting (not an issue for this project)
- ⚠️ **Limited customization**: Cannot add custom patterns easily

**Implementation**:
1. Enable secret scanning in repository settings (Settings → Code security and analysis → Secret scanning → Enable)
2. Remove detect-secrets from pre-commit hooks and dependencies
3. Delete `.secrets.baseline` file
4. Add documentation on how to handle secret scanning alerts
5. Optional: Enable push protection if GitHub Advanced Security is available

**Cost**: Free for public repositories

### Option 2: Gitleaks (Open Source Alternative)

**Overview**: Fast, open-source secret scanner with low false positive rate and active maintenance.

**Advantages**:
- ✅ **Low false positives**: More accurate than detect-secrets
- ✅ **Fast performance**: Written in Go, very efficient
- ✅ **Active maintenance**: Regularly updated with new patterns
- ✅ **Pre-commit integration**: Can block commits locally
- ✅ **Customizable**: Easy to add custom patterns and allowlists
- ✅ **No baseline file**: Uses configuration file instead

**Limitations**:
- ⚠️ **Requires local installation**: Each developer needs gitleaks installed
- ⚠️ **Manual pattern updates**: Need to update tool for new secret types
- ⚠️ **No validity checking**: Cannot verify if secrets are active

**Implementation**:
```yaml
# .pre-commit-config.yaml
- repo: https://github.com/gitleaks/gitleaks
  rev: v8.18.0
  hooks:
    - id: gitleaks
```

**Cost**: Free (open source)

### Option 3: TruffleHog (Enterprise-Grade Alternative)

**Overview**: Comprehensive secret scanner with verification capabilities and multi-environment scanning.

**Advantages**:
- ✅ **Secret verification**: Checks if detected secrets are valid/active
- ✅ **Low false positives**: Advanced detection algorithms
- ✅ **Multi-environment**: Can scan S3, Docker images, etc.
- ✅ **Active maintenance**: Well-supported open source project

**Limitations**:
- ⚠️ **Slower than Gitleaks**: More comprehensive but less performant
- ⚠️ **More complex setup**: Additional configuration required
- ⚠️ **Overkill for notebooks**: Advanced features not needed for this use case

**Cost**: Free (open source), paid enterprise version available

### Option 4: Hybrid Approach (GitHub + Gitleaks)

**Overview**: Use GitHub secret scanning for continuous monitoring + Gitleaks for pre-commit blocking.

**Advantages**:
- ✅ **Defense in depth**: Multiple layers of protection
- ✅ **Pre-commit blocking**: Gitleaks prevents commits with secrets
- ✅ **Continuous monitoring**: GitHub scans entire history
- ✅ **Best of both worlds**: Local and remote protection

**Limitations**:
- ⚠️ **Dual maintenance**: Need to manage both tools
- ⚠️ **Potential conflicts**: Different tools may flag different patterns

## Comparison Matrix

| Feature | detect-secrets | GitHub Scanning | Gitleaks | TruffleHog |
|---------|---------------|-----------------|----------|------------|
| False Positives | High | Low | Low | Very Low |
| Maintenance | High | None | Low | Medium |
| Pre-commit Block | Yes | No (paid tier) | Yes | Yes |
| Validity Check | No | Yes | No | Yes |
| Setup Complexity | Low | None | Low | Medium |
| Performance | Fast | N/A | Very Fast | Medium |
| Cost | Free | Free (public) | Free | Free |
| Notebook Support | Poor | Good | Good | Good |

## Recommendation

**Primary Recommendation: GitHub Native Secret Scanning**

For the ai-kit project, GitHub native secret scanning is the optimal solution because:

1. **Zero Maintenance**: Eliminates the 465-line `.secrets.baseline` file and all associated maintenance
2. **Better Accuracy**: Reduces false positives from notebook metadata
3. **Free for Public Repos**: No cost for the current use case
4. **Sovereign Compatibility**: GitHub is already in use; no additional external dependencies
5. **Developer Experience**: Alerts are clear and actionable in GitHub UI

**Fallback Option: Gitleaks for Pre-commit Blocking**

If pre-commit blocking is required (before GitHub Advanced Security is available):
- Add Gitleaks as a pre-commit hook for local blocking
- Keep GitHub secret scanning for continuous monitoring
- Configure Gitleaks to ignore notebook metadata patterns

## Migration Strategy

### Phase 1: Enable GitHub Secret Scanning (Immediate)
1. Enable secret scanning in repository settings
2. Review any existing alerts
3. Document alert handling process

### Phase 2: Remove detect-secrets (After validation)
1. Remove detect-secrets from `.pre-commit-config.yaml`
2. Remove detect-secrets from `pyproject.toml` dependencies
3. Delete `.secrets.baseline` file
4. Update documentation to reference GitHub secret scanning

### Phase 3: Optional Gitleaks Addition (If needed)
1. Add Gitleaks pre-commit hook if local blocking is required
2. Configure allowlist for notebook metadata patterns
3. Test with existing notebooks

## Configuration Examples

### GitHub Secret Scanning Setup

No configuration file needed. Enable via:
1. Repository Settings → Security → Code security and analysis
2. Click "Enable" next to "Secret scanning"
3. Optionally enable "Push protection" if GitHub Advanced Security is available

### Gitleaks Configuration (if needed)

```toml
# .gitleaks.toml
title = "ai-kit gitleaks config"

[allowlist]
description = "Allowlist for notebook metadata"
paths = [
  '''\.secrets\.baseline$''',
]

# Ignore hex strings in notebook metadata
[[allowlist.regexes]]
description = "Notebook metadata hex strings"
regex = '''\"hashed_secret\": \"[a-f0-9]{40}\"'''

[[rules]]
id = "generic-api-key"
description = "Generic API Key"
regex = '''(?i)(api[_-]?key|apikey)['\"]?\s*[:=]\s*['\"]?([a-z0-9_\-]{32,})'''
```

## Documentation Updates Required

1. **README.md**: Update security section to reference GitHub secret scanning
2. **CONTRIBUTING.md**: Remove detect-secrets instructions, add GitHub alert handling
3. **notebooks/README.md**: Update security guidance for notebook authors
4. **specs/002-i-think-we/quickstart.md**: Update developer setup instructions

## Success Criteria

- ✅ Zero `.secrets.baseline` maintenance overhead
- ✅ Reduced false positive rate by >90%
- ✅ Faster developer workflow (no baseline updates)
- ✅ Maintained or improved security posture
- ✅ Clear documentation for handling secret alerts

## References

- [GitHub Secret Scanning Documentation](https://docs.github.com/en/code-security/secret-scanning)
- [Gitleaks GitHub Repository](https://github.com/gitleaks/gitleaks)
- [TruffleHog vs Gitleaks Comparison](https://www.jit.io/resources/appsec-tools/trufflehog-vs-gitleaks-a-detailed-comparison-of-secret-scanning-tools)
- [GitHub Secret Scanning for Public Repos Announcement](https://github.blog/news-insights/product-news/secret-scanning-alerts-are-now-available-and-free-for-all-public-repositories/)
