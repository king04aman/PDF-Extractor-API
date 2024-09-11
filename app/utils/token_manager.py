import requests
import logging
from datetime import datetime, timedelta, timezone
from config_handler import load_config, save_config

class TokenManager:
    """
    Handles token retrieval and caching.
    Responsible for refreshing the token if expired and managing expiration time.
    """

    def __init__(self, config_file='config.json'):
        """Initialize TokenManager by loading the API credentials from the config file."""
        self.config = load_config(config_file)
        self.config_file = config_file
        self.client_id = self.config['client_id']
        self.client_secret = self.config['client_secret']
        self.url_auth = self.config['url_auth']

    def get_access_token(self) -> str:
        """
        Get the current access token.
        If the token is cached and valid, return it. Otherwise, refresh it.
        """
        current_time = datetime.now(timezone.utc)

        # Check if the cached token is still valid
        if 'access_token' in self.config and 'expires_at' in self.config:
            expires_at = datetime.fromisoformat(self.config['expires_at'])
            if current_time < expires_at:
                logging.info("Using cached access token.")
                return self.config['access_token']

        # If the token is expired or missing, refresh it
        return self._refresh_token()

    def _refresh_token(self) -> str:
        """
        Refresh the access token by making a request to the authentication server.
        Updates the config with the new token and expiration time.
        """
        try:
            # Make a POST request to the authentication URL
            response = requests.post(self.url_auth, data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            })
            response.raise_for_status()

            # Parse response and update configuration
            token_data = response.json()
            self.config['access_token'] = token_data['access_token']
            self.config['expires_at'] = (datetime.now(timezone.utc) + timedelta(seconds=token_data['expires_in'])).isoformat()
            save_config(self.config, self.config_file)
            
            logging.info("Access token refreshed successfully.")
            return token_data['access_token']

        except requests.RequestException as e:
            logging.error(f"Error obtaining access token: {e}")
            raise
