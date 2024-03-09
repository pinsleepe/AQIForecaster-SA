import pandas as pd
from pathlib import Path
from loguru import logger


class FeatureEngineer:
    def __init__(self, data_path: Path):
        """
        Initialize the FeatureEngineer with long-format data.
        :param data: Path to the data folder.
        """
        self.data = pd.read_csv(data_path)
        self.data['datetime'] = pd.to_datetime(self.data['datetime'])
        self.engineered_data_path = None
        logger.info(f"Initialized FeatureEngineer with data from {data_path}")

    def add_time_features(self):
        """Adds time-based features to the data."""
        self.data['day_of_week'] = self.data['datetime'].dt.dayofweek
        self.data['is_weekend'] = self.data['day_of_week'] >= 5
        logger.debug("Added time-based features: day_of_week and is_weekend.")

    def add_lag_features(self, lag_periods):
        """Adds lag features for each time series based on 'parameter'."""
        pollutant_columns = ['no', 'no2', 'nox', 'o3']
        for column in pollutant_columns:
            for lag in lag_periods:
                lag_col_name = f'{column}_lag_{lag}'
                self.data[lag_col_name] = self.data[column].shift(lag)
                # Apply backward and forward fill
                self.data[lag_col_name] = self.data[lag_col_name].bfill().ffill()
        logger.debug(f"Added lag features for periods: {lag_periods}.")

    def add_rolling_window_features(self, window_size):
        """Adds rolling window features for each time series based on 'parameter'."""
        pollutant_columns = ['no', 'no2', 'nox', 'o3']
        for column in pollutant_columns:
            self.data[f'{column}_rolling_mean_{window_size}'] = self.data[column].rolling(
                window=window_size).mean().bfill().ffill()
            self.data[f'{column}_rolling_std_{window_size}'] = self.data[column].rolling(
                window=window_size).std().bfill().ffill()
            logger.debug(f"Added rolling window features with window size: {window_size}.")

    def save_engineered_data(self, file_path: Path):
        """
        Saves the engineered data to a CSV file.

        :param file_path: The file path where the data should be saved.
        """
        file_path = file_path / 'feature_data.csv'
        self.engineered_data_path = file_path
        print(f"Engineered data saved to {file_path}")
        pollutant_columns = ['no', 'no2', 'nox', 'o3']
        df_dropped = self.data.drop(columns=pollutant_columns)
        df_dropped.to_csv(file_path, index=False)
        logger.info(f"Engineered data saved to {self.engineered_data_path}")
