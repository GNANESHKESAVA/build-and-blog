import os
import sys
from github import Github, GithubException
from codeinspector.config import load_config
from codeinspector.git_handler import GitHandler

def verify_setup():
    print("🔍 CodeInspector Environment Verification")
    print("---------------------------------------")
    
    # 1. Check GitHub Token
    print("\n1️⃣  Checking GitHub Token...")
    config = load_config()
    token = config.get("github_token") or os.getenv("GITHUB_TOKEN")
    
    if token:
        print(f"   ✅ Token found ({'Environment Variable' if os.getenv('GITHUB_TOKEN') else 'Config File'})")
        try:
            g = Github(token)
            user = g.get_user()
            print(f"   ✅ Authenticated with GitHub as: {user.login}")
        except GithubException as e:
            print(f"   ❌ GitHub Authentication failed: {e}")
    else:
        print("   ❌ No GitHub token found.")
        print("   👉 Run 'python3 setup_token.py' to configure it.")

    # 2. Check Google API Key
    print("\n2️⃣  Checking Google API Key...")
    api_key = os.getenv("GOOGLE_API_KEY") or config.get("google_api_key")
    if api_key:
        print(f"   ✅ GOOGLE_API_KEY is set ({'Environment Variable' if os.getenv('GOOGLE_API_KEY') else 'Config File'}).")
    else:
        print("   ⚠️  GOOGLE_API_KEY is NOT set.")
        print("   👉 You need this for the AI features (Gemini).")
        print("   👉 export GOOGLE_API_KEY='your_api_key'")

    # 3. Check Git Repository
    print("\n3️⃣  Checking Git Repository...")
    try:
        handler = GitHandler()
        if handler.is_valid_repo():
            print("   ✅ Current directory is a valid git repository.")
            try:
                remote_url = handler.repo.remotes.origin.url
                print(f"   ✅ Remote 'origin' URL: {remote_url}")
                
                if "github.com" not in remote_url:
                    print("   ⚠️  Remote URL does not appear to be a GitHub repository.")
                    print("       CodeInspector is optimized for GitHub.")
            except AttributeError:
                print("   ⚠️  No remote 'origin' found.")
        else:
            print("   ❌ Current directory is NOT a git repository.")
    except Exception as e:
        print(f"   ❌ Error checking git repo: {e}")

    print("\n---------------------------------------")
    print("Done.")

if __name__ == "__main__":
    verify_setup()
