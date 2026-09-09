from flask import Flask, jsonify, request, session
from flask_migrate import Migrate

from models import db, bcrypt, User, Note

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "notes-app-secret-key"

db.init_app(app)
bcrypt.init_app(app)

migrate = Migrate(app, db)


# -------------------------
# Authentication Routes
# -------------------------

@app.post("/signup")
def signup():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"error": "Username already exists"}), 422

    user = User(username=username)
    user.password = password

    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 201


@app.post("/login")
def login():
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.authenticate(password):
        return jsonify({"error": "Invalid username or password"}), 401

    session["user_id"] = user.id

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 200


@app.get("/check_session")
def check_session():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return jsonify({"error": "Unauthorized"}), 401

    return jsonify({
        "id": user.id,
        "username": user.username
    }), 200


@app.delete("/logout")
def logout():
    session.clear()

    return jsonify({
        "message": "Logged out successfully"
    }), 200


# -------------------------
# Notes CRUD Routes
# -------------------------

@app.get("/notes")
def get_notes():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    notes = Note.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            "id": note.id,
            "title": note.title,
            "content": note.content,
            "user_id": note.user_id
        }
        for note in notes
    ]), 200


@app.get("/notes/<int:id>")
def get_note_by_id(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    note = Note.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "user_id": note.user_id
    }), 200


@app.post("/notes")
def create_note():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()

    title = data.get("title")
    content = data.get("content")

    if not title or not content:
        return jsonify({"error": "Title and content are required"}), 400

    note = Note(
        title=title,
        content=content,
        user_id=user_id
    )

    db.session.add(note)
    db.session.commit()

    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "user_id": note.user_id
    }), 201


@app.patch("/notes/<int:id>")
def update_note(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    note = Note.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    data = request.get_json() or {}

    title = data.get("title")
    content = data.get("content")

    if title:
        note.title = title
    if content:
        note.content = content

    db.session.commit()

    return jsonify({
        "id": note.id,
        "title": note.title,
        "content": note.content,
        "user_id": note.user_id
    }), 200


@app.delete("/notes/<int:id>")
def delete_note(id):
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    note = Note.query.filter_by(id=id, user_id=user_id).first()

    if not note:
        return jsonify({"error": "Note not found"}), 404

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted successfully"}), 200


if __name__ == "__main__":
    app.run(port=5555, debug=True)
