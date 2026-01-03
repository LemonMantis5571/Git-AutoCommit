#!/bin/bash
# Installation script for Git-AutoCommit (Linux/Mac)

set -e

echo "======================================"
echo "Git-AutoCommit Installation Script"
echo "======================================"
echo ""

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check for Git
if ! command -v git &> /dev/null; then
    echo "Error: Git is not installed. Please install Git first."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo "✓ Git found: $(git --version)"
echo ""

# Install package
echo "Installing git-autocommit package..."
pip3 install -e .

echo ""
echo "✓ Package installed successfully!"
echo ""

# Prompt for API key
read -p "Do you have a Google Gemini API key? (y/n): " has_key

if [ "$has_key" = "y" ] || [ "$has_key" = "Y" ]; then
    read -p "Enter your Gemini API key: " api_key
    
    # Determine shell config file
    if [ -f "$HOME/.zshrc" ]; then
        shell_config="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        shell_config="$HOME/.bashrc"
    else
        shell_config="$HOME/.profile"
    fi
    
    # Add API key to shell config
    echo "" >> "$shell_config"
    echo "# Git-AutoCommit API Key" >> "$shell_config"
    echo "export api_key=\"$api_key\"" >> "$shell_config"
    
    echo "✓ API key added to $shell_config"
    echo ""
    echo "⚠️  Please run: source $shell_config"
    echo "   Or restart your terminal for the changes to take effect."
else
    echo ""
    echo "⚠️  You'll need to set the API key later:"
    echo "   Get one at: https://aistudio.google.com/app/apikey"
    echo "   Then add to your shell config (~/.bashrc or ~/.zshrc):"
    echo "   export api_key=\"YOUR_API_KEY\""
fi

echo ""

# Setup git alias
read -p "Do you want to set up the 'git aic' alias? (y/n): " setup_alias

if [ "$setup_alias" = "y" ] || [ "$setup_alias" = "Y" ]; then
    git config --global alias.aic '!git-suggest'
    echo "✓ Git alias 'git aic' created!"
    echo "  You can now use: git aic"
fi

echo ""
echo "======================================"
echo "Installation Complete!"
echo "======================================"
echo ""
echo "Usage:"
echo "  git-suggest              # Generate and commit"
echo "  git-suggest --dry-run    # Preview message only"
echo "  git-suggest --interactive # Review before committing"
echo "  git-suggest --help       # Show all options"
echo ""
echo "Or use the git alias:"
echo "  git aic"
echo ""
