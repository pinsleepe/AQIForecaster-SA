import json


class ConfigManager:
    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.config_data = self.load_config()

    def load_config(self):
        """Load configuration from a JSON file."""
        try:
            with open(self.config_file_path, 'r') as file:
                config_data = json.load(file)
                return config_data
        except FileNotFoundError:
            print(f"Configuration file not found: {self.config_file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from the configuration file: {self.config_file_path}")
        return {}

    def get_config_value(self, key):
        """Retrieve a configuration value by key."""
        return self.config_data.get(key, None)
