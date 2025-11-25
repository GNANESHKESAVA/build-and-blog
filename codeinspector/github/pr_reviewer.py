"""PR Reviewer - Automated PR review with inline comments and auto-approve/reject"""

import os
import click
from ..github_client import GitHubClient
from ..quality_checker import QualityChecker


class PRReviewer:
    """Automated PR reviewer that posts inline comments and approves/rejects PRs"""
    
    def __init__(self, github_token):
        self.github_client = GitHubClient(github_token)
        self.quality_checker = QualityChecker()
    
    def review_pr(self, repo_name, pr_number):
        """
        Review a pull request and post inline comments.
        Returns: (status, issues_found, review_url)
        status: 'approved', 'rejected', 'error'
        """
        click.echo(f"🔍 Reviewing PR #{pr_number} in {repo_name}...")
        
        # 1. Get the PR object
        pr = self.github_client.get_pr(repo_name, pr_number)
        if not pr:
            return 'error', 0, None
        
        # 2. Get PR diff
        files_changed = self.github_client.get_pr_diff(repo_name, pr_number)
        if not files_changed:
            click.echo("⚠️  No files changed in PR")
            return 'error', 0, None
        
        click.echo(f"📂 Checking {len(files_changed)} file(s)...")
        
        # 3. Check each file for issues
        all_issues = []
        for file_info in files_changed:
            filename = file_info['filename']
            
            # Skip non-Python files for now
            if not filename.endswith('.py'):
                continue
            
            # Check if file exists locally (needed for flake8)
            if not os.path.exists(filename):
                click.echo(f"⏭️  Skipping {filename} (not found locally)")
                continue
            
            click.echo(f"   Checking {filename}...")
            issues = self.quality_checker.check_file_with_line_details(filename)
            
            if issues:
                click.echo(f"   ❌ Found {len(issues)} issue(s) in {filename}")
                all_issues.extend(issues)
            else:
                click.echo(f"   ✅ No issues in {filename}")
        
        # 4. Post inline comments for each issue
        if all_issues:
            click.echo(f"\n💬 Posting {len(all_issues)} inline comment(s)...")
            for issue in all_issues[:20]:  # Limit to 20 comments to avoid spam
                comment_body = f"🤖 **CodeInspector**: `{issue['code']}` - {issue['message']}"
                success = self.github_client.post_inline_comment(
                    pr, 
                    issue['file'], 
                    issue['line'], 
                    comment_body
                )
                if success:
                    click.echo(f"   ✅ Comment posted at {issue['file']}:{issue['line']}")
                else:
                    click.echo(f"   ❌ Failed to post comment at {issue['file']}:{issue['line']}")
        
        # 5. Approve or reject based on findings
        if all_issues:
            # Reject PR
            summary = f"""❌ **CodeInspector** found {len(all_issues)} issue(s)

Please fix the following before merging:

"""
            # Group issues by file
            issues_by_file = {}
            for issue in all_issues:
                file = issue['file']
                if file not in issues_by_file:
                    issues_by_file[file] = []
                issues_by_file[file].append(issue)
            
            for file, file_issues in issues_by_file.items():
                summary += f"\n**{file}**:\n"
                for issue in file_issues[:10]:  # Limit per file
                    summary += f"- Line {issue['line']}: `{issue['code']}` {issue['message']}\n"
            
            self.github_client.reject_pr(pr, summary)
            click.echo(f"\n❌ PR rejected with {len(all_issues)} issue(s)")
            status = 'rejected'
        else:
            # Approve PR
            summary = "✅ **CodeInspector**: No issues found. All quality checks passed!"
            self.github_client.approve_pr(pr, summary)
            click.echo("\n✅ PR approved - no issues found")
            status = 'approved'
        
        return status, len(all_issues), pr.html_url
