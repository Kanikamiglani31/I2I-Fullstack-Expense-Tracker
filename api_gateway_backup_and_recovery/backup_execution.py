# api_gateway_backup_and_recovery/backup_execution.py

import os
import shutil
import logging
from datetime import datetime
from backup_configuration import BackupConfiguration
from logging import log_backup_activity

class BackupExecution:
    def __init__(self, config: BackupConfiguration):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.backup_location = config.get_backup_location()

        if not os.path.exists(self.backup_location):
            os.makedirs(self.backup_location)

    def execute_backup(self):
        """
        Runs the backup process based on the configuration set in backup_configuration.py.
        Ensures all configurations and logs are properly backed up.
        """
        try:
            start_time = datetime.now()
            self.logger.info(f"Backup process started at {start_time}")
            config_data = self.config.get_config_data()

            for data_path in config_data['data_paths']:
                if os.path.exists(data_path):
                    backup_dest = os.path.join(self.backup_location, os.path.basename(data_path))
                    shutil.copytree(data_path, backup_dest)
                    self.logger.info(f"Backed up {data_path} to {backup_dest}")
                else:
                    self.logger.warning(f"Data path {data_path} does not exist and will be skipped.")

            end_time = datetime.now()
            elapsed_time = end_time - start_time
            self.logger.info(f"Backup process completed at {end_time}, duration: {elapsed_time}")

            log_backup_activity("Backup completed successfully", start_time, end_time)

        except Exception as e:
            self.logger.error(f"Backup process failed: {str(e)}")
            log_backup_activity(f"Backup failed: {str(e)}", start_time, datetime.now())
            raise

# Example usage:
# Assuming backup_configuration is properly set

# from backup_configuration import BackupConfiguration

# config = BackupConfiguration()
# backup_executor = BackupExecution(config)
# backup_executor.execute_backup()
