from flask import Blueprint, request, jsonify
from ..database.db import db
from ..models.models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.json
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user, remember=True)
                return jsonify({"message": "Logged In."})
            else:
                return jsonify({"message": "Password is incorrect."})
        else:
            return jsonify({"message": "User doesn't exist."})
    else:
        return jsonify({"message": "Send a post request with the relevant attributes."})


@auth.route("/register", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        data = request.json
        email = data['email']
        username = data['username']
        password1 = data['password1']
        password2 = data['password2']

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            return jsonify({"message": "Email is already in use."})
        elif username_exists:
            return jsonify({"message": "Username is already in use."})
        elif password1 != password2:
            return jsonify({"message": "Passwords don't match!"})
        else:
            new_user = User(email=email,
                            username=username,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return jsonify({"message": "User created!"})
    else:
        return jsonify({"message": "Send a post request with the relevant attributes."})


@login_required
@auth.route("/logout")
def logout():
    logout_user()
    return jsonify({"message": "User logged out!"})
