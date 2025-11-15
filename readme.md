# Auto-Commit Message Generator

Automatically generate conventional commit messages using Google's Gemini AI based on your staged git changes.

## Features

- 🤖 AI-powered commit message generation
- 📝 Follows Conventional Commits standard
- ⚡ Simple git alias integration
- 🎯 Analyzes staged changes to create meaningful messages

## Prerequisites

- Python 3.7 or higher
- Git
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/LemonMantis5571/Git-AutoCommit.git
cd auto-commit-message
```

### 2. Install Required Package

```bash
pip install google-genai
```

### 3. Set Up Your API Key

Choose one of the following methods:

#### Option A: Windows (Permanent)

```bash
setx api_key "YOUR_GEMINI_API_KEY"
```

**Important**: Restart your terminal/Git Bash after running this command.

#### Option B: Linux/Mac (Permanent)

Add to your `~/.bashrc` or `~/.zshrc`:

```bash
export api_key="YOUR_GEMINI_API_KEY"
```

Then reload:

```bash
source ~/.bashrc  # or source ~/.zshrc
```

#### Option C: Temporary (Current Session Only)

```bash
export api_key="YOUR_GEMINI_API_KEY"
```

### 4. Create the Git Alias

Run this command, replacing the path with the actual location of `suggestCommit.py`:

**Windows:**
```bash
git config --global alias.aic '!_f() { MSG=$(python "C:/path/to/auto-commit-message/suggestCommit.py" 2>&1); if [ $? -eq 0 ]; then git commit -m "$MSG"; else echo "Error: $MSG"; fi; }; _f'
```

**Linux/Mac:**
```bash
git config --global alias.aic '!_f() { MSG=$(python3 "/path/to/auto-commit-message/suggestCommit.py" 2>&1); if [ $? -eq 0 ]; then git commit -m "$MSG"; else echo "Error: $MSG"; fi; }; _f'
```

**Example for Windows:**
```bash
git config --global alias.aic '!_f() { MSG=$(python "C:/Users/YourName/Documents/auto-commit-message/suggestCommit.py" 2>&1); if [ $? -eq 0 ]; then git commit -m "$MSG"; else echo "Error: $MSG"; fi; }; _f'
```

## Usage

1. Stage your changes as usual:
   ```bash
   git add .
   ```

2. Run the auto-commit command:
   ```bash
   git aic
   ```

3. The script will:
   - Analyze your staged changes
   - Generate a conventional commit message
   - Commit automatically with the generated message

## Example Output

```bash
$ git add .
$ git aic
[main abc1234] feat: add user authentication endpoint
 3 files changed, 45 insertions(+), 2 deletions(-)
```

## Commit Message Format

The generated messages follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, etc.)
- `refactor:` - Code refactoring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

## Troubleshooting

### "api_key environment variable not set"

**Windows**: Restart your terminal after running `setx`.

**Linux/Mac**: Make sure you ran `source ~/.bashrc` or restarted your terminal.

Verify the variable is set:
```bash
echo $api_key
```

### "Error calling Gemini API"

- Check your API key is valid
- Verify you have internet connection
- Ensure you have credits/quota available in your Google AI Studio account

### "No staged changes found"

You need to stage files before committing:
```bash
git add <files>
git aic
```

### Script path not found

Make sure to use the absolute path to `suggestCommit.py` in your alias. On Windows, use forward slashes (`/`) not backslashes (`\`).

### Alias already exists

Remove the old alias first:
```bash
git config --global --unset-all alias.aic
```

Then create it again with the correct path.

## Uninstall

Remove the git alias:
```bash
git config --global --unset alias.aic
```

Remove the environment variable:

**Windows:**
```bash
setx api_key ""
```

**Linux/Mac:** Remove the export line from your `~/.bashrc` or `~/.zshrc`


