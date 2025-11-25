# Product Requirements Document (PRD)
## Git Commit & PR Automation Agent

**Version:** 1.0 (1-Day MVP)  
**Focus:** 100% implementable today, no future features

***

## 1. Product Overview

### 1.1 Product Name
**ai code inspector** - AI Git Assistant

### 1.2 Core Value
Transform `git diff` into production-ready commits and PRs. **Auto-approves PRs** that meet quality standards, flags issues for human review when they don't.

### 1.3 Problem Solved
- Developers waste 5-10 min per commit writing messages
- PR descriptions lack context, slowing reviews by 20+ min
- **Manual PR approval bottleneck** - even simple PRs wait hours for review
- Inconsistent commit standards across teams

***

## 2. Target User
**Primary:** Solo developers and 2-5 person teams who want to ship faster without sacrificing quality.

***

## 3. Core Features (MUST-BUILD TODAY)

### 3.1 Feature 1: Conventional Commit Generator
**What it does:** Reads staged changes, outputs commit message in standard format.

**Input:** `git diff --staged`  
**Output:** 
```
feat(auth): add JWT validation

- Validates token format
- Returns False for empty tokens
- Uses SECRET_KEY from config
```

**Success Criteria:**
- ✅ Runs in <5 seconds
- ✅ 90% of messages accepted without edit
- ✅ Handles Python, JavaScript, Go, Rust

***

### 3.2 Feature 2: PR Description Generator
**What it does:** Analyzes branch commits, generates comprehensive PR description.

**Input:** `git log main..feature-branch` + file changes  
**Output:** Markdown with:
- Summary
- Changes list
- Files categorized (Backend/Frontend/Tests)
- Testing checklist
- Breaking change warnings

**Example:**
```markdown
## Summary
Add JWT token validation to auth module

## Changes
- Implement token validation function
- Add error handling for expired tokens
- Update middleware to use new validation

## Files
**Backend:**
- src/auth.py (+45 lines)

**Tests:**
- tests/test_auth.py (+30 lines)

## Testing Checklist
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual token validation tested

## Breaking Changes
None
```

***

### 3.3 Feature 3: PR Quality Analyzer & Auto-Approver
**What it does:** Submits PR to GitHub, analyzes code quality, **auto-approves if all criteria pass**.

**Flow:**
1. User runs: `codeinspector pr --auto`
2. Tool pushes branch, creates PR
3. Agent analyzes PR against quality checklist
4. **If approved:** Comments "✅ Auto-approved: All quality checks passed"
5. **If rejected:** Comments specific issues for human review

**Approval Criteria (ALL must pass):**
- ✅ All unit tests pass
- ✅ No hardcoded secrets (regex scan)
- ✅ Code follows conventions (linting)
- ✅ PR description complete
- ✅ <500 lines changed (configurable)
- ✅ No TODO/FIXME comments
- ✅ Test coverage maintained

**Rejection Example:**
```
🤖 Code Review Results:

❌ ISSUES FOUND:
- Test coverage dropped from 85% to 82%
- 2 TODO comments in src/auth.py (lines 45, 67)
- Missing error handling for network timeout

🔧 Please fix these issues before merge.

✅ PASSED CHECKS:
- No secrets detected
- Code style compliant
- PR description complete
```

***

### 3.4 Feature 4: CLI Tool
**Commands:**
```bash
# Generate commit message
codeinspector commit

# Generate + commit
codeinspector commit --yes

# Create PR
codeinspector pr --title "Add auth feature"

# Create PR + auto-approve if quality passes
codeinspector pr --auto

# Preview without actions
codeinspector preview
```

***

## 4. Technical Implementation (Build TODAY)

### 4.1 Tech Stack
- **Python 3.9+**
- **Google ADK** (agent orchestration)
- **Gemini 2.0 Flash** (fast, cheap)
- **GitPython** (git operations)
- **PyGithub** (GitHub API)
- **Click** (CLI framework)

### 4.2 Architecture

```
┌─────────────┐
│   CLI Tool  │
└──────┬──────┘
       │
       ├─→ GitPython (read diff)
       │
       └─→ Google ADK Agent
            │
            ├─→ CommitGenerator (conventional commits)
            │
            ├─→ PRDescriber (markdown generation)
            │
            └─→ QualityAnalyzer (approval logic)
                 │
                 ├─→ ✅ Pass → PyGithub → Auto-approve
                 │
                 └─→ ❌ Fail → Comment issues
```

### 4.3 ADK Agent Design

**Agent 1: CommitGenerator**
```python
# System prompt includes Conventional Commits spec
# Input: git diff
# Output: formatted commit message
```

**Agent 2: PRDescriber**
```python
# Input: git log + file changes
# Output: structured markdown
# Includes: summary, changes, files, testing checklist
```

**Agent 3: QualityAnalyzer**
```python
# Input: PR data (diff, tests, lint results)
# Output: PASS/FAIL with reasons
# Tools:
# - test_runner (runs pytest/jest)
# - secret_scanner (regex for keys)
# - coverage_checker (coverage delta)
# - lint_checker (runs flake8/eslint)
```

***

## 5. Build Timeline (8 Hours)

### Hour 1-2: Setup & Core Agent
```bash
pip install google-adk gitpython click pygithub
mkdir codeinspector && cd codeinspector
adk init .
# Create basic agent structure
```

**Deliverable:** ADK agent responds to prompts

### Hour 3-4: Git Integration
```python
# git_handler.py
class GitHandler:
    def get_staged_diff(self) -> str
    def get_commit_history(self) -> list
    def push_branch(self) -> bool
```

**Deliverable:** Can read git data

### Hour 5-6: Commit & PR Generation
```python
# agents.py
class CommitGenerator(Agent)
class PRDescriber(Agent)

# Generate messages from real diffs
```

**Deliverable:** Working message generation

### Hour 7-8: Quality Analyzer & GitHub Integration
```python
# quality_checker.py
def check_tests() -> bool
def check_secrets() -> bool
def check_coverage() -> bool

# GitHub integration
def create_pr() -> PR
def auto_approve(pr) -> bool
```

**Deliverable:** Full workflow working

***

## 6. User Experience Flow

### 6.1 Commit Flow
```bash
$ git add .
$ codeinspector commit

🤖 Analyzing changes...
✅ Generated:

feat(auth): add JWT token validation

- Validates token format
- Returns False for empty tokens
- Uses SECRET_KEY from config

Accept? (y/n/e) > y
✅ Committed: 3a4f5b2
```

### 6.2 PR Flow (Auto-Approve)
```bash
$ codeinspector pr --auto

🤖 Creating PR...
✅ PR #42 created: https://github.com/user/repo/pull/42

🤖 Running quality checks...
✅ Tests pass (45/45)
✅ No secrets found
✅ Coverage: 87% (no drop)
✅ Lint: 0 errors
✅ <500 lines changed

🤖 Auto-approving...
✅ PR #42 approved!
✅ Ready to merge
```

### 6.3 PR Flow (Rejected)
```bash
$ codeinspector pr --auto

🤖 Creating PR...
✅ PR #43 created

🤖 Running quality checks...
❌ Tests: 1 failed (test_auth.py::test_token_expiry)
❌ Coverage: Dropped 85% → 82%
❌ TODOs: 2 found in auth.py

💬 Commented issues on PR #43
🔧 Fix issues and re-run
```

***

## 7. Quality Checklist Implementation

### 7.1 Automated Checks (Code)

```python
# quality_checker.py
class QualityChecker:
    def check_tests(self) -> tuple[bool, str]:
        # Run pytest or jest
        # Return (passed, message)
        pass
    
    def check_secrets(self) -> tuple[bool, str]:
        # Regex scan for:
        # - API keys (sk-*, ak_*)
        # - Passwords
        # - Private keys
        pass
    
    def check_coverage(self) -> tuple[bool, str]:
        # Compare current coverage to main branch
        # Fail if dropped >2%
        pass
    
    def check_lint(self) -> tuple[bool, str]:
        # Run flake8 (Python) or eslint (JS)
        # Fail if any errors
        pass
    
    def check_pr_size(self) -> tuple[bool, str]:
        # Count lines changed
        # Fail if >500 (configurable)
        pass
    
    def check_todos(self) -> tuple[bool, str]:
        # Scan for TODO/FIXME comments
        # Fail if found
        pass
```

### 7.2 Approval Decision Logic

```python
def should_approve(pr_data: dict) -> tuple[bool, list[str]]:
    checks = [
        check_tests(),
        check_secrets(),
        check_coverage(),
        check_lint(),
        check_pr_size(),
        check_todos()
    ]
    
    passed = all(check[0] for check in checks)
    issues = [check[1] for check in checks if not check[0]]
    
    return passed, issues
```

***

## 8. GitHub Integration

### 8.1 GitHub API Setup
```python
# github_client.py
from github import Github

class GitHubClient:
    def __init__(self, token: str):
        self.g = Github(token)
    
    def create_pr(self, repo: str, title: str, body: str, 
                  head: str, base: str = "main") -> PullRequest:
        # Create PR
        pass
    
    def approve_pr(self, pr: PullRequest, message: str):
        # Submit approval review
        pr.create_review(
            body=message,
            event="APPROVE"
        )
    
    def comment_on_pr(self, pr: PullRequest, comment: str):
        # Comment issues
        pr.create_issue_comment(comment)
```

### 8.2 Auto-Approval Message
```python
APPROVAL_MESSAGE = """
🤖 Auto-Approved by codeinspector

✅ All quality checks passed:
- Tests: {test_status}
- Coverage: {coverage_status}
- Lint: {lint_status}
- Secrets: {secrets_status}
- Size: {size_status}

This PR meets our quality standards and is ready to merge.
"""

REJECTION_MESSAGE = """
🤖 Code Review Results

❌ ISSUES FOUND:
{issues_list}

🔧 Please address these issues before merge.

✅ PASSED CHECKS:
{passed_list}
"""
```

***

## 9. CLI Interface

### 9.1 Commands
```python
# cli.py
import click

@click.group()
def codeinspector():
    """AI Git Assistant"""

@codeinspector.command()
@click.option('--yes', is_flag=True, help='Commit without confirmation')
def commit(yes):
    """Generate and create commit"""
    # Implementation here

@codeinspector.command()
@click.option('--title', required=True, help='PR title')
@click.option('--auto', is_flag=True, help='Auto-approve if quality passes')
def pr(title, auto):
    """Create PR and optionally auto-approve"""
    # Implementation here

@codeinspector.command()
def preview():
    """Preview changes without actions"""
    # Show what would be generated
```

### 9.2 Configuration
```python
# ~/.codeinspector/config.json
{
    "github_token": "ghp_xxx",
    "llm_model": "gemini-2.0-flash",
    "max_pr_lines": 500,
    "coverage_threshold": 80,
    "lint_strict": true,
    "auto_approve": true
}
```

***

## 10. Error Handling

### 10.1 User Errors
```bash
# No staged changes
$ codeinspector commit
❌ No staged changes. Run 'git add' first.

# Not git repo
$ codeinspector commit
❌ Not a git repository

# No GitHub token
$ codeinspector pr
❌ GitHub token not found. Run: codeinspector config --token <your-token>
```

### 10.2 System Errors
```python
# LLM fails
except Exception as e:
    click.echo("⚠️ Generation failed. Using template.")
    return DEFAULT_TEMPLATE

# GitHub API fails
except GithubException as e:
    click.echo(f"❌ GitHub error: {e}")
    return False
```

***

## 11. Testing (Today)

### 11.1 Test Cases to Run
```bash
# Create test repo
git init test-repo
cd test-repo

# Test 1: Simple feature
echo "def add(a, b): return a + b" > math.py
git add math.py
codeinspector commit --yes
# Expected: feat: add add function

# Test 2: Bug fix
echo "def divide(a, b): return a / b" >> math.py
git add math.py
codeinspector commit --yes
# Expected: fix: add division function

# Test 3: Create PR
git checkout -b feature/test
# ... make changes ...
codeinspector pr --title "Test feature" --auto
# Expected: PR created, quality checks run
```

***

## 12. Launch Checklist (Today)

- [ ] Code committed to GitHub
- [ ] README with installation instructions
- [ ] Demo video (1 minute screen recording)
- [ ] Tweet with demo
- [ ] Post on r/programming
- [ ] Share with 5 developer friends

***

## 13. Success Metrics (End of Day)

- [ ] Tool works on 3+ real repositories
- [ ] Generates 10+ commits without errors
- [ ] Creates 2+ PRs successfully
- [ ] Auto-approves 1+ PR that passes quality checks
- [ ] Rejects 1+ PR with clear feedback

***

## 14. Implementation Files

**Structure:**
```
codeinspector/
├── __init__.py
├── cli.py              # CLI commands
├── git_handler.py      # Git operations
├── github_client.py    # GitHub API
├── agents.py           # ADK agents
├── quality_checker.py  # Quality checks
└── config.py           # Configuration
```

**Start coding NOW:**
```bash
mkdir codeinspector
cd codeinspector
touch cli.py git_handler.py github_client.py agents.py quality_checker.py config.py
pip install google-adk gitpython click pygithub
```

***

## 🚀 **BUILD STARTS NOW**

No future features. No "nice to have." Just these 4 core features implemented today.

**Your next command:**
```bash
pip install google-adk gitpython click pygithub
```

Then create `agents.py` and start building the CommitGenerator agent.

Ready to code? 🔥

[1](https://github.com/marketplace/actions/auto-approve)
[2](https://github.com/marketplace/actions/pr-automation)
[3](https://docs.github.com/articles/approving-a-pull-request-with-required-reviews)
[4](https://stackoverflow.com/questions/74159955/can-i-set-up-github-repo-to-autoapprove-and-merge-prs-from-a-specific-user)
[5](https://fluxcd.io/flux/use-cases/gh-actions-auto-pr/)
[6](https://logicballs.com/tools/code-review-checklist)
[7](https://github.com/orgs/community/discussions/24346)
[8](https://graphite.com/guides/streamlining-pull-request-process-automation)
[9](https://www.qodo.ai/blog/code-review-checklist/)
[10](https://stackoverflow.com/questions/44159555/how-do-we-know-a-pull-request-is-approved-or-rejected-using-api-in-github)
[11](https://linearb.io/blog/github-approve-pull-request)
[12](https://www.taskade.com/generate/programming/code-review-checklist)
[13](https://graphite.com/guides/how-to-track-pull-request-approval-rates-in-github)
[14](https://github.com/marketplace/actions/automatic-pull-request-review)
[15](https://sentry.io/product/ai-code-review/)
[16](https://docs.github.com/en/rest/pulls/pulls)
[17](https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/configure-automatic-review)
[18](https://www.reddit.com/r/softwaredevelopment/comments/1ei4nat/elevating_code_quality_the_ultimate_code_review/)
[19](https://docs.github.com/en/rest/pulls/reviews)
[20](https://coderabbit.ai)