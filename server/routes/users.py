from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.models import User, Want, Dislike, Dream
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update, select

users = Blueprint("users", __name__)


@users.route('/users')
def all_users():
    users = User.query.all()
    outputs = map(lambda u: {
        "id": u.id, "email": u.email, "username": u.username, "password": u.password}, users)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200


@users.route('/users/<user_name>', methods=['GET', 'DELETE'])
def username_handler(user_name):
    if request.method == 'GET':
        try:
            foundUser = User.query.filter_by(username=user_name).first()
            output = {
                "id": foundUser.id,
                "email": foundUser.email,
                "username": foundUser.username,
                "password": foundUser.password,
                "friends": foundUser.friends,
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a user with that username: {user_name}")
    elif request.method == 'DELETE':
        try:
            users = User.query.all()
            for user in users:
                friends = user.friends["friends_list"]
                if user_name in friends:
                    user_id = user.id
                    friends.remove(user_name)
                    stmt = update(User).where(User.id == user_id).values(
                        friends={"friends_list": friends})
                    db.session.execute(stmt)
                    db.session.commit()

            foundUser = User.query.filter_by(username=user_name).first()
            db.session.delete(foundUser)
            db.session.commit()
            return "User deleted", 204
        except:
            raise exceptions.BadRequest(
                f"failed to delete a user with that name: {user_name}")


@ users.route('/users/<user_name>/friends', methods=['GET', 'POST'])
def friends(user_name):
    foundUser = User.query.filter_by(username=user_name).first()
    friends = foundUser.friends["friends_list"]
    if request.method == 'GET':
        return jsonify(friends), 200
    elif request.method == 'POST':
        data = request.json
        friend = data['friend']
        foundUser = User.query.filter_by(username=friend).first()
        if foundUser:
            if foundUser.username == user_name:
                raise exceptions.BadRequest(
                    f"You can't add yourself as a friend!")
            if friend in friends:
                raise exceptions.BadRequest(
                    f"{foundUser.username} has already been added to your friends!")
            friends.append(friend)
            stmt = update(User).where(User.username == user_name).values(
                friends={"friends_list": friends})
            db.session.execute(stmt)
            db.session.commit()
            return "Added friend", 201
        else:
            raise exceptions.BadRequest(
                f"We do not have a user with that name: {friend}")


@ users.route('/users/<user_name>/wants', methods=['GET'])
def display_wants(user_name):
    foundWants = Want.query.filter_by(author=user_name).all()
    outputs = map(lambda w: {
        "id": w.id, "category": w.category, "item": w.item, "author": w.author, "purchased": w.purchased}, foundWants)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200


@ users.route('/users/<user_name>/dislikes', methods=['GET'])
def display_dislikes(user_name):
    foundDislikes = Dislike.query.filter_by(author=user_name).all()
    outputs = map(lambda d: {
        "id": d.id, "category": d.category, "item": d.item, "author": d.author}, foundDislikes)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200


@ users.route('/users/<user_name>/dreams', methods=['GET'])
def display_dreams(user_name):
    foundDreams = Dream.query.filter_by(author=user_name).all()
    outputs = map(lambda d: {
        "id": d.id, "category": d.category, "item": d.item, "author": d.author, "purchased": d.purchased}, foundDreams)
    usableOutputs = list(outputs)
    return jsonify(usableOutputs), 200


@ users.route('/users/<user_name>/wishlist')
def display_wishlist(user_name):
    foundWants = Want.query.filter_by(author=user_name).all()
    wants = map(lambda w: {
        "id": w.id, "category": w.category, "item": w.item, "author": w.author, "purchased": w.purchased}, foundWants)
    foundDislikes = Dislike.query.filter_by(author=user_name).all()
    dislikes = map(lambda d: {
        "id": d.id, "category": d.category, "item": d.item, "author": d.author}, foundDislikes)
    foundDreams = Dream.query.filter_by(author=user_name).all()
    dreams = map(lambda d: {
        "id": d.id, "category": d.category, "item": d.item, "author": d.author, "purchased": d.purchased}, foundDreams)
    usableOutputs = {'wants': list(wants), 'dislikes': list(
        dislikes), 'dreams': list(dreams)}
    return usableOutputs, 200
