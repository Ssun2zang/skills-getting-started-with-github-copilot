"""
Test suite for High School Management System API
"""
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_root_redirect():
    """Test that root path redirects to index.html"""
    # Ensure TestClient does not follow the redirect so we can assert the
    # redirect status and Location header coming from the app.
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307  # Temporary redirect
    assert response.headers["location"] == "/static/index.html"

def test_get_activities():
    """Test retrieving all activities"""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    
    # Check if we have all the expected activities
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", 
        "Basketball Team", "Swimming Club", "Art Studio",
        "Drama Club", "Debate Team", "Science Club"
    ]
    assert all(activity in activities for activity in expected_activities)

    # Check activity structure
    for activity_name, details in activities.items():
        assert "description" in details
        assert "schedule" in details
        assert "max_participants" in details
        assert "participants" in details
        assert isinstance(details["participants"], list)

def test_signup_for_activity():
    """Test signing up for an activity"""
    activity_name = "Chess Club"
    email = "test@mergington.edu"
    
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}

def test_signup_nonexistent_activity():
    """Test signing up for a non-existent activity"""
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}