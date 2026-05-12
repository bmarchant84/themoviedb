# TMDB API Test Suite

An automated API test suite built with **Pytest** that validates endpoints from [The Movie Database (TMDB)](https://www.themoviedb.org/) REST API. Designed as a clean, maintainable framework that can serve as a template for future API testing projects.

## Overview

This project demonstrates how to build a production-quality API test suite from scratch using Python and Pytest. It covers happy path scenarios, non-happy path edge cases, schema validation, and pagination across multiple endpoints (movies, TV, and search).

## Tech Stack

- **Python 3** – core language
- **Pytest** – test framework
- **Requests** – HTTP client for API calls
- **python-dotenv** – loads environment variables from a `.env` file so credentials are never hardcoded

## Project Structure

```
themoviedb/
├── helpers/
│   ├── api_client.py      # Reusable HTTP client class (TMDBClient)
│   └── endpoints.py       # All endpoint paths in one place
├── tests/
│   ├── test_movies.py     # Movie endpoint tests (popular, details, search)
│   ├── test_search.py     # Search endpoint tests (movies and TV)
│   └── test_tv.py         # TV endpoint tests (popular, top rated, details)
├── conftest.py            # Shared Pytest fixtures
├── .env                   # API key and base URL (not committed)
├── .gitignore             # Excludes .env, venv, and cache files
└── README.md
```

## Design Principles

### Abstraction
Tests do not make raw HTTP calls. Instead, every test uses the `TMDBClient` class from `helpers/api_client.py`, which centralizes auth, base URL configuration, and request handling. If TMDB ever changes how authentication works, only one file needs updating.

### Separation of concerns
- **Endpoints** live in `helpers/endpoints.py` so URLs are never hardcoded inside tests
- **Configuration** lives in `.env` so the API key and base URL are not hardcoded anywhere
- **Fixtures** live in `conftest.py` so setup logic is shared across all test files

### Maintainability
Tests are organized by feature area (movies, search, TV) so the suite can grow without becoming chaotic. Adding a new endpoint takes minutes, not hours.

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/themoviedb.git
cd themoviedb
```

### 2. Create and activate a virtual environment

Mac/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install pytest requests python-dotenv
```

### 4. Create your `.env` file

Get a free API key from [TMDB](https://www.themoviedb.org/settings/api), then create a `.env` file in the project root:

```
TMDB_API_KEY=your_api_key_here
TMDB_BASE_URL=https://api.themoviedb.org/3
```

The `.env` file is excluded from version control via `.gitignore`, so your key stays private.

## Running the Tests

Run the entire suite:

```bash
pytest -v
```

Run a single test file:

```bash
pytest tests/test_movies.py -v
```

Run a single test by name:

```bash
pytest -v -k "test_invalid_api_key_returns_401"
```

## Test Coverage

The suite includes 20+ tests across three categories:

### Happy path
- Endpoint reachability (200 responses)
- Correct payload structure (`results` array, required fields)
- Known data validation (specific movie and TV titles return correctly)
- Pagination works across pages

### Non-happy path
- Invalid API key returns 401 Unauthorized
- Nonexistent movie or TV ID returns 404 Not Found
- Empty search query is handled gracefully
- Search with special characters does not break the API
- Nonsense search queries return zero results (no false positives)

### Schema and contract
- Each result contains the fields a UI consumer would require
- Numeric fields (like `vote_average`) are returned as numbers, not strings
- Top rated content actually meets a quality threshold

## Cleanup

This suite does not require teardown because all tests use `GET` requests against a read-only public API. JSON responses are scoped to each test function and garbage collected automatically by Python.

If this suite were extended to test `POST`, `PUT`, or `DELETE` endpoints, cleanup would be handled using Pytest's `yield` fixture pattern: create the resource in setup, yield it to the test, then delete it during teardown.

## What This Project Demonstrates

- Writing maintainable, abstracted API tests in Pytest
- Using fixtures and `conftest.py` to share setup logic
- Loading credentials from environment variables (never hardcoded)
- Organizing tests by feature area for scalability
- Covering happy and non-happy path scenarios
- Validating both response status and response payload structure
