# api_gateway_backup_and_recovery/recovery_configuration.py

import json
import os
import logging

# Constants for default recovery configuration
DEFAULT_RECOVERY_LOCATION = "/default/recovery/location"
DEFAULT_RECOVERY_STRATEGY = "incremental"

# Ensuring the log file is setup
logging.basicConfig(filename='recovery_configuration.log', level=logging.INFO)

def validate_recovery_configuration(config):
    """
    Validates the recovery configuration provided by the user.
    Config should contain required keys: 'recovery_location' and 'recovery_strategy'.
    """
    required_keys = ['recovery_location', 'recovery_strategy']
    if not all(key in config for key in required_keys):
        logging.error("Invalid configuration: Missing required keys.")
        raise ValueError(f"Configuration must include: {required_keys}")
    
    if not os.path.exists(config['recovery_location']):
        logging.error(f"Invalid recovery location: {config['recovery_location']} does not exist.")
        raise ValueError(f"Recovery location {config['recovery_location']} does not exist.")
    
    valid_strategies = ['full', 'incremental', 'differential']
    if config['recovery_strategy'] not in valid_strategies:
        logging.error(f"Invalid recovery strategy: {config['recovery_strategy']}. Must be one of {valid_strategies}.")
        raise ValueError(f"Recovery strategy must be one of {valid_strategies}.")

    logging.info("Recovery configuration validated successfully.")
    return True


def configure_recovery(recovery_location=None, recovery_strategy=None):
    """
    Sets up the recovery configuration for the API Gateway. Stores recovery location and recovery strategy.

    Parameters:
    recovery_location (str): Path to the recovery location.
    recovery_strategy (str): Strategy to use for recovery. Options: 'full', 'incremental', 'differential'.

    Returns:
    dict: Recovery configuration.
    """
    try:
        recovery_location = recovery_location or DEFAULT_RECOVERY_LOCATION
        recovery_strategy = recovery_strategy or DEFAULT_RECOVERY_STRATEGY
        
        logging.info(f"Setting recovery configuration with location: {recovery_location} "
                     f"and strategy: {recovery_strategy}")

        recovery_config = {
            'recovery_location': recovery_location,
            'recovery_strategy': recovery_strategy
        }

        # Validate the configuration provided
        validate_recovery_configuration(recovery_config)

        # If validation passes, save configuration to a file for persistence
        with open('recovery_config.json', 'w') as config_file:
            json.dump(recovery_config, config_file)

        logging.info("Recovery configuration successfully saved.")
        return recovery_config

    except Exception as e:
        logging.error(f"An error occurred while configuring recovery: {str(e)}")
        raise

# Example usage:
# try:
#     config = configure_recovery("/usr/local/recovery", "full")
#     print("Recovery Configured: ", config)
# except Exception as error:
#     print(f"Configuration failed: {error}")
