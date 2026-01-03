#!/usr/bin/env python3
"""Installation script for Git-AutoCommit"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def print_header():
    """Print installation header"""
    print("=" * 40)
    print("Git-AutoCommit Installation Script")
    print("=" * 40)
    print()


def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✓ Python found: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print("✗ Error: Python 3.7 or higher is required")
        return False


def check_git():
    """Check if Git is installed"""
    try:
        result = subprocess.run(
            ["git", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"✓ Git found: {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Error: Git is not installed. Please install Git first.")
        return False


def install_package():
    """Install the git-suggest package"""
    print("\nInstalling git-suggest package...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-e", "."],
            check=True
        )
        print("\n✓ Package installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("\n✗ Error: Failed to install package")
        return False


def setup_api_key():
    """Prompt user to set up API key"""
    print()
    has_key = input("Do you have a Google Gemini API key? (y/n): ").strip().lower()
    
    if has_key in ['y', 'yes']:
        api_key = input("Enter your Gemini API key: ").strip()
        
        # Set environment variable based on OS
        if platform.system() == "Windows":
            # Windows: Use setx command
            try:
                subprocess.run(
                    ["setx", "api_key", api_key],
                    check=True,
                    capture_output=True
                )
                print("\n✓ API key set as environment variable")
                print("⚠️  Please restart your terminal for the changes to take effect.")
            except subprocess.CalledProcessError:
                print("\n✗ Error: Failed to set environment variable")
                print(f"   Please manually set: setx api_key \"{api_key}\"")
        else:
            # Unix-like systems: Add to shell profile
            shell = os.environ.get('SHELL', '/bin/bash')
            if 'zsh' in shell:
                profile = Path.home() / '.zshrc'
            else:
                profile = Path.home() / '.bashrc'
            
            export_line = f'\nexport api_key="{api_key}"\n'
            
            try:
                with open(profile, 'a') as f:
                    f.write(export_line)
                print(f"\n✓ API key added to {profile}")
                print("⚠️  Please restart your terminal or run: source ~/.bashrc")
            except Exception as e:
                print(f"\n✗ Error: Failed to update {profile}")
                print(f"   Please manually add: export api_key=\"{api_key}\"")
    else:
        print("\n⚠️  You'll need to set the API key later:")
        print("   Get one at: https://aistudio.google.com/app/apikey")
        if platform.system() == "Windows":
            print("   Then run in PowerShell:")
            print('   setx api_key "YOUR_API_KEY"')
        else:
            print("   Then add to your shell profile (~/.bashrc or ~/.zshrc):")
            print('   export api_key=\"YOUR_API_KEY\"')


def setup_model_config():
    """Prompt user to select a Gemini model"""
    print()
    print("=" * 40)
    print("Model Configuration")
    print("=" * 40)
    
    # Available models as of January 2026
    models = {
        '1': ('gemini-2.5-flash', 'Fast, efficient, everyday tasks (Recommended)'),
        '2': ('gemini-2.5-pro', 'Deep reasoning, complex analysis'),
        '3': ('gemini-2.5-flash-lite', 'High throughput, cost efficient'),
        '4': ('gemini-3-flash-preview', 'Latest experimental, fast performance'),
        '5': ('gemini-3-pro-preview', 'Latest experimental, advanced reasoning'),
    }
    
    print("\nAvailable Gemini models:")
    for key, (model_name, description) in models.items():
        print(f"  {key}. {model_name:<25} - {description}")
    
    print()
    choice = input("Select a model (1-5) [default: 1]: ").strip() or '1'
    
    if choice not in models:
        print("Invalid choice, using default: gemini-2.5-flash")
        choice = '1'
    
    selected_model, description = models[choice]
    print(f"\n✓ Selected: {selected_model}")
    
    # Create .gitcommit.yml in home directory
    config_path = Path.home() / '.gitcommit.yml'
    config_content = f"""# Git-Suggest Configuration
# Google Gemini model to use
model: {selected_model}

# Maximum number of diff lines before summarization kicks in
max_diff_lines: 300

# Environment variable name for API key
api_key_env: api_key
"""
    
    try:
        with open(config_path, 'w') as f:
            f.write(config_content)
        print(f"✓ Configuration saved to {config_path}")
    except Exception as e:
        print(f"⚠️  Could not save config file: {e}")
        print(f"   You can manually create {config_path} with:")
        print(f"   model: {selected_model}")



def setup_git_alias():
    """Set up git alias for convenience"""
    print()
    setup = input("Do you want to set up the 'git aic' alias? (y/n): ").strip().lower()
    
    if setup in ['y', 'yes']:
        try:
            subprocess.run(
                ["git", "config", "--global", "alias.aic", "!python -m git_suggest"],
                check=True
            )
            print("✓ Git alias 'git aic' created!")
        except subprocess.CalledProcessError:
            print("✗ Error: Failed to create git alias")


def print_usage():
    """Print usage information"""
    print("\n" + "=" * 40)
    print("Installation Complete!")
    print("=" * 40)
    print("\nUsage:")
    print("  python -m git_suggest               # Generate and commit")
    print("  python -m git_suggest --dry-run     # Preview message only")
    print("  python -m git_suggest --interactive # Review before committing")
    print("  python -m git_suggest --help        # Show all options")
    print("\nOr use the git alias:")
    print("  git aic")
    print()


def main():
    """Main installation flow"""
    print_header()
    
    # Check prerequisites
    if not check_python():
        sys.exit(1)
    
    if not check_git():
        sys.exit(1)
    
    print()
    
    # Install package
    if not install_package():
        sys.exit(1)
    
    # Setup API key
    setup_api_key()
    
    # Setup model configuration
    setup_model_config()
    
    # Setup git alias
    setup_git_alias()
    
    # Print usage
    print_usage()


if __name__ == "__main__":
    main()
