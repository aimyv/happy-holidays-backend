from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug import exceptions

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return jsonify({"message": "Hello, from Flask!"}), 200


@views.route('/users')
def urls_handler():
    users = User.query.all()
    outputs = map(lambda u: {
        "id": u.id, "email": u.email, "username": u.username, "password": u.password}, users)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200
