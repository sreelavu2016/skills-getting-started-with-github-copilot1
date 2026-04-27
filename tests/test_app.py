import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

# Test data - copy of the activities from app.py for testing
test_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    }
}

class TestActivitiesAPI:
    """Test suite for the Activities API endpoints"""

    def test_get_activities(self):
        """Test GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()

        # Check that we get activities data
        assert isinstance(data, dict)
        assert len(data) > 0

        # Check structure of first activity
        first_activity = next(iter(data.values()))
        assert "description" in first_activity
        assert "schedule" in first_activity
        assert "max_participants" in first_activity
        assert "participants" in first_activity
        assert isinstance(first_activity["participants"], list)

    def test_get_activities_specific_activity(self):
        """Test that specific activities have correct structure"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()

        # Check Chess Club data
        chess_club = data.get("Chess Club")
        assert chess_club is not None
        assert chess_club["description"] == "Learn strategies and compete in chess tournaments"
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_signup_successful(self):
        """Test POST /activities/{activity_name}/signup with valid data"""
        email = "test@mergington.edu"
        activity_name = "Chess Club"

        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify the participant was added
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_duplicate_participant(self):
        """Test POST /activities/{activity_name}/signup prevents duplicates"""
        email = "michael@mergington.edu"  # Already signed up
        activity_name = "Chess Club"

        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"]

    def test_signup_invalid_activity(self):
        """Test POST /activities/{activity_name}/signup with invalid activity"""
        email = "test@mergington.edu"
        activity_name = "Invalid Activity"

        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_unregister_successful(self):
        """Test DELETE /activities/{activity_name}/unregister removes participant"""
        email = "michael@mergington.edu"
        activity_name = "Chess Club"

        # First verify they're signed up
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

        # Unregister them
        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

        # Verify they were removed
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_not_signed_up(self):
        """Test DELETE /activities/{activity_name}/unregister for non-participant"""
        email = "notsignedup@mergington.edu"
        activity_name = "Chess Club"

        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "not signed up" in data["detail"]

    def test_unregister_invalid_activity(self):
        """Test DELETE /activities/{activity_name}/unregister with invalid activity"""
        email = "test@mergington.edu"
        activity_name = "Invalid Activity"

        response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
        assert response.status_code == 404

        data = response.json()
        assert "detail" in data
        assert "Activity not found" in data["detail"]

    def test_root_redirect(self):
        """Test GET / redirects to static index"""
        response = client.get("/")
        assert response.status_code == 200
        # FastAPI's RedirectResponse should serve the static file
        assert "text/html" in response.headers.get("content-type", "")