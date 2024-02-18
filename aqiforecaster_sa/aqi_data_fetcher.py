import requests


class AQIDataFetcher:
    def __init__(self, api_key, base_url):
        self.base_url = base_url
        self.api_key = api_key

    def get_current_aqi(self, station_id):
        """Fetch current AQI data for a specified station ID."""
        endpoint = f"/feed/@{station_id}/"  # Adjusted to use station ID
        params = {'token': self.api_key}
        response = self._make_request(endpoint, params)
        return response

    def get_historical_aqi(self, city, start_date, end_date):
        """Fetch historical AQI data. This is a placeholder; actual implementation may vary."""
        # Note: The AQICN API might not support direct fetching of historical data through the API.
        # You may need to store daily data fetched using get_current_aqi and compile it for historical analysis.
        print("Historical data fetching not implemented.")
        return None

    def get_forecast_data(self, city):
        """Fetch forecast AQI data. This is a placeholder; actual implementation may vary."""
        # Forecast data might not be directly available or may be part of the current AQI data response.
        # Adjust this method based on the actual data structure and availability.
        print("Forecast data fetching not implemented.")
        return None

    def _make_request(self, endpoint, params):
        """Private method to make HTTP requests to the AQICN API."""
        try:
            url = self.base_url + endpoint
            response = requests.get(url, params=params)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")
        return None
