# backup_configuration.py

import os
import json
from pathlib import Path


class BackupConfigurationError(Exception):
    """Custom exception for backup configuration errors"""
    pass


class BackupConfigurationManager:
    """Manages configuration for API Gateway backup settings."""

    CONFIG_FILE_PATH = Path.home() / ".api_gateway_backup_config.json"

    def __init__(self):
        self.backup_details = None
        self.load_existing_configuration()

    def configure_backup(self, backup_interval: int, retention_period: int, backup_location: str):
        """
        Sets the backup configuration for the API Gateway.

        Params:
            backup_interval (int): Interval (in hours) between backups.
            retention_period (int): Retention period (in days) for backups to be kept.
            backup_location (str): File path where backups will be stored.
        
        Raises:
            ValueError: If any of the parameters are invalid.
            BackupConfigurationError: If there's an issue writing to the config file.
        """
        self.validate_parameters(backup_interval, retention_period, backup_location)

        self.backup_details = {
            "backup_interval": backup_interval,
            "retention_period": retention_period,
            "backup_location": backup_location,
        }

        self.save_configuration()

    def validate_parameters(self, backup_interval, retention_period, backup_location):
        """Validates the backup configuration parameters."""

        if not isinstance(backup_interval, int) or backup_interval <= 0:
            raise ValueError("Backup interval must be a positive integer.")
        
        if not isinstance(retention_period, int) or retention_period <= 0:
            raise ValueError("Retention period must be a positive integer.")

        if not os.path.isdir(backup_location):
            raise ValueError("Backup location must be a valid directory path.")

    def save_configuration(self):
        """Saves the backup configuration details to a file."""
        try:
            with open(self.CONFIG_FILE_PATH, 'w') as config_file:
                json.dump(self.backup_details, config_file, indent=4)
        except IOError as e:
            raise BackupConfigurationError(f"Failed to save backup configuration: {e}")

    def load_existing_configuration(self):
        """Loads an existing configuration from file if available."""
        if self.CONFIG_FILE_PATH.is_file():
            try:
                with open(self.CONFIG_FILE_PATH, 'r') as config_file:
                    self.backup_details = json.load(config_file)
            except (IOError, json.JSONDecodeError) as e:
                self.backup_details = None
                raise BackupConfigurationError(f"Failed to load existing backup configuration: {e}")

