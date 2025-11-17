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
cd Git-AutoCommit
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

Run this command, replacing the path with the actual location of your cloned repository:

**Windows (Git Bash):**
```bash
git config --global alias.aic '!python "C:/Users/YourName/Documents/Git-AutoCommit/suggestCommit.py" | git commit -F -'
```

**Linux/Mac:**
```bash
git config --global alias.aic '!python3 "$HOME/Git-AutoCommit/suggestCommit.py" | git commit -F -'
```

**Example for Windows:**
```bash
git config --global alias.aic '!python "C:/Users/lemonmantis/Documents/Git-AutoCommit/suggestCommit.py" | git commit -F -'
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
# Windows (Command Prompt)
echo %api_key%

# Windows (Git Bash) / Linux / Mac
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

### "can't find '__main__' module" or Script path not found

Make sure to use the correct path to `suggestCommit.py` (not just the folder name) in your alias:
- **Correct**: `C:/Users/YourName/Documents/Git-AutoCommit/suggestCommit.py`
- **Incorrect**: `C:/Users/YourName/Documents/Git-AutoCommit`

On Windows, use forward slashes (`/`) not backslashes (`\`) in the git config.

### Alias already exists

Remove the old alias first:
```bash
git config --global --unset alias.aic
```

Then create it again with the correct path.

### "Aborting commit due to empty commit message"

This usually means:
1. The Python script path is incorrect
2. The API key is not set properly
3. There's an error in the script execution

Check the script runs correctly by testing it directly:
```bash
python "C:/path/to/Git-AutoCommit/suggestCommit.py"
```

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.