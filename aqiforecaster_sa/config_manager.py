from loguru import logger
import json


class ConfigManager:
    """
    A configuration manager class to handle loading and accessing
    configuration data from a JSON file.
    """

    def __init__(self, config_file_path):
        """
        Initialize the configuration manager with the given config file path.

        Parameters:
        - config_file_path: A string path to the configuration JSON file.
        """
        self.config_file_path = config_file_path
        self.config_data = self.load_config()

    def load_config(self):
        """
        Load the configuration data from the JSON file specified at initialization.

        Returns:
        - A dictionary containing the configuration data.
        """
        try:
            with open(self.config_file_path, 'r') as file:
                config_data = json.load(file)
                logger.info("Configuration file loaded successfully.")
                return config_data
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_file_path}")
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON from the configuration file: {self.config_file_path}")
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
        return {}

    def get_config_value(self, key):
        """
        Retrieve a configuration value for a given key.

        Parameters:
        - key: A string representing the key in configuration data to retrieve.

        Returns:
        - The value from the configuration data associated with the key, or None if the key is not found.
        """
        value = self.config_data.get(key)
        if value is not None:
            logger.info(f"Retrieved value for key: {key}")
            return value
        else:
            logger.warning(f"No value found for key: {key}")
            return None
