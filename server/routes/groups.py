from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from ..models.models import User, Group
from ..database.db import db
from werkzeug import exceptions
from sqlalchemy import update, select

groups = Blueprint("groups", __name__)


@groups.route('/groups', methods=['GET', 'POST'])
def all_groups():
    if request.method == 'GET':
        groups = Group.query.all()
        outputs = map(lambda g: {
            "id": g.id,
            "name": g.name,
            "members": g.members
        }, groups)
        usableOutputs = list(outputs)
        return jsonify(usableOutputs), 200
    elif request.method == 'POST':
        data = request.json
        new_group = Group(
            name=data["name"],
            members={"members_list": data["members"]})
        db.session.add(new_group)
        db.session.commit()
        output = {
            "id": new_group.id,
            "name": new_group.name,
            "members": new_group.members
        }
        return jsonify(output), 201


@groups.route('/groups/<int:group_id>', methods=['GET', 'DELETE'])
def groupname_handler(group_id):
    if request.method == 'GET':
        try:
            foundGroup = Group.query.filter_by(id=group_id).first()
            output = {
                "id": foundGroup.id,
                "name": foundGroup.name,
                "members": foundGroup.members
            }
            return output
        except:
            raise exceptions.BadRequest(
                f"We do not have a group with that id: {group_id}")
    elif request.method == 'DELETE':
        try:
            foundGroup = Group.query.filter_by(id=group_id).first()
            db.session.delete(foundGroup)
            db.session.commit()
            return "Group deleted", 204
        except:
            raise exceptions.BadRequest(
                f"failed to delete a group with that id: {group_id}")
