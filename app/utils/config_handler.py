import json
import logging

def load_config(config_file: str) -> dict:
    """Load configuration from a JSON file."""
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            logging.info("Configuration loaded successfully.")
            return config
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_file}' not found.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON from the configuration file: {e}")
        raise


def save_config(config: dict, config_file: str) -> None:
    """
    Save configuration to a JSON file.
    Overwrites the file with the new configuration in a human-readable format.
    """
    try:
        with open(config_file, 'w') as file:
            json.dump(config, file, indent=4)
            logging.info("Configuration saved successfully.")
    except IOError as e:
        logging.error(f"Error saving configuration file: {e}")
        raise
