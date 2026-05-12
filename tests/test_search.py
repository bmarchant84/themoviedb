from helpers.endpoints import SEARCH_MOVIE, SEARCH_TV
import os
import requests

# Test 1: Search movie by exact title returns the expected movie
def test_search_finds_exact_movie(client):
    # Searches for "The Godfather" and verifies it appears in the results.
    # Confirms search can locate well-known titles reliably.
    response = client.get(SEARCH_MOVIE, params={"query": "The Godfather"})
    titles = [movie["title"] for movie in response.json()["results"]]
    assert "The Godfather" in titles

# Test 2: Search with special characters does not break the API
def test_search_with_special_characters(client):
    # Sends a query with special characters and confirms a valid response.
    # Non-happy path: verifies the API handles unusual input without errors.
    response = client.get(SEARCH_MOVIE, params={"query": "!@#$%"})
    assert response.status_code == 200

# Test 3: Search supports pagination
def test_search_pagination(client):
    # Searches for a broad term and confirms page 2 returns different results than page 1.
    # Verifies that the search endpoint correctly supports paging.
    page1 = client.get(SEARCH_MOVIE, params={"query": "love", "page": 1}).json()["results"]
    page2 = client.get(SEARCH_MOVIE, params={"query": "love", "page": 2}).json()["results"]
    assert page1 != page2

# Test 4: Search with a nonsense query returns zero results
def test_search_nonsense_query_returns_no_results(client):
    # Sends a query unlikely to match any movie and expects an empty results list.
    # Confirms the API does not invent matches for irrelevant input.
    response = client.get(SEARCH_MOVIE, params={"query": "zzzqqqxxx123nonsense"})
    data = response.json()
    assert data["total_results"] == 0
    assert len(data["results"]) == 0

# Test 5: TV search returns relevant results
def test_search_tv_returns_results(client):
    # Searches the TV endpoint for "Breaking Bad" and confirms it is returned.
    # Validates that TV search functions and matches expected shows.
    response = client.get(SEARCH_TV, params={"query": "Breaking Bad"})
    names = [show["name"] for show in response.json()["results"]]
    assert "Breaking Bad" in names

# Test 6: Search results include required fields for UI display
def test_search_results_have_display_fields(client):
    # Verifies each search result has the fields a UI would need to display it.
    # Guards against missing data that would break downstream consumers.
    response = client.get(SEARCH_MOVIE, params={"query": "Matrix"})
    for movie in response.json()["results"]:
        assert "id" in movie
        assert "title" in movie
        assert "overview" in movie