from helpers.endpoints import POPULAR_TV, TOP_RATED_TV
import os
import requests

# Test 1: Popular TV endpoint returns 200
def test_popular_tv_returns_200(client):
    # Verifies the popular TV shows endpoint is reachable and returning success.
    # Core smoke test for the TV side of the API.
    response = client.get(POPULAR_TV)
    assert response.status_code == 200

# Test 2: Popular TV response contains a results list
def test_popular_tv_has_results(client):
    # Confirms the response body contains a "results" array with at least one show.
    # Verifies the documented payload structure is returned.
    response = client.get(POPULAR_TV)
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0

# Test 3: Each TV show has the expected fields
def test_popular_tv_fields_present(client):
    # Verifies each TV result has the fields a consumer would depend on.
    # TV uses "name" and "first_air_date" instead of "title" and "release_date".
    response = client.get(POPULAR_TV)
    for show in response.json()["results"]:
        assert "id" in show
        assert "name" in show
        assert "first_air_date" in show

# Test 4: Top rated TV shows have a vote_average present
def test_top_rated_tv_has_ratings(client):
    # Confirms each top rated show includes a vote_average field.
    # Required since this endpoint is specifically about ratings.
    response = client.get(TOP_RATED_TV)
    for show in response.json()["results"]:
        assert "vote_average" in show
        assert isinstance(show["vote_average"], (int, float))

# Test 5: Top rated shows are actually highly rated
def test_top_rated_tv_ratings_are_high(client):
    # Verifies top rated shows have ratings above a reasonable threshold.
    # Sanity check that the endpoint is returning genuinely top rated content.
    response = client.get(TOP_RATED_TV)
    for show in response.json()["results"]:
        assert show["vote_average"] >= 7.0

# Test 6: TV details endpoint returns the correct show
def test_tv_details_returns_correct_show(client):
    # Fetches details for Breaking Bad (ID 1396) and confirms the name matches.
    # Validates the details endpoint returns accurate data for a known show.
    response = client.get("/tv/1396")
    data = response.json()
    assert data["name"] == "Breaking Bad"

# Test 7: TV details for nonexistent ID returns 404
def test_invalid_tv_id_returns_404(client):
    # Requests details for a TV ID that does not exist.
    # Non-happy path: confirms the API returns a proper not found error.
    response = client.get("/tv/999999999")
    assert response.status_code == 404