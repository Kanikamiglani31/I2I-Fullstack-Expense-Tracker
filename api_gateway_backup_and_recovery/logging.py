import logging
import os
from datetime import datetime

# Constants
LOG_DIR = "logs"
BACKUP_LOG_FILE = "backup.log"
RECOVERY_LOG_FILE = "recovery.log"

# Ensure the logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def initialize_logging():
    """
    Sets up a logging system to track backup and recovery processes.
    Creates separate log files for backup activities and recovery activities.
    """
    logger = logging.getLogger('BackupRecoveryLogger')
    logger.setLevel(logging.DEBUG)

    # Backup logging configuration
    backup_handler = logging.FileHandler(os.path.join(LOG_DIR, BACKUP_LOG_FILE), mode='a')
    backup_handler.setLevel(logging.DEBUG)
    backup_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    backup_handler.setFormatter(backup_format)
    logger.addHandler(backup_handler)

    # Recovery logging configuration
    recovery_handler = logging.FileHandler(os.path.join(LOG_DIR, RECOVERY_LOG_FILE), mode='a')
    recovery_handler.setLevel(logging.DEBUG)
    recovery_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    recovery_handler.setFormatter(recovery_format)
    logger.addHandler(recovery_handler)

    return logger

def log_backup_activity(activity, status, logger):
    """
    Logs activities related to backup execution including timestamps and status.
    
    Parameters:
    - activity: Description of the backup activity.
    - status: Status of the backup activity (e.g., "success", "failure").
    - logger: The logging object used for writing the log entry.
    """
    log_message = f"Backup Activity: {activity} - Status: {status}"
    if status.lower() == "success":
        logger.info(log_message)
    else:
        logger.error(log_message)

def log_recovery_activity(activity, status, logger):
    """
    Logs activities related to recovery execution including timestamps and status.
    
    Parameters:
    - activity: Description of the recovery activity.
    - status: Status of the recovery activity (e.g., "success", "failure").
    - logger: The logging object used for writing the log entry.
    """
    log_message = f"Recovery Activity: {activity} - Status: {status}"
    if status.lower() == "success":
        logger.info(log_message)
    else:
        logger.error(log_message)

# Example usage
if __name__ == "__main__":
    # Initialize the logging system
    logger = initialize_logging()
    
    # Log some example activities
    log_backup_activity("Backup started", "success", logger)
    log_backup_activity("Backup failed due to network error", "failure", logger)
    log_recovery_activity("Recovery process initiated", "success", logger)
    log_recovery_activity("Recovery failed due to missing files", "failure", logger)
