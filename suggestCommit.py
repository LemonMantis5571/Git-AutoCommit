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


def get_staged_diff_summary():
    """Gets a smart summary of staged changes including stats and meaningful content."""
    try:
        # Get file stats (which files changed and how much)
        stat_result = subprocess.run(
            ["git", "diff", "--staged", "--stat"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True
        )
        stats = stat_result.stdout

      
        diff_result = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True
        )
        full_diff = diff_result.stdout

        name_status_result = subprocess.run(
            ["git", "diff", "--staged", "--name-status"],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True
        )
        name_status = name_status_result.stdout

     
        summary = f"=== FILE CHANGES ===\n{name_status}\n\n=== STATS ===\n{stats}\n\n"
        
       
        lines = full_diff.split('\n')
        total_lines = len(lines)
        
        if total_lines > 300:
            
            important_lines = []
       
            
            for i, line in enumerate(lines):
               
                if line.startswith('diff --git') or line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
                    important_lines.append(line)
                   
                    continue
                
             
                if any(keyword in line for keyword in ['import ', 'export ', 'from ', 'require(']):
                    important_lines.append(line)
                    continue
                
              
                if any(keyword in line for keyword in ['function ', 'class ', 'def ', 'const ', 'let ', 'var ', 'async ', 'interface ', 'type ']):
                    important_lines.append(line)
                 
                    for j in range(i + 1, min(i + 3, total_lines)):
                        if lines[j].strip():
                            important_lines.append(lines[j])
                    continue
                
           
                if (line.startswith('+') or line.startswith('-')) and not line.startswith('+++') and not line.startswith('---'):
                    if len(important_lines) < 200 or i % 3 == 0:  # Sample every 3rd change if too many
                        important_lines.append(line)
            
            summary += "=== KEY CHANGES (Summarized) ===\n"
            summary += '\n'.join(important_lines[:250])  # Limit to 250 lines of important content
            summary += f"\n\n[Note: Full diff has {total_lines} lines. Above shows key structural changes.]"
        else:
            
            summary += "=== FULL DIFF ===\n"
            summary += full_diff

        return summary

    except subprocess.CalledProcessError as e:
        print(f"Error running git command: {e.stderr}", file=sys.stderr)
        return None


def generate_commit_message(diff_summary):
    """Sends the diff summary to the Gemini API and gets a suggestion."""
    if not diff_summary or not diff_summary.strip():
        print("No staged changes found. Use 'git add' to stage files.", file=sys.stderr)
        sys.exit(0)

    try:
        # Create the prompt
        prompt = f"{SYSTEM_PROMPT}\n\n{diff_summary}"

        # Generate commit message with higher context window
        response = client.models.generate_content(
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
        sys.exit(1)


if __name__ == "__main__":
    diff_summary = get_staged_diff_summary()
    if diff_summary is None:
        sys.exit(1)

    # Generate and print the commit message
    message = generate_commit_message(diff_summary)
    print(message)