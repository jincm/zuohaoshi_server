# encoding: utf-8

"""
    zuohaoshi view
    Good man is well
"""
import datetime

from flask import Blueprint, request, abort, url_for, jsonify
from flask.ext.login import login_required

from myapp.models.user import User
from myapp import app

users_blueprint = Blueprint('users', __name__, url_prefix='/v1/users')

#loster_blueprint = Blueprint('loster', __name__)
#message_blueprint = Blueprint('message', __name__)


########################
#### register ##########
########################
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    app.logger.info("get user headers:[%s] args:[%s]" % (request.headers, request.args))
    app.logger.info("json:[%s]\n" % request.json)

    #app.logger.info(url_for('.show_user', user='test'))

    if request.method == 'GET':
        accout = request.args.get("accout")
        if accout is None:
            app.logger.error("missing something")
            abort(400) #missing phone_num
        ret = User.register_user(accout, None, None)
        return jsonify(ret)
    elif request.method == 'POST':
        accout = request.json.get('accout')
        identify_code = request.json.get('identify_code')
        passwd = request.json.get('passwd')
        if accout is None or identify_code is None or passwd is None:
            app.logger.error("missing something")
            abort(400)
        ret = User.register_user(accout, identify_code, passwd)
        return jsonify(ret)


########################
#### login ##########
########################
@users_blueprint.route('/login', methods=['POST'])
def user_login():
    app.logger.info("get user headers:[%s] json:[%s]" % (request.headers, request.json))
    accout = request.json.get('accout')
    passwd = request.json.get('passwd')
    if accout is None or passwd is None:
        app.logger.error("missing something")
        abort(400)
    ret = User.login(accout, passwd)
    return jsonify(ret)


########################
#########logout#########
########################
@users_blueprint.route('/logout/<user_id>', methods=['GET'])
@login_required
def user_logout(user_id):
    user = User(user_id)
    ret = user.logout()
    return jsonify(ret)


@users_blueprint.route('/<user_id>', methods=["GET"])
@login_required
def show_user(user_id):
    user = User(user_id)
    ret = user.show_user()
    app.logger.info("show_user %s" % user_id)
    return jsonify(ret)


#admin add user direct
@users_blueprint.route('/users', methods=['POST'])
@login_required
def add_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    user = User(username, password)
    user.hash_password(password)
    #user.save()

    return jsonify({'username': user.username}), 201, {'Location': url_for('get_user', id=user.id, _external=True)}


#save file to oss
#post

#save redis

#relationship
#face_match

