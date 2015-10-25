# encoding: utf-8

"""
    zuohaoshi admin
    Be a good man
"""
from flask import Blueprint
from myapp import app

from myapp.models.user import User
from myapp.models.activity import Activity
from myapp.models.group import Group

admin_blueprint = Blueprint('admin', __name__, url_prefix='/1/admin')

@admin_blueprint.route("/hello", methods=["GET", "POST"])
def hello():
    user = User()
    ac = Activity()
    group = Group()
    app.logger.info("Test for admin")
    return "hello admin"


########################
# #user edit by admin###
########################
# admin add user direct
@admin_blueprint.route('/admin/add_user', methods=['POST'])
def add_user_by_admin():
    account = request.json.get('account')
    password = request.json.get('password')
    token = request.args.get('token')
    if account is None or password is None or token is None:
        abort(400)
    admin = User.get_user_fromtoken(token)
    if not admin:
        abort(401)

    ret = User.add_user(account, password)
    # user.save()

    return jsonify({'username': account}), 201, {'Location': url_for('.get_user')}

@admin_blueprint.route('/admin/del_user/<user_id>', methods=['POST'])
def del_user_by_admin(user_id):
    # account = request.json.get('account')
    # password = request.json.get('password')
    token = request.args.get('token')
    if token is None:
        abort(400)
    admin = User.get_user_from_token(token)
    if not admin:
        abort(401)

    ret = User.del_user(user_id)
    # user.save()

    return jsonify({'username': user_id}), 201, {'Location': url_for('.get_user')}
