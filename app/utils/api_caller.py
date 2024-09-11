import requests
import logging
from token_manager import TokenManager

class APIClient:
    """
    Handles API requests to external services.
    Uses a TokenManager to ensure valid authentication tokens.
    """

    def __init__(self, config_file='config.json'):
        """Initialize the API client by setting up TokenManager and loading API URL."""
        self.token_manager = TokenManager(config_file)
        self.config = self.token_manager.config
        self.api_url = self.config['api_url']

    def call_api(self, json_object: dict) -> dict:
        """
        Makes a POST request to the API with the given JSON payload.
        Adds the access token for authorization in the headers.
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.token_manager.get_access_token()}",
                "AI-Resource-Group": "default"
            }

            # Send the POST request with the given JSON object
            response = requests.post(self.api_url, json=json_object, headers=headers)
            response.raise_for_status()

            # Return the API response as a dictionary
            return response.json()

        except requests.RequestException as e:
            logging.error(f"Error calling API: {e}")
            raise
