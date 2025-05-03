"""
Configuration settings for the finance tracker application.
"""
import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

# Default application settings
DEFAULT_CONFIG = {
    # Database settings
    "database": {
        "path": "finance_tracker.db",
        "backup_dir": "backups"
    },
    
    # Application settings
    "application": {
        "default_currency": "USD",
        "date_format": "%Y-%m-%d",
        "auto_backup": True,
        "backup_frequency_days": 7
    },
    
    # Analysis settings
    "analysis": {
        "default_analysis_period_months": 6,
        "unusual_expense_threshold": 2.0,
        "recurring_min_occurrences": 2
    },
    
    # Budget settings
    "budget": {
        "needs_target_percent": 50,
        "wants_target_percent": 30,
        "savings_target_percent": 20
    },
    
    # Visualization settings
    "visualization": {
        "chart_style": "seaborn-v0_8-darkgrid",
        "color_palette": "viridis",
        "export_format": "png",
        "export_dpi": 100
    }
}

class Config:
    """
    Configuration manager for the finance tracker application.
    
    This class handles loading, saving, and accessing configuration settings.
    """
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Optional path to the configuration file.
                         If not provided, uses the default location.
        """
        # Determine config file path
        if config_path:
            self.config_path = Path(config_path)
        else:
            # Use platform-specific user config directory
            if os.name == 'nt':  # Windows
                config_dir = Path(os.environ.get('APPDATA', '')) / 'FinanceTracker'
            else:  # Unix-like
                config_dir = Path.home() / '.config' / 'finance_tracker'
            
            # Create directory if it doesn't exist
            config_dir.mkdir(parents=True, exist_ok=True)
            self.config_path = config_dir / 'config.json'
        
        # Load configuration
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """
        Load configuration from file or use defaults.
        
        Returns:
            Dictionary containing configuration settings.
        """
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = json.load(f)
                
                # Merge with defaults to ensure all settings exist
                return self._merge_configs(DEFAULT_CONFIG, config)
            except Exception as e:
                print(f"Error loading config file: {e}")
                print("Using default configuration.")
                return dict(DEFAULT_CONFIG)
        else:
            # No config file exists, create one with default settings
            self.save_config(DEFAULT_CONFIG)
            return dict(DEFAULT_CONFIG)
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """
        Recursively merge user config with default config.
        
        Args:
            default: Default configuration dictionary.
            user: User configuration dictionary.
            
        Returns:
            Merged configuration dictionary.
        """
        result = dict(default)
        
        for key, user_value in user.items():
            # If the key exists in default and both values are dicts, merge recursively
            if key in default and isinstance(default[key], dict) and isinstance(user_value, dict):
                result[key] = self._merge_configs(default[key], user_value)
            else:
                # Otherwise use the user value
                result[key] = user_value
        
        return result
    
    def save_config(self, config: Dict[str, Any] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            config: Optional config dict to save. If not provided, saves the current config.
        """
        if config is None:
            config = self.config
        
        try:
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: Configuration section (e.g., 'database', 'application').
            key: Configuration key within the section.
            default: Default value to return if the key doesn't exist.
            
        Returns:
            The configuration value, or default if not found.
        """
        try:
            return self.config[section][key]
        except KeyError:
            return default
    
    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set a configuration value.
        
        Args:
            section: Configuration section (e.g., 'database', 'application').
            key: Configuration key within the section.
            value: Value to set.
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        self.save_config()
    
    def get_db_path(self) -> str:
        """
        Get the database path, considering environment variables.
        
        Returns:
            Path to the database file.
        """
        # Environment variable takes precedence
        env_path = os.environ.get('FINANCE_DB_PATH')
        if env_path:
            return env_path
        
        # Otherwise use the configured path
        return self.get('database', 'path', 'finance_tracker.db')
    
    def reset_to_defaults(self) -> None:
        """Reset all configuration to default values."""
        self.config = dict(DEFAULT_CONFIG)
        self.save_config()


# Global configuration instance
config = Config()