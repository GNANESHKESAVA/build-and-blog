import os
import sys
import getpass
from github import Github, GithubException
from codeinspector.config import save_config, load_config

def setup_token():
    print("🔧 CodeInspector GitHub Token Setup")
    print("-----------------------------------")
    print("This script will help you configure your GitHub Personal Access Token.")
    print("The token will be saved to ~/.codeinspector/config.json")
    print("")
    
    current_config = load_config()
    current_token = current_config.get("github_token")
    
    if current_token:
        print(f"ℹ️  A token is already configured: {current_token[:4]}...{current_token[-4:]}")
        change = input("Do you want to change it? (y/N): ").lower()
        if change != 'y':
            print("✅ Keeping existing token.")
            return

    print("Please enter your GitHub Personal Access Token.")
    print("You can generate one at https://github.com/settings/tokens")
    print("Scopes required: repo (for private repos), read:user")
    
    try:
        token = getpass.getpass("Token: ").strip()
    except Exception:
        # Fallback for environments where getpass might fail
        token = input("Token: ").strip()

    if not token:
        print("❌ No token entered. Aborting.")
        return

    print("\n🔄 Verifying token...")
    try:
        g = Github(token)
        user = g.get_user()
        print(f"✅ Authenticated as: {user.login}")
        
        config = load_config()
        config["github_token"] = token
        save_config(config)
        print("✅ Token saved successfully!")
        
    except GithubException as e:
        print(f"❌ Authentication failed: {e}")
        print("Please check your token and try again.")
    except Exception as e:
        print(f"❌ An error occurred: {e}")

    # Google API Key Setup
    print("\n🔑 Google API Key Setup (for AI features)")
    print("----------------------------------------")
    current_api_key = current_config.get("google_api_key")
    
    if current_api_key:
        print(f"ℹ️  API Key is already configured: {current_api_key[:4]}...{current_api_key[-4:]}")
        change = input("Do you want to change it? (y/N): ").lower()
        if change != 'y':
            print("✅ Keeping existing API Key.")
            return

    print("Please enter your Google API Key.")
    print("Get one here: https://aistudio.google.com/app/apikey")
    
    try:
        api_key = getpass.getpass("API Key: ").strip()
    except Exception:
        api_key = input("API Key: ").strip()

    if api_key:
        config = load_config()
        config["google_api_key"] = api_key
        save_config(config)
        print("✅ Google API Key saved successfully!")
    else:
        print("⚠️  No API Key entered. AI features might not work.")

if __name__ == "__main__":
    setup_token()
