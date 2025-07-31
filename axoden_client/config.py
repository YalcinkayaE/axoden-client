"""
AxoDen Client - Configuration management
"""

import os
import json
import keyring
from pathlib import Path
from typing import Optional, Dict, Any


class AxoDenConfig:
    """Manage AxoDen client configuration"""
    
    def __init__(self):
        self.config_dir = Path.home() / ".axoden"
        self.config_file = self.config_dir / "config.json"
        self.version = "0.1.0"
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Load configuration
        self._load_config()
    
    def _load_config(self):
        """Load configuration from file and environment"""
        # Default values
        self.base_url = "https://api.axoden.com"
        self.agent_id = None
        self.default_format = "claude"
        
        # Load from config file if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config_data = json.load(f)
                    self.base_url = config_data.get("base_url", self.base_url)
                    self.agent_id = config_data.get("agent_id", self.agent_id)
                    self.default_format = config_data.get("default_format", self.default_format)
            except Exception:
                pass
        
        # Override with environment variables
        self.base_url = os.environ.get("AXODEN_API_URL", self.base_url)
        self.agent_id = os.environ.get("AXODEN_AGENT_ID", self.agent_id)
        
        # API key from environment or secure storage
        self._api_key = os.environ.get("AXODEN_API_KEY")
    
    @property
    def api_key(self) -> Optional[str]:
        """Get API key from environment or secure storage"""
        if self._api_key:
            return self._api_key
        
        # Try to get from keyring
        try:
            return keyring.get_password("axoden", "api_key")
        except Exception:
            return None
    
    def save_api_key(self, api_key: str):
        """Save API key securely"""
        try:
            keyring.set_password("axoden", "api_key", api_key)
        except Exception:
            # Fallback to environment variable instruction
            print("Could not save API key securely.")
            print(f"Please set environment variable: export AXODEN_API_KEY='{api_key}'")
    
    def save(self):
        """Save configuration to file"""
        config_data = {
            "base_url": self.base_url,
            "agent_id": self.agent_id,
            "default_format": self.default_format
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(config_data, f, indent=2)
    
    def reset(self):
        """Reset configuration to defaults"""
        if self.config_file.exists():
            self.config_file.unlink()
        
        # Clear API key from keyring
        try:
            keyring.delete_password("axoden", "api_key")
        except Exception:
            pass
        
        # Reload defaults
        self._load_config()