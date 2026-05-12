import pytest
import os
from dotenv import load_dotenv
from helpers.api_client import TMDBClient

load_dotenv()

@pytest.fixture
def client():
    base_url = os.getenv("TMDB_BASE_URL")
    api_key = os.getenv("TMDB_API_KEY")
    return TMDBClient(base_url, api_key)