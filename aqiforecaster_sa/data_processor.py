from pathlib import Path
import pandas as pd
import json
from loguru import logger
from requests import Response


class DataProcessor:
    def __init__(self, json_response: Response):
        self.data = json_response

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

    def extract_current_data(self):
        # Extract the date and air quality data
        date = self.data['data']['time']['iso'].split('T')[0]  # Extracting the date part
        pm25 = self.data['data']['iaqi'].get('pm25', {}).get('v', '')
        pm10 = self.data['data']['iaqi'].get('pm10', {}).get('v', '')
        no2 = self.data['data']['iaqi'].get('no2', {}).get('v', '')
        so2 = self.data['data']['iaqi'].get('so2', {}).get('v', '')
        co = self.data['data']['iaqi'].get('co', {}).get('v', '')

        return {
            "date": date,
            "pm25": pm25,
            "pm10": pm10,
            "no2": no2,
            "so2": so2,
            "co": co
        }