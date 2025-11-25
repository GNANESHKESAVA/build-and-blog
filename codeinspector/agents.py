import google.generativeai as genai
import os

class Agent:
    def __init__(self, model_name="gemini-2.0-flash"):
        # Assumes GOOGLE_API_KEY is set in environment or config
        from .config import load_config
        config = load_config()
        api_key = os.getenv("GOOGLE_API_KEY") or config.get("google_api_key")
        if api_key:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
        else:
            self.model = None

    def generate(self, prompt):
        if not self.model:
            # Fallback for testing/demo without API key
            return "feat(demo): this is a generated commit message\n\n- Added new feature\n- Fixed bug"
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating content: {e}"

class CommitGenerator(Agent):
    def generate_message(self, diff):
        prompt = f"""
        You are an expert developer. Generate a Conventional Commit message for the following git diff.
        
        Rules:
        - Use the format: <type>(<scope>): <description>
        - Followed by a blank line
        - Followed by a bulleted list of details
        - Keep the first line under 72 characters
        - Types: feat, fix, docs, style, refactor, test, chore
        
        Diff:
        {diff}
        """
        return self.generate(prompt)

class PRDescriber(Agent):
    def generate_description(self, commits, diff):
        prompt = f"""
        You are an expert developer. Generate a Pull Request description based on the following commits and diff.
        
        Output Markdown with:
        - Summary
        - Changes list
        - Files categorized (Backend/Frontend/Tests)
        - Testing checklist
        - Breaking change warnings
        
        Commits:
        {commits}
        
        Diff:
        {diff}
        """
        return self.generate(prompt)

class QualityAnalyzer(Agent):
    def analyze(self, quality_report):
        prompt = f"""
        You are a strict code reviewer. Analyze the following quality report and decide if the PR should be approved.
        
        Report:
        {quality_report}
        
        If all critical checks passed, approve it. If there are issues, reject it and explain why.
        """
        return self.generate(prompt)
