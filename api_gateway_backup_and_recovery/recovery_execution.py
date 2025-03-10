# api_gateway_backup_and_recovery/recovery_execution.py

import os
import logging
from backup_verification import verify_backup
from recovery_configuration import configure_recovery
from logging import initialize_logging, log_recovery_activity

# Ensure logging is initialized
initialize_logging()

def execute_recovery(backup_path, recovery_path):
    """
    Runs the recovery process using the backups created. Ensures the system can be restored to its previous state without any data loss.

    Parameters:
        backup_path (str): The path where the backup data is stored.
        recovery_path (str): The path where the data should be recovered to.
    
    Returns:
        bool: True if recovery was successful, False otherwise.
    """
    try:
        log_recovery_activity("Recovery process started.")
        
        # Verify the backup before attempting recovery
        if not verify_backup(backup_path):
            log_recovery_activity("Backup verification failed. Recovery aborted.")
            return False

        # Configure recovery settings
        recovery_config = configure_recovery(recovery_path)
        
        if not recovery_config:
            log_recovery_activity("Recovery configuration failed. Recovery aborted.")
            return False

        # Perform the recovery by copying files from the backup path to the recovery path
        for root, dirs, files in os.walk(backup_path):
            for file in files:
                source_file = os.path.join(root, file)
                relative_path = os.path.relpath(source_file, backup_path)
                dest_file = os.path.join(recovery_path, relative_path)

                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                os.link(source_file, dest_file)
                log_recovery_activity(f"Recovered file {dest_file}")
        
        log_recovery_activity("Recovery process completed successfully.")
        return True

    except Exception as e:
        logging.error(f"An error occurred during recovery: {e}")
        log_recovery_activity(f"An error occurred during recovery: {e}")
        return False

