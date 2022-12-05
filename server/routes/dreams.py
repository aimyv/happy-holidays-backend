from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.models import User, Dream
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update

dreams = Blueprint("dreams", __name__)


@dreams.route('/dreams', methods=['GET', 'POST'])
def all_dreams():
    if request.method == 'GET':
        dreams = Dream.query.all()
        outputs = map(lambda d: {
            "id": d.id, "category": d.category, "item": d.item, "author": d.author}, dreams)
        usableOutputs = list(outputs)
        return jsonify(usableOutputs), 200
    elif request.method == 'POST':
        data = request.json
        new_dream = Dream(
            category=data["category"], item=data["item"], author=data["author"])
        db.session.add(new_dream)
        db.session.commit()
        output = {"id": new_dream.id, "category": new_dream.category,
                  "item": new_dream.item, "author": new_dream.author}
        return jsonify(output), 201


@dreams.route('/dreams/<int:dream_id>', methods=['GET', 'DELETE'])
def dreams_handler(dream_id):
    if request.method == 'GET':
        try:
            foundDream = Dream.query.filter_by(id=dream_id).first()
            output = {
                "id": foundDream.id,
                "category": foundDream.category,
                "item": foundDream.item,
                "author": foundDream.author
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a dream with that id: {dream_id}")
    elif request.method == 'DELETE':
        try:
            foundDream = Dream.query.filter_by(id=dream_id).first()
            db.session.delete(foundDream)
            db.session.commit()
            return "deleted", 204
        except:
            raise exceptions.BadRequest(
                f"failed to delete a dream with that id: {dream_id}")
