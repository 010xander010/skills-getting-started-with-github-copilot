from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_200_and_data():
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_adds_participant():
    # Arrange
    activity = "Chess Club"
    email = "test_signup_unique@example.com"
    url = f"/activities/{activity}/signup?email={email}"

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate_returns_400():
    # Arrange
    activity = "Chess Club"
    email = "test_signup_duplicate@example.com"
    url = f"/activities/{activity}/signup?email={email}"
    first = client.post(url)
    assert first.status_code == 200

    # Act
    response = client.post(url)

    # Assert
    assert response.status_code == 400
    assert "already" in response.json()["detail"].lower()


def test_unregister_removes_participant():
    # Arrange
    activity = "Chess Club"
    email = "test_unregister@example.com"
    signup_url = f"/activities/{activity}/signup?email={email}"
    client.post(signup_url)

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_missing_returns_404():
    # Arrange
    activity = "Chess Club"
    email = "test_unregister_missing@example.com"

    # Act
    response = client.post(f"/activities/{activity}/unregister?email={email}")

    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]
