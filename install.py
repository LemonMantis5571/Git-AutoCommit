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
    """Install the git-autocommit package"""
    print("\nInstalling git-autocommit package...")
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
            print('   export api_key="YOUR_API_KEY"')


def setup_git_alias():
    """Set up git alias for convenience"""
    print()
    setup = input("Do you want to set up the 'git aic' alias? (y/n): ").strip().lower()
    
    if setup in ['y', 'yes']:
        try:
            subprocess.run(
                ["git", "config", "--global", "alias.aic", "!git-suggest"],
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
    print("  git-suggest               # Generate and commit")
    print("  git-suggest --dry-run     # Preview message only")
    print("  git-suggest --interactive # Review before committing")
    print("  git-suggest --help        # Show all options")
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
    
    # Setup git alias
    setup_git_alias()
    
    # Print usage
    print_usage()


if __name__ == "__main__":
    main()
