# load_balancer/config.py

import json
import os

CONFIG_FILE_PATH = 'config/config.json'  # Assumes configs are in JSON format in specified directory

class ConfigError(Exception):
    """Custom exception for configuration errors."""
    pass

def load_configurations():
    """
    This function will load configuration settings related to microservices and their instances. 
    It will be responsible for defining the services and how they should be balanced.
    """
    try:
        if not os.path.isfile(CONFIG_FILE_PATH):
            raise ConfigError(f"Configuration file not found at {CONFIG_FILE_PATH}")
        
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            configs = json.load(config_file)
        
        # Example format: {'services': [{'name': 'svc1', 'instances': ['url1', 'url2']}, ...]}
        if 'services' not in configs:
            raise ConfigError("Missing 'services' key in configuration.")
        
        return configs
    
    except json.JSONDecodeError as e:
        raise ConfigError(f"Error parsing the configuration file: {e}")
    except Exception as e:
        raise ConfigError(f"An error occurred while loading configurations: {e}")

def validate_configurations(configs):
    """
    This function will ensure that all loaded configurations follow the required specifications 
    for the load balancer to function optimally. It will check for misconfigurations and report any issues.
    """
    try:
        # Check if configurations contain required keys
        if not isinstance(configs, dict) or 'services' not in configs:
            raise ConfigError("Configurations must include a 'services' key with service details.")

        services = configs['services']
        
        if not isinstance(services, list):
            raise ConfigError("'services' should be a list of service definitions.")
        
        for service in services:
            if not isinstance(service, dict):
                raise ConfigError("Each service definition should be a dictionary.")
            
            if 'name' not in service or 'instances' not in service:
                raise ConfigError("Each service must have 'name' and 'instances' defined.")
            
            if not isinstance(service['instances'], list) or len(service['instances']) == 0:
                raise ConfigError(f"Service '{service['name']}' must have a non-empty list of 'instances'.")
        
        return True
    
    except ConfigError as e:
        print(f"Configuration validation failed: {e}")
        return False

# Example usage
if __name__ == '__main__':
    try:
        configs = load_configurations()
        if validate_configurations(configs):
            print("Configurations loaded and validated successfully.")
        else:
            print("There were issues validating the configurations.")
    except ConfigError as e:
        print(str(e))
