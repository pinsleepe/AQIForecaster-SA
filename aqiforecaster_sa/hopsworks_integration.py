import hopsworks
import pandas as pd
from aqiforecaster_sa.config_manager import ConfigManager
from loguru import logger


class FeatureStoreManager:
    def __init__(self, config_manager: ConfigManager, feature_data_path):
        self.config_manager = config_manager
        self.feature_data_path = feature_data_path
        self.project = None
        self.fs = None
        self.trans_fg = None

    def login_to_hopsworks(self):
        self.project = hopsworks.login(api_key_value=self.config_manager.get_config_value('hopsworks_api_key'))
        self.fs = self.project.get_feature_store()

    def get_or_create_feature_group(self):
        self.trans_fg = self.fs.get_or_create_feature_group(
            name="air_quality_forecast_batch_fg",
            version=1,
            description="Air quality data with time-based, lag, and rolling window features for pollutants.",
            primary_key=["datetime"],
            event_time="datetime",
        )

    def update_feature_descriptions(self):
        feature_descriptions = self.generate_feature_descriptions()
        for desc in feature_descriptions:
            self.trans_fg.update_feature_description(desc["name"], desc["description"])

    def generate_feature_descriptions(self):
        feature_descriptions = [
            {"name": "datetime", "description": "Reference time for the data observation"},
            {"name": "day_of_week", "description": "Day of the week extracted from the datetime"},
            {"name": "is_weekend", "description": "Boolean indicating if the day is a weekend"},
        ]
        pollutant_columns = ['no', 'no2', 'nox', 'o3']
        lag_periods = [1, 2, 3]
        window_sizes = [3]

        for column in pollutant_columns:
            for lag in lag_periods:
                feature_descriptions.append(
                    {"name": f"{column}_lag_{lag}",
                     "description": f"Lag of {lag} period(s) for {column} pollutant levels"}
                )
            for window_size in window_sizes:
                feature_descriptions.append(
                    {"name": f"{column}_rolling_mean_{window_size}",
                     "description": f"Rolling mean of the past {window_size} periods for {column} pollutant levels"}
                )
                feature_descriptions.append(
                    {"name": f"{column}_rolling_std_{window_size}",
                     "description": f"Rolling standard deviation of the past {window_size} periods for {column} pollutant levels"}
                )
        return feature_descriptions

    def insert_data(self):
        trans_df = pd.read_csv(self.feature_data_path)
        trans_df['datetime'] = pd.to_datetime(trans_df['datetime'])
        self.trans_fg.insert(trans_df)
