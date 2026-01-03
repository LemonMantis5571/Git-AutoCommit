"""Git operations utilities."""

import subprocess
import sys


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


def commit_with_message(message):
  
    try:
        result = subprocess.run(
            ["git", "commit", "-m", message],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',
            check=True
        )
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr
