"""
=================================================
Project Phoenix
Configuration Manager
=================================================

Responsible for:
- Loading environment variables
- Reading YAML configuration
- Validating project settings
"""

from pathlib import Path
from dotenv import load_dotenv
import os
import yaml

# -------------------------------------------------
# Project Root Directory
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_DIR = PROJECT_ROOT / "config"
# -------------------------------------------------
# Configuration Manager
# -------------------------------------------------

class Config:
    """
    Central configuration manager for Project Phoenix.
    """

    def __init__(self):
        """Initialize configuration."""
        self.project_root = PROJECT_ROOT
        self.config_dir = CONFIG_DIR

        self.env_loaded = False
        self.settings = {}

    def load_environment(self):
        """
        Load environment variables from .env file.
        """

        env_file = self.project_root / ".env"

        if env_file.exists():
            load_dotenv(env_file)
            self.env_loaded = True
        else:
            print("WARNING: .env file not found.")

    def load_settings(self):
        """
        Load settings from YAML configuration file.
        """

        settings_file = self.config_dir / "settings.yaml"

        if not settings_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {settings_file}"
            )

        with open(settings_file, "r", encoding="utf-8") as file:
            self.settings = yaml.safe_load(file) or {}
            
    def validate(self):
        """
        Validate loaded configuration.
        """

        if not self.env_loaded:
            raise RuntimeError(
                "Environment variables are not loaded."
            )

        if not isinstance(self.settings, dict):
            raise TypeError(
                "Settings must be a dictionary."
            )

        return True
# -------------------------------------------------
# Global Configuration Instance
# -------------------------------------------------

config = Config()