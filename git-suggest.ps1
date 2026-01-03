#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Wrapper script for git-suggest command
.DESCRIPTION
    This script calls the git_autocommit Python module with all arguments passed through.
    Use this if the git-suggest command is not available in your PATH.
.EXAMPLE
    .\git-suggest.ps1 --help
    .\git-suggest.ps1 --dry-run
    .\git-suggest.ps1 --interactive
#>

# Pass all arguments to the Python module
python -m git_suggest $args
