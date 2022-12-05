from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.models import User, Want, Dislike, Dream
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update

dislikes = Blueprint("dislikes", __name__)


@dislikes.route('/dislikes', methods=['GET', 'POST'])
def all_dislikes():
    if request.method == 'GET':
        dislikes = Dislike.query.all()
        outputs = map(lambda d: {
            "id": d.id, "category": d.category, "item": d.item, "author": d.author}, dislikes)
        usableOutputs = list(outputs)
        return jsonify(usableOutputs), 200
    elif request.method == 'POST':
        data = request.json
        count = Dislike.query.count()
        id = count + 1
        new_dislike = Dislike(
            id=id, category=data["category"], item=data["item"], author=data["author"])
        db.session.add(new_dislike)
        db.session.commit()
        output = {"id": new_dislike.id, "category": new_dislike.category,
                  "item": new_dislike.item, "author": new_dislike.author}
        return jsonify(output), 201


@dislikes.route('/dislikes/<int:dislike_id>', methods=['GET', 'DELETE'])
def dislikes_handler(dislike_id):
    if request.method == 'GET':
        try:
            foundDislike = Dislike.query.filter_by(id=dislike_id).first()
            output = {
                "id": foundDislike.id,
                "category": foundDislike.category,
                "item": foundDislike.item,
                "author": foundDislike.author
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a dislike with that id: {dislike_id}")
    elif request.method == 'DELETE':
        try:
            foundDislike = Dislike.query.filter_by(id=dislike_id).first()
            db.session.delete(foundDislike)
            db.session.commit()
            return "deleted", 204
        except:
            raise exceptions.BadRequest(
                f"failed to delete a dislike with that id: {dislike_id}")
