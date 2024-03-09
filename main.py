from loguru import logger
from aqiforecaster_sa.data_fetcher import ArchivalDataFetcher
from aqiforecaster_sa.config_manager import ConfigManager
from aqiforecaster_sa.data_processor import DataProcessor
from aqiforecaster_sa.feature_engineer import FeatureEngineer
from pathlib import Path

from aqiforecaster_sa.hopsworks_integration import FeatureStoreManager

logger.add("aq_logs.log", rotation="10 MB")

config_manager = ConfigManager('config.json')
bucket_name = config_manager.get_config_value('bucket_name')
location_id = config_manager.get_config_value('location_id')

base_path = Path(__file__).parent / 'data'
fetcher = ArchivalDataFetcher(base_path, bucket_name, location_id)
fetcher.download_data('2024', '01')
fetcher.unzip_file()

processor = DataProcessor(base_path)
processor.process_all_csv_files()
processor.create_parameter_timeseries()

engineer = FeatureEngineer(processor.timeseries_data_path)
engineer.add_time_features()
engineer.add_lag_features([1, 2, 3])
engineer.add_rolling_window_features(3)
engineer.save_engineered_data(base_path)

feature_store_manager = FeatureStoreManager(config_manager, engineer.engineered_data_path)
feature_store_manager.login_to_hopsworks()
feature_store_manager.get_or_create_feature_group()
feature_store_manager.update_feature_descriptions()
feature_store_manager.insert_data()
