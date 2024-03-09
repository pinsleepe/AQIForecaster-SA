import gzip

import boto3
from botocore import UNSIGNED
from botocore.config import Config
from loguru import logger
from pathlib import Path


# https://docs.openaq.org/docs/accessing-openaq-archive-data

class ArchivalDataFetcher:
    def __init__(self, destination: Path, bucket_name='openaq-data-archive', location_id='225454'):
        self.bucket_name = bucket_name
        self.location_id = location_id
        # Configure the S3 client for unsigned (anonymous) requests
        self.s3_client = boto3.client('s3',
                                      config=Config(signature_version=UNSIGNED))
        self.destination = destination
        logger.info(f"ArchivalDataFetcher initialized with destination: "
                    f"{destination} and location_id: {location_id}")

    def download_data(self, year, month):
        """
        Downloads data for the specified location, year, and month to the destination.

        :param year: Year of the data to download.
        :param month: Month of the data to download.
        :param destination: Path to save the downloaded data.
        """
        # Ensure the destination directory exists
        self.destination.mkdir(parents=True, exist_ok=True)
        # Format the S3 key prefix
        key_prefix = f'records/csv.gz/locationid={self.location_id}/year={year}/month={month}/'
        paginator = self.s3_client.get_paginator('list_objects_v2')
        logger.debug(f"Starting download for year: {year}, month: {month}")
        try:
            for page in paginator.paginate(Bucket=self.bucket_name, Prefix=key_prefix):
                for item in page.get('Contents', []):
                    file_key = item['Key']
                    file_name = file_key.split('/')[-1]
                    local_file_path = self.destination / file_name

                    # Download the file
                    self.s3_client.download_file(self.bucket_name, file_key, str(local_file_path))
                    logger.info(f"Downloaded {file_key} to {local_file_path}")

        except Exception as e:
            logger.info(f"An error occurred: {e}")

    def unzip_file(self):
        """
        Unzips all .gz files in a given directory, saves the uncompressed data in the same location,
        and then deletes the original .gz files.

        :param directory: The directory containing .gz files to be unzipped.
        """
        gz_files = self.destination.glob('*.gz')
        logger.debug(f"Starting to unzip files in {self.destination}")
        for gz_file in gz_files:
            # Define the output filename by removing '.gz' from the original filename
            output_file = gz_file.with_suffix('')

            # Open the gzipped file and read the decompressed content
            with gzip.open(gz_file, 'rb') as f_in:
                # Write the decompressed content to a new file
                with open(output_file, 'wb') as f_out:
                    f_out.write(f_in.read())
                    logger.info(f"Decompressed and saved {output_file}")

            # Delete the original gzipped file
            gz_file.unlink()
            logger.info(f"Deleted original file {gz_file}")
