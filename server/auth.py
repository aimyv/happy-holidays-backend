from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    pass


@auth.route("/register", methods=['GET', 'POST'])
def sign_up():
    pass


@login_required
@auth.route("/logout")
def logout():
    pass
