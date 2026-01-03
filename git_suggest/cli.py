"""Command-line interface for git_autocommit."""

import argparse
import sys
from .version import __version__
from .git_utils import get_staged_diff_summary, commit_with_message
from .ai_client import GeminiClient
from .config import Config


def get_user_confirmation(message):
    """Ask user to confirm or edit the commit message."""
    print("\n" + "="*60)
    print("Generated commit message:")
    print("="*60)
    print(f"\n  {message}\n")
    print("="*60)
    
    while True:
        choice = input("\nOptions: [c]ommit, [e]dit, [r]egenerate, [a]bort: ").lower().strip()
        
        if choice == 'c':
            return message, True
        elif choice == 'e':
            print("\nEnter your commit message (press Enter when done):")
            edited = input("> ").strip()
            if edited:
                return edited, True
            print("Empty message, try again.")
        elif choice == 'r':
            return None, False  # Signal to regenerate
        elif choice == 'a':
            print("Commit aborted.")
            sys.exit(0)
        else:
            print("Invalid choice. Please enter c, e, r, or a.")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='AI-powered git commit message generator using Google Gemini',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  git-suggest                    # Generate and commit with AI message
  git-suggest --dry-run          # Show message without committing
  git-suggest --interactive      # Review message before committing
  git-suggest --config ~/.myconfig.yml  # Use custom config file

For more information, visit: https://github.com/LemonMantis5571/Git-AutoCommit
        """
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version=f'git-suggest {__version__}'
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='Generate message without committing'
    )
    
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Review and optionally edit message before committing'
    )
    
    parser.add_argument(
        '--config', '-c',
        type=str,
        help='Path to custom configuration file'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output for debugging'
    )
    
    args = parser.parse_args()
    
  
    config = Config(args.config)
    
    # Get API key
    api_key = config.get_api_key()
    if not api_key:
        print("Error: API key not found.", file=sys.stderr)
        print("\nPlease set the 'api_key' environment variable:", file=sys.stderr)
        print("  Windows: setx api_key \"YOUR_API_KEY\"", file=sys.stderr)
        print("  Linux/Mac: export api_key=\"YOUR_API_KEY\"", file=sys.stderr)
        print("\nOr add it to your .gitcommit.yml config file.", file=sys.stderr)
        sys.exit(1)
    
   
    if args.verbose:
        print("Fetching staged changes...")
    
    diff_summary = get_staged_diff_summary()
    if diff_summary is None:
        sys.exit(1)
    
    if not diff_summary.strip():
        print("No staged changes found. Use 'git add' to stage files.", file=sys.stderr)
        sys.exit(0)
    
    
    try:
        model = config.get('model', 'gemini-2.5-flash')
        client = GeminiClient(api_key, model=model)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate commit message
    if args.verbose:
        print("Generating commit message with AI...")
    
    message = client.generate_commit_message(diff_summary)
    if not message:
        sys.exit(1)
    
    
    if args.dry_run:
        print(message)
        sys.exit(0)
    
    if args.interactive:
        final_message = message
        while True:
            final_message, should_commit = get_user_confirmation(final_message)
            if should_commit:
                message = final_message
                break
            # Regenerate if requested
            if args.verbose:
                print("Regenerating commit message...")
            new_message = client.generate_commit_message(diff_summary)
            if new_message:
                final_message = new_message
            else:
                print("Failed to regenerate message.", file=sys.stderr)
                sys.exit(1)
    
   
    if args.verbose:
        print(f"Committing with message: {message}")
    
    success, output = commit_with_message(message)
    if success:
        print(output)
    else:
        print(f"Error committing: {output}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
