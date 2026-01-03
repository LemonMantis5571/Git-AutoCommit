import os
import sys
from google import genai


SYSTEM_PROMPT = """You are an expert programmer who writes concise and professional git commit messages.
Based on the following git changes, generate a commit message.

Guidelines:
- Follow the "Conventional Commits" standard (e.g., 'feat:', 'fix:', 'docs:', 'style:', 'refactor:', 'test:').
- The message should be a single line, 72 characters or less.
- Do NOT include any extra text, explanations, or markdown formatting.
- Just return the raw commit message.
- Focus on WHAT changed and WHY, not implementation details.

EXAMPLE:
feat: add user login endpoint

Here are the changes:
"""


class GeminiClient:
    
    
    def __init__(self, api_key=None, model="gemini-2.5-flash"):
        """Initialize Gemini client.
        
        Args:
            api_key: Google Gemini API key
            model: Model name to use (default: gemini-2.5-flash)
        """
        self.api_key = api_key or os.getenv("api_key")
        if not self.api_key:
            raise ValueError("API key not provided. Set 'api_key' environment variable or pass it to the constructor.")
        
        self.model = model
        self.client = genai.Client(api_key=self.api_key)
    
    def generate_commit_message(self, diff_summary):
   
        if not diff_summary or not diff_summary.strip():
            print("No staged changes found. Use 'git add' to stage files.", file=sys.stderr)
            return None

        try:
            
            prompt = f"{SYSTEM_PROMPT}\n\n{diff_summary}"

           
            response = self.client.models.generate_content(
                model=self.model, 
                contents=prompt,
            )

            
            message = response.text.strip().replace("`", "").replace("**", "")
            
            
            message = message.split('\n')[0]
            
            return message

        except Exception as e:
            print(f"Error calling Gemini API: {e}", file=sys.stderr)
            return None
