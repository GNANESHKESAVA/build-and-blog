# End-to-End Testing Guide

To fully test the `codeinspector` tool, especially the Pull Request (PR) creation and auto-approval features, follow these steps.

## Prerequisites
- GitHub Token configured (You did this!)
- Google API Key configured (You did this!)
- `codeinspector` installed or available via `run_local.sh`

## Step 1: Install CodeInspector Locally (Recommended)
To run `codeinspector` from *any* directory (like a new test repo), install it in "editable" mode.

```bash
# In the code_inspector_ai directory
pip install -e .
```
*Now you can type `codeinspector` in any terminal window!*

## Step 2: Create a Test Repository
To avoid creating junk PRs on your main project, create a temporary test repo.

1.  **Go to GitHub**: Create a new repository named `ci-test-repo` (Public or Private).
    *   Initialize it with a README.
2.  **Clone it locally**:
    ```bash
    cd ~/Downloads
    git clone https://github.com/<YOUR_USERNAME>/ci-test-repo.git
    cd ci-test-repo
    ```

## Step 3: Test Commit Generation
1.  **Create a file**:
    ```bash
    echo "def hello(): print('Hello AI')" > hello.py
    ```
2.  **Stage it**:
    ```bash
    git add hello.py
    ```
3.  **Generate Commit**:
    ```bash
    codeinspector commit
    ```
    *   Accept the generated message.

## Step 4: Test PR Creation & Auto-Approval
1.  **Create a Feature Branch**:
    ```bash
    git checkout -b feature/add-math
    ```
2.  **Make Changes**:
    ```bash
    echo "def add(a, b): return a + b" >> hello.py
    git add hello.py
    codeinspector commit --yes
    ```
3.  **Create PR**:
    ```bash
    codeinspector pr --title "Add math function" --auto
    ```

**What should happen:**
1.  The tool pushes your branch to GitHub.
2.  It creates a Pull Request.
3.  It runs quality checks (Tests, Secrets, Lint, etc.).
4.  If checks pass, it **Auto-Approves** the PR! 
5.  If checks fail, it comments on the PR with the issues.

## Step 5: Cleanup
You can delete the test repo from GitHub and your local machine when done.
