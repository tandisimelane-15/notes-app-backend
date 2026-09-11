from models import User, Note, db


def signup_user(client, username="testuser", password="password123"):
    return client.post(
        "/signup",
        json={
            "username": username,
            "password": password
        }
    )


def login_user(client, username="testuser", password="password123"):
    return client.post(
        "/login",
        json={
            "username": username,
            "password": password
        }
    )


def test_get_notes_requires_login(client):
    response = client.get("/notes")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


def test_get_single_note_requires_login(client):
    response = client.get("/notes/1")

    assert response.status_code == 401
    assert response.get_json()["error"] == "Unauthorized"


def test_create_note(client):
    signup_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "Test Note",
            "content": "This is a test note."
        }
    )

    assert response.status_code == 201

    data = response.get_json()

    assert data["title"] == "Test Note"
    assert data["content"] == "This is a test note."
    assert "id" in data
    assert "user_id" in data


def test_create_note_missing_content(client):
    signup_user(client)

    response = client.post(
        "/notes",
        json={
            "title": "Incomplete Note"
        }
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Title and content are required"


def test_get_own_notes(client):
    signup_user(client)

    client.post(
        "/notes",
        json={
            "title": "Note One",
            "content": "First note"
        }
    )

    client.post(
        "/notes",
        json={
            "title": "Note Two",
            "content": "Second note"
        }
    )

    response = client.get("/notes")

    assert response.status_code == 200

    data = response.get_json()

    # Works with the paginated /notes response
    assert "notes" in data
    assert len(data["notes"]) == 2

    titles = [note["title"] for note in data["notes"]]

    assert "Note One" in titles
    assert "Note Two" in titles


def test_get_note_by_id(client):
    signup_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Single Note",
            "content": "Read this note"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.get(f"/notes/{note_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert data["id"] == note_id
    assert data["title"] == "Single Note"


def test_update_note(client):
    signup_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Old Title",
            "content": "Old Content"
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "Updated Title",
            "content": "Updated Content"
        }
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated Content"


def test_delete_note(client):
    signup_user(client)

    create_response = client.post(
        "/notes",
        json={
            "title": "Delete Me",
            "content": "This note will be deleted."
        }
    )

    note_id = create_response.get_json()["id"]

    response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 200
    assert response.get_json()["message"] == "Note deleted successfully"

    get_response = client.get(f"/notes/{note_id}")

    assert get_response.status_code == 404


def test_user_cannot_access_another_users_note(client):
    signup_user(client, "user1")

    create_response = client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "User 1 owns this."
        }
    )

    note_id = create_response.get_json()["id"]

    client.delete("/logout")

    signup_user(client, "user2")

    response = client.get(f"/notes/{note_id}")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Note not found"


def test_user_cannot_update_another_users_note(client):
    signup_user(client, "user1")

    create_response = client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "Original content"
        }
    )

    note_id = create_response.get_json()["id"]

    client.delete("/logout")

    signup_user(client, "user2")

    response = client.patch(
        f"/notes/{note_id}",
        json={
            "title": "Hacked Title"
        }
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Note not found"


def test_user_cannot_delete_another_users_note(client):
    signup_user(client, "user1")

    create_response = client.post(
        "/notes",
        json={
            "title": "Private Note",
            "content": "Do not delete"
        }
    )

    note_id = create_response.get_json()["id"]

    client.delete("/logout")

    signup_user(client, "user2")

    response = client.delete(f"/notes/{note_id}")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Note not found"

    note = db.session.get(Note, note_id)

    assert note is not None


def test_notes_pagination(client):
    signup_user(client)

    for i in range(5):
        client.post(
            "/notes",
            json={
                "title": f"Note {i + 1}",
                "content": f"Content {i + 1}"
            }
        )

    response = client.get("/notes?page=1&per_page=2")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["notes"]) == 2
    assert data["page"] == 1
    assert data["per_page"] == 2
    assert data["total"] == 5
    assert data["pages"] == 3
    assert data["has_next"] is True
    assert data["has_prev"] is False


def test_second_page_of_notes(client):
    signup_user(client)

    for i in range(5):
        client.post(
            "/notes",
            json={
                "title": f"Note {i + 1}",
                "content": f"Content {i + 1}"
            }
        )

    response = client.get("/notes?page=2&per_page=2")

    assert response.status_code == 200

    data = response.get_json()

    assert len(data["notes"]) == 2
    assert data["page"] == 2
    assert data["has_prev"] is True