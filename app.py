from flask import Flask
from flask_migrate import Migrate

from models import db, bcrypt, User, Note

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
bcrypt.init_app(app)

migrate = Migrate(app, db)