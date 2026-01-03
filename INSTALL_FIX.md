# Git-Suggest Command Not Found - Fix Guide

If you're seeing the error `git-suggest : The term 'git-suggest' is not recognized`, this means the command-line script wasn't created during installation. Don't worry - here are several solutions!

## ✅ Solution 1: Use Python Module Directly (Works Immediately)

The package is installed correctly, you just need to call it differently:

```powershell
# Instead of:
git-suggest --help

# Use:
python -m git_autocommit --help
```

**Usage:**
```powershell
git add .
python -m git_autocommit
python -m git_autocommit --dry-run
python -m git_autocommit --interactive
```

---

## ✅ Solution 2: Add PowerShell Function (Recommended)

Add a function to your PowerShell profile so `git-suggest` works as expected.

### Step 1: Open your PowerShell profile
```powershell
notepad $PROFILE
```

If you get an error that the file doesn't exist, create it first:
```powershell
New-Item -Path $PROFILE -Type File -Force
notepad $PROFILE
```

### Step 2: Add this function to the file
```powershell
function git-suggest {
    python -m git_autocommit $args
}
```

### Step 3: Save and reload
```powershell
# Save the file in Notepad, then reload your profile:
. $PROFILE

# Now test it:
git-suggest --help
```

---

## ✅ Solution 3: Use the Wrapper Script

We've created a PowerShell wrapper script in the project directory:

```powershell
# From the Git-AutoCommit directory:
.\git-suggest.ps1 --help
.\git-suggest.ps1 --dry-run
```

To use it from anywhere, add the project directory to your PATH or copy `git-suggest.ps1` to a directory that's already in your PATH.

---

## ✅ Solution 4: Reinstall with Regular Install (Not Editable)

Try a regular installation instead of editable mode:

```powershell
# Uninstall first
pip uninstall git-autocommit

# Reinstall without -e flag
pip install .
```

Then check if the script was created:
```powershell
where.exe git-suggest
```

---

## 🔍 Why This Happened

The `pip install -e .` (editable install) sometimes doesn't create the executable wrapper scripts in the `Scripts` folder on Windows. This is a known issue with Python packaging on Windows.

The package itself is installed correctly - it's just the command-line wrapper that's missing.

---

## ✨ Recommended Setup

For the best experience, use **Solution 2** (PowerShell function). This gives you:
- ✅ `git-suggest` command works everywhere
- ✅ All arguments and options work correctly
- ✅ No need to remember the Python module syntax
- ✅ Works with the `git aic` alias

**Complete PowerShell Profile Setup:**
```powershell
# Open profile
notepad $PROFILE

# Add this:
function git-suggest {
    python -m git_autocommit $args
}

# Save, then reload:
. $PROFILE

# Test:
git-suggest --version
```

---

## 🎯 Quick Test

After applying any solution, test with:
```powershell
git-suggest --version
```

You should see: `git-suggest 1.0.0`
