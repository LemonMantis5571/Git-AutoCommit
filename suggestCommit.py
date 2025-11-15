from google import genai
import subprocess
import os
import sys

# Get API key from environment
api_key = os.getenv("api_key")
if not api_key:
    print("Error: api_key environment variable not set.")
    sys.exit(1)


client = genai.Client(api_key=api_key)

SYSTEM_PROMPT = """You are an expert programmer who writes concise and professional git commit messages.
Based on the following 'git diff --staged' output, generate a commit message.

Guidelines:
- Follow the "Conventional Commits" standard (e.g., 'feat:', 'fix:', 'docs:', 'style:', 'refactor:', 'test:').
- The message should be a single line, 72 characters or less.
- Do NOT include any extra text, explanations, or markdown formatting.
- Just return the raw commit message.

EXAMPLE:
feat: add user login endpoint

Here is the diff:
"""


def get_staged_diff(max_lines=100):
    """Fetches the staged changes from git, truncated if too large."""
    try:
        result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True
        )
        diff = result.stdout

        # Truncate if too long
        lines = diff.split('\n')
        if len(lines) > max_lines:
            diff = '\n'.join(lines[:max_lines])
            diff += f"\n\n[... {len(lines) - max_lines} more lines truncated ...]"

        return diff
    except subprocess.CalledProcessError as e:
        print(f"Error running 'git diff': {e.stderr}", file=sys.stderr)
        return None


def generate_commit_message(diff_text):
    """Sends the diff to the Gemini API and gets a suggestion."""
    if not diff_text or not diff_text.strip():
        print("No staged changes found. Use 'git add' to stage files.", file=sys.stderr)
        sys.exit(0)

    try:
        # Create the prompt
        prompt = f"{SYSTEM_PROMPT}\n\n{diff_text}"

        # Generate commit message
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        # Clean up the response
        message = response.text.strip().replace("`", "").replace("**", "")
        return message

    except Exception as e:
        print(f"Error calling Gemini API: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    diff = get_staged_diff()
    if diff is None:
        sys.exit(1)

    # Generate and print the commit message
    message = generate_commit_message(diff)
    print(message)
