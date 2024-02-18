from pathlib import Path
import pandas as pd
import json
from loguru import logger


class DataProcessor:
    def __init__(self):
        # Initialize if there's any default state needed
        pass

    def parse_historical_data_csv(self, csv_file_path):
        """
        Parses historical AQI data from a CSV file using Path for path handling.

        :param csv_file_path: Path to the CSV file containing historical AQI data.
        :return: DataFrame containing the historical AQI data.
        """
        try:
            # Convert the string path to a Path object
            csv_path = Path(csv_file_path)
            df = pd.read_csv(csv_path)
            df['date'] = pd.to_datetime(df['date'])  # Ensure the date column is in datetime format
            logger.info(f"Historical data CSV parsed successfully from {csv_file_path}")
            return df
        except Exception as e:
            logger.error(f"Error parsing historical data CSV from {csv_file_path}: {e}")
            return None

    def parse_current_data_json(self, json_data):
        """
        Parses current AQI data from a JSON string or dictionary and converts it to a pandas DataFrame.

        :param json_data: JSON data containing current AQI information.
        :return: pandas DataFrame with the parsed current AQI data.
        """
        try:
            # If json_data is a string, convert it to a dictionary
            if isinstance(json_data, str):
                json_data = json.loads(json_data)

            # Extract the necessary information and prepare for DataFrame creation
            data = {
                'aqi': [json_data['data']['aqi']],
                'pm25': [json_data['data']['iaqi'].get('pm25', {}).get('v', None)],
                'pm10': [json_data['data']['iaqi'].get('pm10', {}).get('v', None)],
                'no2': [json_data['data']['iaqi'].get('no2', {}).get('v', None)],
                'so2': [json_data['data']['iaqi'].get('so2', {}).get('v', None)],
                'co': [json_data['data']['iaqi'].get('co', {}).get('v', None)],
                'timestamp': [json_data['data']['time']['s']]
            }

            # Create DataFrame
            df = pd.DataFrame(data)

            logger.info("Current data JSON parsed successfully into DataFrame.")
            return df
        except Exception as e:
            logger.error(f"Error parsing current data JSON into DataFrame: {e}")
            return None
