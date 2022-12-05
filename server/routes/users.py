from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.models import User, Want, Dislike, Dream
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update

users = Blueprint("users", __name__)


@users.route('/users')
def all_users():
    users = User.query.all()
    outputs = map(lambda u: {
        "id": u.id, "email": u.email, "username": u.username, "password": u.password}, users)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200


@users.route('/users/<int:user_id>', methods=['GET', 'DELETE'])
def users_handler(user_id):
    if request.method == 'GET':
        try:
            foundUser = User.query.filter_by(id=user_id).first()
            output = {
                "id": foundUser.id,
                "email": foundUser.email,
                "username": foundUser.username,
                "password": foundUser.password,
                # "friends": foundUser.friends,
                # "wants": foundUser.wants,
                # "dislikes": foundUser.dislikes,
                # "dreams": foundUser.dreams
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a user with that id: {user_id}")
    elif request.method == 'DELETE':
        try:
            foundUser = User.query.filter_by(id=user_id).first()
            db.session.delete(foundUser)
            db.session.commit()
            return "User deleted", 204
        except:
            raise exceptions.BadRequest(
                f"failed to delete a user with that id: {user_id}")


@users.route('/users/<int:user_id>/wants', methods=['GET'])
def display_wants(user_id):
    foundWants = Want.query.filter_by(author=user_id).all()
    outputs = map(lambda w: {
        "id": w.id, "category": w.category, "item": w.item, "author": w.author}, foundWants)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200


@users.route('/users/<int:user_id>/dislikes', methods=['GET'])
def display_dislikes(user_id):
    pass


@users.route('/users/<int:user_id>/dreams', methods=['GET'])
def display_dreams(user_id):
    pass
