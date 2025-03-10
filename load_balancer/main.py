# load_balancer/main.py

import logging
from config import load_configurations, validate_configurations
from balancer import distribute_requests, monitor_instances

# Initialize the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_load_balancer(config_path):
    """
    This function will initialize the load balancer configuration and prepare it
    to start managing requests. It will set up the necessary services and 
    instances configurations needed for load balancing across microservices.
    
    :param config_path: Path to the configuration file
    """
    try:
        # Load the configurations
        config = load_configurations(config_path)
        
        # Validate the loaded configurations
        validate_configurations(config)
        
        logger.info("Load balancer initialized with configurations from %s", config_path)
        
    except Exception as e:
        logger.error("Failed to initialize load balancer: %s", str(e))
        raise


def start_load_balancer():
    """
    This function will commence the load balancing process. It will use the 
    initialized settings to distribute requests across available instances ensuring
    even distribution and handling of requests.
    """
    try:
        logger.info("Starting load balancer...")
        
        # Start monitoring instances
        monitor_instances()
        
        # Start distributing requests
        distribute_requests()
        
        logger.info("Load balancer started.")

    except Exception as e:
        logger.error("Failed to start load balancer: %s", str(e))
        raise

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) != 2:
        logger.error("Usage: python main.py <config_path>")
        sys.exit(1)

    config_path = sys.argv[1]
    initialize_load_balancer(config_path)
    start_load_balancer()
