"""Setup configuration for git_autocommit package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
readme_file = Path(__file__).parent / "readme.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="git-autocommit",
    version="1.0.0",
    author="LemonMantis5571",
    description="AI-powered git commit message generator using Google Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LemonMantis5571/Git-AutoCommit",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'git-suggest=git_autocommit.cli:main',
        ],
    },
    keywords="git commit ai gemini automation conventional-commits",
    project_urls={
        "Bug Reports": "https://github.com/LemonMantis5571/Git-AutoCommit/issues",
        "Source": "https://github.com/LemonMantis5571/Git-AutoCommit",
    },
)
