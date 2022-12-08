from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.models import User, Want
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update
from sqlalchemy import func

wants = Blueprint("wants", __name__)


@wants.route('/wants', methods=['GET', 'POST'])
def all_wants():
    if request.method == 'GET':
        wants = Want.query.all()
        outputs = map(lambda w: {
            "id": w.id, "category": w.category, "item": w.item, "purchased": w.purchased, "author": w.author}, wants)
        usableOutputs = list(outputs)
        return jsonify(usableOutputs), 200
    elif request.method == 'POST':
        data = request.json
        new_want = Want(category=data["category"],
                        item=data["item"], purchased=False, author=data["author"])
        db.session.add(new_want)
        db.session.commit()
        output = {"id": new_want.id, "category": new_want.category,
                  "item": new_want.item, "author": new_want.author, "purchased": new_want.purchased}
        return jsonify(output), 201


@wants.route('/wants/<int:want_id>', methods=['GET', 'PUT', 'DELETE'])
def wants_handler(want_id):
    if request.method == 'GET':
        try:
            foundWant = Want.query.filter_by(id=want_id).first()
            output = {
                "id": foundWant.id,
                "category": foundWant.category,
                "item": foundWant.item,
                "purchased": foundWant.purchased,
                "author": foundWant.author
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a want with that id: {want_id}")
    elif request.method == 'PUT':
        try:
            foundWant = Want.query.filter_by(id=want_id).first()
            flip = not foundWant.purchased
            stmt = update(Want).where(
                Want.id == want_id).values(purchased=flip)
            db.session.execute(stmt)
            db.session.commit()
            output = {
                "id": foundWant.id,
                "category": foundWant.category,
                "item": foundWant.item,
                "purchased": flip,
                "author": foundWant.author
            }
            return output, 202
        except:
            raise exceptions.BadRequest(
                f"We do not have a want with that id: {want_id}")
    elif request.method == 'DELETE':
        try:
            foundWant = Want.query.filter_by(id=want_id).first()
            db.session.delete(foundWant)
            db.session.commit()
            return "deleted", 204
        except:
            raise exceptions.BadRequest(
                f"failed to delete a want with that id: {want_id}")
