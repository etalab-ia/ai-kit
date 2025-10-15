# Manual Testing Checklist: Jupyter Notebook Support

**Feature**: Jupyter Notebook Support (MVP)  
**Branch**: `002-i-think-we`  
**Date**: 2025-10-15

## Purpose

This checklist should be completed during PR review to verify the notebook functionality works end-to-end with real notebooks and git operations.

## Prerequisites

- [ ] Branch `002-i-think-we` checked out
- [ ] Dependencies synced: `just sync`
- [ ] Pre-commit hooks installed: `pre-commit install`

## Test 1: Create Exploratory Notebook

**Goal**: Verify interactive notebook creation works

```bash
just notebook create
```

**Steps**:
1. Select category: `1` (Exploratory)
2. Enter name: `test-exploratory`
3. Enter purpose: `Testing notebook creation workflow for PR review`
4. Confirm author name
5. Confirm creation

**Expected**:
- [ ] Notebook created at `notebooks/exploratory/test-exploratory.ipynb`
- [ ] First cell contains proper metadata
- [ ] Success message displayed with next steps

## Test 2: Verify Pre-commit Hooks

**Goal**: Verify security hooks work correctly

### 2a. Test Output Stripping

**Steps**:
1. Open the notebook: `jupyter lab notebooks/exploratory/test-exploratory.ipynb`
2. Add a code cell with: `print("Hello, world!")`
3. Execute the cell (generates output)
4. Save the notebook
5. Commit: `git add notebooks/exploratory/test-exploratory.ipynb && git commit -m "test: add exploratory notebook"`

**Expected**:
- [ ] `nbstripout` hook runs
- [ ] Commit succeeds
- [ ] Check committed file has no outputs: `git show HEAD:notebooks/exploratory/test-exploratory.ipynb | grep -c '"outputs"'` (should be 0 or minimal)

### 2b. Test Credential Blocking

**Steps**:
1. Open the notebook again
2. Add a cell with: `api_key = "sk-test-abc123def456ghi789"`
3. Save the notebook
4. Try to commit: `git add notebooks/exploratory/test-exploratory.ipynb && git commit -m "test: add credential"`

**Expected**:
- [ ] `detect-secrets` hook runs
- [ ] Commit **fails** with error about potential secrets
- [ ] Error message suggests using environment variables

**Cleanup**:
```bash
git restore notebooks/exploratory/test-exploratory.ipynb
```

### 2c. Test Metadata Validation

**Steps**:
1. Open the notebook
2. Delete the `**Purpose**:` line from the first cell
3. Save the notebook
4. Try to commit: `git add notebooks/exploratory/test-exploratory.ipynb && git commit -m "test: missing metadata"`

**Expected**:
- [ ] `notebook-metadata-validation` hook runs
- [ ] Commit **fails** with error about missing 'purpose' field
- [ ] Error message shows how to fix

**Cleanup**:
```bash
git restore notebooks/exploratory/test-exploratory.ipynb
```

### 2d. Test Size Checking

**Steps**:
1. Create a large test file: `dd if=/dev/zero of=/tmp/large.txt bs=1m count=11`
2. Open the notebook
3. Add a cell that reads the large file (or just note the size check works)
4. For this test, we'll skip actually creating a 10MB+ notebook

**Expected**:
- [ ] Size check hook is configured in `.pre-commit-config.yaml`
- [ ] Hook would block files > 10 MB

**Note**: Skip actual test to avoid creating large files in repo

## Test 3: List and Validate Commands

**Goal**: Verify CLI commands work

### 3a. List Notebooks

```bash
just notebook list
```

**Expected**:
- [ ] Shows `EXPLORATORY:` section
- [ ] Lists `test-exploratory.ipynb`

### 3b. Show Statistics

```bash
just notebook stats
```

**Expected**:
- [ ] Shows count for each category
- [ ] `exploratory: 1`
- [ ] `Total: 1 notebooks`

### 3c. Validate Notebook

```bash
just notebook validate notebooks/exploratory/test-exploratory.ipynb
```

**Expected**:
- [ ] Validation passes
- [ ] Success message displayed

## Test 4: Create Notebooks in Other Categories

**Goal**: Verify templates work for all categories

### 4a. Tutorial Notebook

```bash
just notebook create
```

- Select: `2` (Tutorials)
- Name: `test-tutorial`
- Purpose: `Testing tutorial template`

**Expected**:
- [ ] Created in `notebooks/tutorials/`
- [ ] Template has tutorial-specific structure

### 4b. Evaluation Notebook

```bash
just notebook create
```

- Select: `3` (Evaluations)
- Name: `test-evaluation`
- Purpose: `Testing evaluation template`
- Model version: `test-model-v1.0`
- Baseline: `previous-model`

**Expected**:
- [ ] Created in `notebooks/evaluations/`
- [ ] Template has evaluation-specific sections
- [ ] Additional metadata fields present

### 4c. Compliance Notebook

```bash
just notebook create
```

- Select: `4` (Compliance)
- Name: `test-compliance`
- Purpose: `Testing compliance template`
- Regulatory framework: `EU AI Act`
- Risk level: `high`

**Expected**:
- [ ] Created in `notebooks/compliance/`
- [ ] Template has EU AI Act checklist
- [ ] Compliance-specific sections present

### 4d. Reporting Notebook

```bash
just notebook create
```

- Select: `5` (Reporting)
- Name: `test-reporting`
- Purpose: `Testing reporting template`
- Schedule: `weekly`
- Parameters: `start_date,end_date`

**Expected**:
- [ ] Created in `notebooks/reporting/`
- [ ] Template has papermill parameters section
- [ ] Reporting-specific structure

## Test 5: Delete Notebook

**Goal**: Verify safe deletion works

```bash
just notebook delete notebooks/exploratory/test-exploratory.ipynb
```

**Expected**:
- [ ] Confirmation prompt appears
- [ ] After confirming, notebook is deleted
- [ ] Success message mentions git history preservation

## Test 6: Generic CLI Command

**Goal**: Verify `just cli` works

```bash
just cli --help
just cli notebook --help
just cli notebook list
```

**Expected**:
- [ ] All commands work
- [ ] Same output as `just notebook` commands

## Test 7: Documentation Review

**Goal**: Verify documentation is accurate and helpful

- [ ] Read `notebooks/README.md` - clear and accurate
- [ ] Read `docs/notebooks/governance.md` - comprehensive
- [ ] Read `docs/notebooks/compliance-officer-guide.md` - clear for target audience
- [ ] Read `docs/notebooks/migration-guide.md` - helpful examples
- [ ] Check root `README.md` - notebook section accurate

## Cleanup

After testing, clean up test notebooks:

```bash
git rm notebooks/exploratory/test-exploratory.ipynb
git rm notebooks/tutorials/test-tutorial.ipynb
git rm notebooks/evaluations/test-evaluation.ipynb
git rm notebooks/compliance/test-compliance.ipynb
git rm notebooks/reporting/test-reporting.ipynb
git commit -m "test: remove test notebooks after manual testing"
```

## Summary

- [ ] All tests passed
- [ ] No issues found
- [ ] Ready to merge

**Tested by**: _______________  
**Date**: _______________  
**Notes**: _______________
