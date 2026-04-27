# FastAPI Backend Tests

This directory contains tests for the Mergington High School Activities API backend.

## Dependencies

The tests require the following packages (included in `requirements.txt`):
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `httpx` - HTTP client
- `watchfiles` - File watching utilities
- `pytest` - Testing framework

## Running Tests

Install dependencies and run tests:

```bash
# Install all dependencies including pytest
pip install -r requirements.txt

# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_app.py

# Run specific test method
pytest tests/test_app.py::TestActivitiesAPI::test_get_activities_returns_all_activities

# Run tests with coverage (if pytest-cov is installed)
pytest --cov=src --cov-report=html
```

## Test Coverage

The tests cover:

- **GET /activities**: Retrieving all activities
- **POST /activities/{activity_name}/signup**: Signing up for activities
  - Successful signup
  - Duplicate signup prevention
  - Invalid activity handling
- **DELETE /activities/{activity_name}/unregister**: Unregistering from activities
  - Successful unregistration
  - Attempting to unregister non-participants
  - Invalid activity handling
- **GET /**: Root endpoint redirect

## Test Structure

- `test_app.py`: Main test file containing all API endpoint tests
- Uses FastAPI's TestClient for making HTTP requests
- Tests both success and error scenarios
- Validates response status codes and data structure