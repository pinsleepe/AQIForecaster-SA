from loguru import logger
from aqiforecaster_sa.data_fetcher import ArchivalDataFetcher
from aqiforecaster_sa.config_manager import ConfigManager
from aqiforecaster_sa.data_processor import DataProcessor
from aqiforecaster_sa.feature_engineer import FeatureEngineer
from pathlib import Path
from aqiforecaster_sa.file_handler import FileHandler
from aqiforecaster_sa.utils import create_iaqi_filename

logger.add("aq_logs.log", rotation="10 MB")

config_manager = ConfigManager('config.json')
bucket_name = config_manager.get_config_value('bucket_name')
location_id = config_manager.get_config_value('location_id')

base_path = Path(__file__).parent / 'data'
fetcher = ArchivalDataFetcher(base_path, bucket_name, location_id)
fetcher.download_data('2024', '01')
fetcher.unzip_file()


# base_path = Path(__file__).parent
# file_name = create_iaqi_filename(station_id)
# file_path = base_path / 'data' / file_name
# file_handler = FileHandler(file_path)
# file_handler.write_json(current_aqi_data)

# processor = DataProcessor()
# historical_data_csv_path = config_manager.get_config_value('historical_aqi_data')
#
# # Process historical data
# historical_df = processor.parse_historical_data_csv(historical_data_csv_path)
# if historical_df is not None:
#     logger.info("Historical data processed successfully. Here are the first 5 rows:")
#     logger.info(historical_df.head(5))
# else:
#     logger.error("Failed to process historical data.")

# Process current data
# processor = DataProcessor(current_aqi_data)
# try:
#     logger.info("Current AQI data processed successfully into DataFrame.")
#     logger.info(f"Here are the details: {processor.extract_current_data()}")
# except Exception as e:
#     logger.error(f"Failed to process current AQI data into DataFrame with error {e}.")

# # Initialize the feature engineer with your data
# engineer = FeatureEngineer(historical_df)
#
# # Add desired features
# engineer.add_time_features()
# engineer.add_lag_features(columns=['pm25', 'pm10'], lag_periods=[1, 2, 3])
# engineer.add_rolling_window_features(columns=['pm25', 'pm10'], window_size=7)
#
# # Retrieve the data with engineered features
# df_engineered = engineer.get_engineered_data()
#
# # Log the head of the engineered data frame to demonstrate successful feature engineering
# logger.info("Feature engineering completed successfully. Here are the first 5 rows of the engineered data:")
# logger.info(df_engineered.head())
#
# except Exception as e:
# logger.exception("An error occurred during the AQI data fetching, processing, and feature engineering.")
