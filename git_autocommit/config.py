"""Configuration management for git_autocommit."""

import os
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


DEFAULT_CONFIG = {
    'model': 'gemini-2.0-flash-exp',
    'max_diff_lines': 300,
    'api_key_env': 'api_key',
}


class Config:
    """Configuration manager for git_autocommit."""
    
    def __init__(self, config_path=None):
        """Initialize configuration."""
        self.config = DEFAULT_CONFIG.copy()
        
        # Try to load from config file
        if config_path:
            self.load_config(config_path)
        else:
            # Look for .gitcommit.yml in current directory or home
            for path in [Path.cwd() / '.gitcommit.yml', Path.home() / '.gitcommit.yml']:
                if path.exists():
                    self.load_config(path)
                    break
    
    def load_config(self, path):
        """Load configuration from YAML file."""
        if not HAS_YAML:
            print(f"Warning: PyYAML not installed. Install with 'pip install pyyaml' to use config files.")
            return
        
        try:
            with open(path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    self.config.update(user_config)
        except Exception as e:
            print(f"Warning: Could not load config from {path}: {e}")
    
    def get(self, key, default=None):
        """Get configuration value."""
        return self.config.get(key, default)
    
    def get_api_key(self):
        """Get API key from environment."""
        env_var = self.config.get('api_key_env', 'api_key')
        return os.getenv(env_var)
