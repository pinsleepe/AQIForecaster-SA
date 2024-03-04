from datetime import datetime

def create_iaqi_filename(station_id, timestamp_format='%Y%m%d%H%M%S'):
    """
    Generates a filename for IAQI data that includes a station ID and the current timestamp.

    :param station_id: The station ID to include in the filename.
    :param timestamp_format: The format string for the timestamp. Defaults to 'YYYYMMDDHHMMSS'.
    :return: A string representing the filename.
    """
    # Get the current time for the timestamp
    current_time = datetime.now()
    # Format the timestamp
    timestamp_str = current_time.strftime(timestamp_format)
    # Create the filename
    filename = f"iaqi_data_{station_id}_{timestamp_str}.json"
    return filename