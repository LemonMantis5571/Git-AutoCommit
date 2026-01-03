"""AI client for generating commit messages using Google Gemini."""

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
    """Client for interacting with Google Gemini API."""
    
    def __init__(self, api_key=None):
        """Initialize the Gemini client."""
        self.api_key = api_key or os.getenv("api_key")
        if not self.api_key:
            raise ValueError("API key not provided. Set 'api_key' environment variable or pass it to the constructor.")
        
        self.client = genai.Client(api_key=self.api_key)
    
    def generate_commit_message(self, diff_summary):
        """Sends the diff summary to the Gemini API and gets a suggestion."""
        if not diff_summary or not diff_summary.strip():
            print("No staged changes found. Use 'git add' to stage files.", file=sys.stderr)
            return None

        try:
            # Create the prompt
            prompt = f"{SYSTEM_PROMPT}\n\n{diff_summary}"

            # Generate commit message with higher context window
            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp", 
                contents=prompt,
            )

            # Clean up the response
            message = response.text.strip().replace("`", "").replace("**", "")
            
            # Ensure it's a single line
            message = message.split('\n')[0]
            
            return message

        except Exception as e:
            print(f"Error calling Gemini API: {e}", file=sys.stderr)
            return None
