from pathlib import Path
import pandas as pd
from loguru import logger


# TODO use pandera for data quality checks
class DataProcessor:
    def __init__(self, location: Path):
        """
        Initialize the DataProcessor class.

        :param location: Path to the data directory.
        """
        self.location = location
        self.csv_files = self.location.glob('*.csv')
        self.aggregated_data_path = None

    def flatten_and_prepare_data(self, file_name: Path):
        """
        Reads a CSV file, flattens the data by aggregating to a daily resolution, keeping only the date part in 'datetime',
        and arranges the DataFrame with 'parameter', 'value', and 'datetime' columns.

        :param file_name: Path to the input CSV file.
        """
        file_path = self.location / file_name
        try:
            df = pd.read_csv(file_path)

            # Convert 'datetime' to datetime objects and extract just the date part
            df['datetime'] = pd.to_datetime(df['datetime']).dt.date

            # Ensure 'value' is numeric, coercing errors to NaN
            df['value'] = pd.to_numeric(df['value'], errors='coerce')

            # Drop rows where 'value' conversion to numeric failed (if any)
            df = df.dropna(subset=['value'])

            # Group by 'parameter' and 'datetime', then aggregate 'value' by mean
            df_daily = df.groupby(['parameter', 'datetime']).agg({'value': 'mean'}).reset_index()

            # Reorder the columns to match the desired output
            df_daily = df_daily[['datetime', 'parameter', 'value']]

            logger.info("Data has been flattened and prepared successfully.")
            logger.debug(f"\n{df_daily.head()}")  # Display the first few rows to verify structure

            return df_daily

        except Exception as e:
            logger.error(f"Error in processing data: {e}", exc_info=True)

    def process_all_csv_files(self):
        """
        Loops through all CSV files, applies flatten_and_prepare_data to each, and concatenates them into a final DataFrame.
        """
        all_dfs = []  # List to hold all the DataFrames

        for file_path in self.csv_files:
            df = self.flatten_and_prepare_data(file_path)
            if not df.empty:
                all_dfs.append(df)
                logger.info(f"Processed file {file_path}")

        # Concatenate all DataFrames if any exist
        if all_dfs:
            final_df = pd.concat(all_dfs, ignore_index=True)
            # Save the final DataFrame to CSV
            final_csv_path = self.location / 'final_aggregated_data.csv'
            self.aggregated_data_path = final_csv_path
            final_df.to_csv(final_csv_path, index=False)
            logger.info(f"Final aggregated data saved to {final_csv_path}")
        else:
            logger.info("No data files were processed.")

    def create_parameter_timeseries(self):
        # Read the CSV data into a DataFrame

        df = pd.read_csv(self.aggregated_data_path)

        # Convert 'datetime' column to datetime type
        df['datetime'] = pd.to_datetime(df['datetime'])

        # Pivot the DataFrame to have 'datetime' as index, 'parameter' as columns, and 'value' as cell values
        timeseries_df = df.pivot(index='datetime', columns='parameter', values='value')
        final_csv_path = self.location / 'timeseries_data.csv'
        timeseries_df.to_csv(final_csv_path)
