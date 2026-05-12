from helpers.endpoints import POPULAR_MOVIES, SEARCH_MOVIE
import os
import requests

# Test 1: Popular Movies Endpoints returns 200
def test_popular_movies_returns_200(client):
    # Core smoke test, if this fails, the API is likely down or the endpoint has changed
    response = client.get(POPULAR_MOVIES)
    assert response.status_code == 200

# Test 2: Populare Movies endpoint returns results
def test_popular_movies_returns_results(client):
    response = client.get(POPULAR_MOVIES)
    data = response.json()
    assert "results" in data
    assert len(data["results"]) > 0

# Test 3: Each movie in popular list has required fields
def test_popular_movies_required_fields(client):
    response = client.get(POPULAR_MOVIES)
    data = response.json()
    for movie in data["results"]:
        assert "id" in movie
        assert "title" in movie
        assert "release_date" in movie
        assert "overview" in movie

# Test 4: Movie details returns the correct movie
def test_movie_details_correct_title(client):
    # Fetches details for The Dark Knight (ID 155) and confirms the title matches.
    # Validates that the details endpoint returns accurate data for a known movie.
    response = client.get("/movie/155")
    data = response.json()
    assert data["title"] == "The Dark Knight"

# Test 5: Search returns relevant results for a known title
def test_search_movie_returns_results(client):
    # Searches for "Inception" and verifies at least one result is returned.
    # Confirms basic search functionality is working end to end.
    response = client.get(SEARCH_MOVIE, params={"query": "Inception"})
    data = response.json()
    assert data["total_results"] > 0

# Test 6: Invalid API key returns 401
def test_invalid_api_key_returns_401():
    # Sends a request with a bad API key and expects 401 Unauthorized.
    # Non-happy path: verifies authentication is being enforced by the API.
    base_url = os.getenv("TMDB_BASE_URL")
    response = requests.get(
        f"{base_url}{POPULAR_MOVIES}",
        params={"api_key": "invalid_key_123"}
    )
    assert response.status_code == 401

# Test 7: Search with an empty query is handled gracefully
def test_search_empty_query(client):
    # Sends a search request with an empty query string.
    # Non-happy path: verifies the API handles missing required params without crashing.
    response = client.get(SEARCH_MOVIE, params={"query": ""})
    assert response.status_code in [200, 422]

# Test 8: Movie details for a nonexistent ID returns 404
def test_invalid_movie_id_returns_404(client):
    # Requests details for a movie ID that does not exist.
    # Non-happy path: confirms the API returns a proper not found error.
    response = client.get("/movie/999999999")
    assert response.status_code == 404

# Test 9: Pagination returns different results across pages
def test_popular_movies_page_2(client):
    # Fetches page 1 and page 2 of popular movies and confirms they differ.
    # Verifies pagination is functioning and not returning duplicate data.
    page1 = client.get(POPULAR_MOVIES, params={"page": 1}).json()["results"]
    page2 = client.get(POPULAR_MOVIES, params={"page": 2}).json()["results"]
    assert page1 != page2

# Test 10: Search results actually match the query term
def test_search_results_match_query(client):
    # Searches for "Batman" and confirms at least one result contains it in the title.
    # Confirms the search endpoint returns relevant results, not random ones.
    response = client.get(SEARCH_MOVIE, params={"query": "Batman"})
    titles = [movie["title"] for movie in response.json()["results"]]
    assert any("Batman" in title for title in titles)