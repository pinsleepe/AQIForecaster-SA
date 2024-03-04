import pandas as pd


class FeatureEngineer:
    def __init__(self, data):
        """
        Initialize the FeatureEngineer with data.

        :param data: A pandas DataFrame containing the data for feature engineering.
        """
        self.data = data

    def add_time_features(self):
        """
        Adds time-based features to the data.

        This can include extracting parts of the date like day of the week,
        hour of the day, is_weekend, etc., which can be important for time series forecasting.
        """
        self.data['day_of_week'] = self.data['timestamp'].dt.dayofweek
        self.data['is_weekend'] = self.data['day_of_week'] >= 5
        # Add more time-based features as needed

    def add_lag_features(self, columns, lag_periods):
        """
        Adds lag features for specified columns.

        :param columns: List of column names to create lag features for.
        :param lag_periods: List of integers representing the lag periods to create.
        """
        for column in columns:
            for lag in lag_periods:
                self.data[f'{column}_lag_{lag}'] = self.data[column].shift(lag)

    def add_rolling_window_features(self, columns, window_size):
        """
        Adds rolling window features for specified columns.

        :param columns: List of column names to create rolling window features for.
        :param window_size: Integer representing the window size for the rolling calculation.
        """
        for column in columns:
            self.data[f'{column}_rolling_mean_{window_size}'] = self.data[column].rolling(window=window_size).mean()
            self.data[f'{column}_rolling_std_{window_size}'] = self.data[column].rolling(window=window_size).std()
            # Add more rolling window calculations as needed

    def get_engineered_data(self):
        """
        Returns the data with the engineered features.

        :return: A pandas DataFrame with the original and new engineered features.
        """
        return self.data
