import requests
import os

class TMDBClient:
    def __init__(self, base_url, api_key):
        self.base_url = base_url
        self.api_key = api_key

    def get(self, endpoint, params=None):
        if params is None:
            params = {}
        params["api_key"] = self.api_key
        url = f"{self.base_url}{endpoint}"
        response = requests.get(url, params=params)
        return response