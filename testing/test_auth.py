from models import User


def test_signup(client):
    response = client.post(
        "/signup",
        json={
            "username": "newuser",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["username"] == "newuser"
    assert "id" in data


def test_duplicate_signup(client):
    client.post(
        "/signup",
        json={
            "username": "newuser",
            "password": "password123"
        }
    )

    response = client.post(
        "/signup",
        json={
            "username": "newuser",
            "password": "password123"
        }
    )

    assert response.status_code == 422
    assert response.get_json()["error"] == "Username already exists"


def test_signup_missing_password(client):
    response = client.post(
        "/signup",
        json={
            "username": "newuser"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Username and password are required"


def test_login(client):
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    client.delete("/logout")

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "testuser"
    assert "id" in data


def test_invalid_login(client):
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    client.delete("/logout")

    response = client.post(
        "/login",
        json={
            "username": "testuser",
            "password": "wrongpassword"
        }
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid username or password"


def test_check_session(client):
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    response = client.get("/check_session")

    assert response.status_code == 200

    data = response.get_json()

    assert data["username"] == "testuser"


def test_check_session_unauthorized(client):
    response = client.get("/check_session")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


def test_logout(client):
    client.post(
        "/signup",
        json={
            "username": "testuser",
            "password": "password123"
        }
    )

    response = client.delete("/logout")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Logged out successfully"

    response = client.get("/check_session")

    assert response.status_code == 401


def test_password_is_hashed(client):
    client.post(
        "/signup",
        json={
            "username": "secureuser",
            "password": "password123"
        }
    )

    user = User.query.filter_by(username="secureuser").first()

    assert user is not None
    assert user.password_hash != "password123"
    assert user.authenticate("password123") is True