# encoding: utf-8

"""
    zuohaoshi view
    Good man is well
"""
#system package
import os
import datetime

#flask and other thirdparty package
from flask import Blueprint, request, abort, url_for, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename

#project package
from myapp.models.user import User
from myapp.ext.file_oss import oss_upload_file as upload_file_to_store
from myapp import app

users_blueprint = Blueprint('users', __name__, url_prefix='/1/u')

#loster_blueprint = Blueprint('loster', __name__)
#message_blueprint = Blueprint('message', __name__)


########################
#### register ##########
########################
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    app.logger.info("get user headers:[%s] args:[%s]" % (request.headers, request.args))
    app.logger.info("json:[%s]\n" % request.json) #json:post,args:get,header have format

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


########################
#########user show######
########################
@users_blueprint.route('/<user_id>', methods=["GET"])
@login_required
def show_user(user_id):
    user = User(user_id)
    ret = user.show_user()
    app.logger.info("show_user %s" % user_id)
    return jsonify(ret)


#admin add user direct
@users_blueprint.route('/admin/add_user', methods=['POST'])
def add_user_byadmin():
    accout = request.json.get('accout')
    password = request.json.get('password')
    token = request.args.get('token')
    if accout is None or password is None or token is None:
        abort(400)
    admin = User.get_user_fromtoken(token)
    if not admin:
        abort(401)

    ret = User.add_user(accout, password)
    #user.save()

    return jsonify({'username': accout}), 201, {'Location': url_for('.get_user')}


ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
#save file to oss
@users_blueprint.route('/upload', methods=['POST'])
@login_required
def user_upload_file():
    app.logger.info("start upload file")
    f = request.files['file']
    fname = secure_filename(f.filename)
    localfile = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    app.logger.info("start upload file to store:%s,%s" % (fname, localfile))

    f.save(localfile)
    res = upload_file_to_store('zuohaoshi/2015/beijing', fname, localfile)
    app.logger.info("end upload file to store:%s,%s" % (res.status, res.read()))
    return jsonify({'file': fname})


#user add friends/follow sb/followers/blacklist/search
@users_blueprint.route('/fs/<user_id>', methods=["GET"])
@login_required
def follow_sb(user_id):
    app.logger.info("get activity:%s,%s,%s" % (request.headers, request.args))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    user = User(user_id)
    ret = user.show_user()
    app.logger.info("show_user %s" % user_id)
    return jsonify(ret)

@users_blueprint.route('/ufs/<user_id>', methods=["GET"])
@login_required
def unfollow_sb(user_id):
    app.logger.info("get activity:%s,%s,%s" % (request.headers, request.args))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    user = User(user_id)
    ret = user.show_user()
    app.logger.info("show_user %s" % user_id)
    return jsonify(ret)

@users_blueprint.route('/black/<user_id>', methods=["GET"])
@login_required
def black_sb(user_id):
    app.logger.info("get activity:%s,%s,%s" % (request.headers, request.args))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    user = User(user_id)
    ret = user.show_user()
    app.logger.info("show_user %s" % user_id)
    return jsonify(ret)

@users_blueprint.route('/search/<user_id>', methods=["GET"])
@login_required
def search_sb(user_id):
    app.logger.info("get activity:%s,%s,%s" % (request.headers, request.args))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    user = User(user_id)
    ret = user.show_user()
    app.logger.info("show_user %s" % user_id)
    return jsonify(ret)

