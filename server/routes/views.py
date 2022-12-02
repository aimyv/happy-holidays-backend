from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.models import User, Want, Dislike, Dream
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return jsonify({"message": "Hello, from Flask!"}), 200


@views.route('/users')
def all_users():
    users = User.query.all()
    outputs = map(lambda u: {
        "id": u.id, "email": u.email, "username": u.username, "password": u.password}, users)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200


@views.route('/wants', methods=['GET', 'POST'])
def all_wants():
    if request.method == 'GET':
        wants = Want.query.all()
        outputs = map(lambda w: {
            "id": w.id, "category": w.category, "item": w.item}, wants)
        usableOutputs = list(outputs)
        return jsonify(usableOutputs), 200
    elif request.method == 'POST':
        data = request.json
        count = Want.query.count()
        id = count + 1

        # update user wants
        foundUser = User.query.filter_by(id=data["user"]).first()
        new_array = foundUser.wants["wants_list"]
        new_array.append(id)
        stmt = (update(User).where(
            User.id == data["user"]).values(wants={"wants_list": new_array}))
        db.session.execute(stmt)
        db.session.commit()

        # post want
        new_want = Want(
            id=id, category=data["category"], item=data["item"])
        db.session.add(new_want)
        db.session.commit()
        output = {"id": new_want.id, "category": new_want.category,
                  "item": new_want.item}
        return jsonify(output), 201


@views.route('/users/<int:user_id>', methods=['GET', 'DELETE'])
def users_handler(user_id):
    if request.method == 'GET':
        try:
            foundUser = User.query.filter_by(id=user_id).first()
            output = {
                "id": foundUser.id,
                "email": foundUser.email,
                "username": foundUser.username,
                "password": foundUser.password,
                "friends": foundUser.friends,
                "wants": foundUser.wants,
                "dislikes": foundUser.dislikes,
                "dreams": foundUser.dreams
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


@views.route('/wants/<int:want_id>', methods=['GET', 'PUT', 'DELETE'])
def wants_handler(want_id):
    if request.method == 'GET':
        pass
    elif request.method == 'PUT':
        pass
    elif request.method == 'DELETE':
        pass
