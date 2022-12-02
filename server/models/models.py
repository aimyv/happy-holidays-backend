from ..database.db import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    friends = db.Column(db.JSON)
    wants = db.Column(db.JSON)
    dislikes = db.Column(db.JSON)
    dreams = db.Column(db.JSON)


class Want(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20))
    item = db.Column(db.String(150))


class Dislike(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20))
    item = db.Column(db.String(150))


class Dream(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(20))
    item = db.Column(db.String(150))
