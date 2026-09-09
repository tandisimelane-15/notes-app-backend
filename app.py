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


if __name__ == "__main__":
    app.run(port=5555, debug=True)
