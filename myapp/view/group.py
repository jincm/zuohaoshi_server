# encoding: utf-8
"""
    zuohaoshi view
    Good man is well
"""

from flask import Blueprint, request, abort, jsonify
from flask.ext.login import login_required, current_user

from myapp.models.user import User
from myapp.models.group import Group
from myapp import app

group_blueprint = Blueprint('group', __name__, url_prefix='/v1/g')

@group_blueprint.route('/create', methods=['POST'])
@login_required
def create_group():
    app.logger.info("post activity:%s,%s" % (request.headers, request.json))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))
    token = request.args.get("token")
    group = request.json.get("group")
    if token is None or group is None:
        app.logger.error("missing parameters:%s,%s" % (token, group))
        abort(400)

    ret = Group.post_group(current_user.user_id, group)
    app.logger.info("post activity:%s" % ret)
    return jsonify(ret)

@group_blueprint.route('/<group_id>', methods=["GET"])
@login_required
def show_group(group_id):
    app.logger.info("get activity:%s,%s,%s" % (group_id, request.headers, request.args))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    group = Group(group_id, current_user.user_id)
    ret = group.get_one_group()
    app.logger.info("get_activity:%s" % ret)

    return jsonify(ret)

@group_blueprint.route('/<group_id>', methods=["DELETE"])
@login_required
def del_group(group_id):
    app.logger.info("get activity:%s,%s,%s" % (group_id, request.headers, request.args))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    group = Group(group_id, current_user.user_id)
    ret = group.del_group()
    app.logger.info("get_activity:%s" % ret)

    return jsonify(ret)

@group_blueprint.route('/search', methods=["GET"])
@login_required
def search_group():
    app.logger.info("get activity:%s,%s" % (request.headers, request.args))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    ret = Group.group_search(current_user.user_id, group)
    #ret = group.get_one_group()
    app.logger.info("get_activity:%s" % ret)

    return jsonify(ret)

@group_blueprint.route('/addto', methods=["POST"])
@login_required
def add_to_one_group(user_id, group_id):
    app.logger.info("add to one group:%s,%s" % (user_id, group_id))

    return jsonify(ret)

@group_blueprint.route('/delfrom', methods=["POST"])
@login_required
def del_from_one_group(user_id, group_id):
    app.logger.info("add to one group:%s,%s" % (user_id, group_id))

    return jsonify(ret)

@group_blueprint.route('/confirmadd', methods=["POST"])
@login_required
def confirm_addto_one_group(user_id, group_id):
    app.logger.info("add to one group:%s,%s" % (user_id, group_id))

    return jsonify(ret)