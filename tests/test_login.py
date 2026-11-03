
import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# Test 1: Verify login page loads
def test_login_page_loads(client):
    response = client.get("/")

    assert response.status_code == 200


# Test 2: Verify login with valid credentials
def test_valid_login(client):
    response = client.post(
        "/",
        data={
            "username": "admin",
            "password": "Admin@123"
        }
    )

    assert response.status_code == 302
    assert "/dashboard" in response.location


# Test 3: Verify login with invalid credentials
def test_invalid_login(client):
    response = client.post(
        "/",
        data={
            "username": "wrong",
            "password": "wrong123"
        }
    )

    assert response.status_code == 200
    assert b"Invalid username or password!" in response.data


# Test 4: Verify dashboard without login
def test_dashboard_without_login(client):
    response = client.get("/dashboard")

    assert response.status_code == 302
    assert response.location.endswith("/")


# Test 5: Verify logout functionality
def test_logout(client):
    with client.session_transaction() as session:
        session["username"] = "admin"

    response = client.get("/logout")

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert "username" not in session
