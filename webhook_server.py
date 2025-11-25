"""
GitHub Webhook Server for CodeInspector
Handles pull_request events and triggers automated PR reviews
"""

import os
import hmac
import hashlib
from flask import Flask, request, jsonify
import click

app = Flask(__name__)


def verify_github_signature(payload_body, signature_header):
    """Verify that the payload was sent from GitHub by validating SHA256"""
    secret = os.getenv('GITHUB_WEBHOOK_SECRET', '')
    if not secret:
        return True  # Skip verification if no secret set (dev mode)
    
    hash_object = hmac.new(
        secret.encode('utf-8'),
        msg=payload_body,
        digestmod=hashlib.sha256
    )
    expected_signature = 'sha256=' + hash_object.hexdigest()
    
    return hmac.compare_digest(expected_signature, signature_header)


@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    """Handle GitHub webhook events"""
    
    # Verify signature
    signature = request.headers.get('X-Hub-Signature-256')
    if signature and not verify_github_signature(request.data, signature):
        return jsonify({'error': 'Invalid signature'}), 401
    
    event = request.headers.get('X-GitHub-Event')
    payload = request.json
    
    click.echo(f"📨 Received {event} event")
    
    # Handle pull_request events
    if event == 'pull_request':
        action = payload.get('action')
        
        # Trigger review on opened or synchronized (new commits pushed)
        if action in ['opened', 'synchronize']:
            pr = payload.get('pull_request')
            pr_number = pr.get('number')
            repo_full_name = payload.get('repository', {}).get('full_name')
            
            click.echo(f"🔍 Triggering review for PR #{pr_number} in {repo_full_name}")
            
            # Import here to avoid circular imports
            from codeinspector.github.pr_reviewer import PRReviewer
            from codeinspector.db.pr_repository import PRReviewRepository
            from codeinspector.config import load_config
            
            try:
                config = load_config()
                token = os.getenv('GITHUB_TOKEN') or config.get('github_token')
                
                if not token:
                    return jsonify({'error': 'GitHub token not configured'}), 500
                
                # Run PR review
                reviewer = PRReviewer(token)
                status, issues_found, review_url = reviewer.review_pr(repo_full_name, pr_number)
                
                # Save to database
                db_repo = PRReviewRepository(config.get('db_path'))
                review_data = {
                    'pr_number': pr_number,
                    'repository': repo_full_name,
                    'status': status,
                    'issues_found': issues_found,
                    'review_url': review_url,
                    'comments': []
                }
                db_repo.save_pr_review(review_data)
                db_repo.close()
                
                return jsonify({
                    'status': 'success',
                    'pr_number': pr_number,
                    'review_status': status,
                    'issues_found': issues_found
                }), 200
                
            except Exception as e:
                click.echo(f"❌ Error processing webhook: {e}")
                return jsonify({'error': str(e)}), 500
    
    return jsonify({'status': 'ignored'}), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/history', methods=['GET'])
def history():
    """View PR review history"""
    try:
        from codeinspector.db.pr_repository import PRReviewRepository
        from codeinspector.config import load_config
        
        config = load_config()
        db_repo = PRReviewRepository(config.get('db_path'))
        reviews = db_repo.get_pr_review_history(limit=50)
        db_repo.close()
        
        html = """
        <html>
        <head>
            <title>CodeInspector History</title>
            <style>
                body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
                h1 { color: #333; }
                .review { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 8px; }
                .approved { border-left: 5px solid #28a745; }
                .rejected { border-left: 5px solid #dc3545; }
                .meta { color: #666; font-size: 0.9em; margin-bottom: 10px; }
                .status { font-weight: bold; }
                .status.approved { color: #28a745; }
                .status.rejected { color: #dc3545; }
            </style>
        </head>
        <body>
            <h1>🤖 CodeInspector Review History</h1>
        """
        
        if not reviews:
            html += "<p>No reviews found yet.</p>"
        
        for review in reviews:
            status_class = "approved" if review['status'] == 'approved' else "rejected"
            icon = "✅" if review['status'] == 'approved' else "❌"
            
            html += f"""
            <div class="review {status_class}">
                <div class="meta">
                    {icon} <strong>PR #{review['pr_number']}</strong> in {review['repository']}
                    <br>
                    📅 {review['timestamp']}
                </div>
                <div>
                    Status: <span class="status {status_class}">{review['status'].upper()}</span>
                    <br>
                    🐛 Issues found: {review['issues_found']}
                    <br>
                    <a href="{review.get('review_url', '#')}" target="_blank">View on GitHub</a>
                </div>
            </div>
            """
            
        html += "</body></html>"
        return html
        
    except Exception as e:
        return f"Error loading history: {str(e)}", 500



if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
