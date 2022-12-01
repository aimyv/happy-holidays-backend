from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User
from . import db
from werkzeug import exceptions

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return jsonify({"message": "Hello, from Flask!"})
