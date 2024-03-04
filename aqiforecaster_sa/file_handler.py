from loguru import logger
import json
from pathlib import Path
from requests import Response


class FileHandler:
    def __init__(self, file_path: str):
        """
        A file handler class for reading and writing JSON files using pathlib.

        :param file_path: The path to the JSON file as a string or Path object.
        """
        self.file_path = Path(file_path)

    def read_json(self) -> dict:
        """
        Reads a JSON file and logs the action.

        :return: A dictionary with the JSON content.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"JSON file read successfully: {self.file_path}")
                return data
        except FileNotFoundError:
            logger.error(f"JSON file not found: {self.file_path}")
            raise
        except json.JSONDecodeError:
            logger.error(f"Error decoding JSON file: {self.file_path}")
            raise
        except Exception as e:
            logger.error(f"An unexpected error occurred while reading the JSON file: {e}")
            raise

    def write_json(self, response: Response, indent=4):
        """
        Writes a dictionary to a JSON file and logs the action.

        :param response: The Response object to extract and write as JSON.
        :param indent: The indentation level for the JSON file.
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(response, file, ensure_ascii=False, indent=indent)
                logger.info(f"JSON file written successfully: {self.file_path}")
        except Exception as e:
            logger.error(f"Error writing to the JSON file at {self.file_path}: {e}")
            raise
