# encoding: utf-8

"""
    zuohaoshi view
    Good man is well
"""
# system package
import os
import datetime

# flask and other third party package
from flask import Blueprint, request, abort, url_for, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename

# project package
from myapp.models.user import User
from myapp.ext.file_oss import oss_upload_file as upload_file_to_store
from myapp import app

users_blueprint = Blueprint('users', __name__, url_prefix='/1/u')
# loster_blueprint = Blueprint('loster', __name__)
# message_blueprint = Blueprint('message', __name__)

# account-->username
# user_id-->objectid

########################
# ## register ##########
########################
@users_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    # json:post,args:get,header have format

    # get identify code
    if request.method == 'GET':
        account = request.args.get("account")
        if account is None:
            app.logger.error("missing something")
            abort(400)  # missing phone_num
        ret = User.register_user(account, None, None)
        return jsonify(ret)
    elif request.method == 'POST':
        account = request.json.get('account')
        identify_code = request.json.get('identify_code')
        password = request.json.get('passwd')
        if account is None or identify_code is None or password is None:
            app.logger.error("missing something")
            abort(400)
        ret = User.register_user(account, identify_code, password)
        return jsonify(ret)


########################
# ##### login ##########
########################
@users_blueprint.route('/login', methods=['POST'])
def user_login():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    account = request.json.get('account')
    password = request.json.get('passwd')
    if account is None or password is None:
        app.logger.error("missing something")
        abort(400)
    ret = User.login(account, password)

    ret_json = jsonify(ret)
    app.logger.info("user_login %s:[%s]" % (account, ret_json))
    return ret_json


########################
# #######logout#########
########################
@users_blueprint.route('/logout/<user_id>', methods=['GET'])
@login_required
def user_logout(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)
    app.logger.info("logout: %s" % user_id)

    user = User(user_id)
    ret = user.logout()
    ret_json = jsonify(ret)
    app.logger.info("logout %s:[%s]" % (user_id, ret_json))
    return ret_json


########################
# #######delete#########
########################
@users_blueprint.route('/delete', methods=['POST'])
@login_required
def del_user():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    user_id = request.json.get("uid")
    if user_id is None:
        app.logger.error("missing something:uid key is lost")
        abort(400)

    # may delete by self or admin
    user = User(current_user.user_id)
    ret = user.del_user(user_id)

    ret_json = jsonify(ret)
    app.logger.info("logout %s:[%s]" % (user_id, ret_json))
    return ret_json

# save file to oss
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
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


########################
# #######user edit######
########################
@users_blueprint.route('/mf_user', methods=["POST"])
@login_required
def modify_user():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    user = User(current_user.user_id)
    info = request.json

    files = request.files['file']
    if files:
        # upload new head portrait to store and update info's url
        app.logger.info("update user's portrait")
        pic_url = '%s/' % current_user.user_id
        info = info + {'head_pic': pic_url}
        # user.modify_user(info)

    if info is None:
        app.logger.error("missing something:info key is lost")
        abort(400)

    ret = user.modify_user(info)

    ret_json = jsonify(ret)
    app.logger.info("modify_user %s:[%s]" % (current_user.user_id, ret_json))
    return ret_json


@users_blueprint.route('/<user_id>', methods=["GET"])
@login_required
def show_user(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    user = User(user_id)
    ret = user.show_user()

    ret_json = jsonify(ret)
    app.logger.info("show_user %s:[%s]" % (user_id, ret_json))
    return ret_json


@users_blueprint.route('/nb', methods=["POST"])
@login_required
def nearby_users():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if request.json is None or 'loc' not in request.json:
        app.logger.error("missing something:loc key is lost")
        abort(400)

    user = User(current_user.user_id)
    # search nearby users by some conditions, example age/sex/pos
    ret = user.person_nearby(request.json)

    ret_json = jsonify(ret)
    app.logger.info("nearby_users %s:[%s]" % (current_user.user_id, ret_json))
    return ret_json


# user add friends/follow sb/followers/blacklist
@users_blueprint.route('/add_friend', methods=["POST"])
@login_required
def add_friend_ask():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if request.json is None or 'friend' not in request.json:
        app.logger.error("missing something:friend key is lost")
        abort(400)

    friend = request.json.get('friend')

    user = User(current_user.user_id)
    ret = user.add_friend_ask(friend, request.json.get('msg'))

    ret_json = jsonify(ret)
    app.logger.info("add_friend_ask %s:[%s]" % (friend, ret_json))
    return ret_json

@users_blueprint.route('/confirm_friend', methods=["POST"])
@login_required
def add_friend_confirm():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)
    if request.json is None or 'friend' not in request.json:
        app.logger.error("missing something:friend key is lost")
        abort(400)

    friend = request.json.get('friend')

    user = User(current_user.user_id)
    ret = user.add_friend_confirm(friend)

    ret_json = jsonify(ret)
    app.logger.info("add_friend_confirm %s:[%s]" % (friend, ret_json))
    return ret_json


@users_blueprint.route('/fs', methods=["POST"])
@login_required
def follow_sb():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if request.json is None or 'follow' not in request.json:
        app.logger.error("missing something:follow key is lost")
        abort(400)

    follow = request.json.get('follow')

    user = User(current_user.user_id)
    ret = user.follow_sb(follow)

    ret_json = jsonify(ret)
    app.logger.info("add_friend_ask %s:[%s]" % (follow, ret_json))
    return ret_json

@users_blueprint.route('/ufs/<user_id>', methods=["GET"])
@login_required
def un_follow_sb(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if request.json is None or 'follow' not in request.json:
        app.logger.error("missing something:follow key is lost")
        abort(400)

    follow = request.json.get('follow')

    user = User(current_user.user_id)
    ret = user.un_follow_sb(follow)

    ret_json = jsonify(ret)
    app.logger.info("un_follow_sb %s:[%s]" % (user_id, ret_json))
    return ret_json


@users_blueprint.route('/black', methods=["POST"])
@login_required
def black_sb():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if request.json is None or 'black' not in request.json:
        app.logger.error("missing something:follow key is lost")
        abort(400)

    black = request.json.get('black')

    user = User(current_user.user_id)
    ret = user.block(current_user.user_id, black)

    ret_json = jsonify(ret)
    app.logger.info("black_sb %s:[%s]" % (black, ret_json))
    return ret_json


@users_blueprint.route('/unblack', methods=["POST"])
@login_required
def un_black_sb():
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if request.json is None or 'black' not in request.json:
        app.logger.error("missing something:follow key is lost")
        abort(400)

    black = request.json.get('black')

    user = User(current_user.user_id)
    ret = user.unblock(current_user.user_id, black)

    ret_json = jsonify(ret)
    app.logger.info("black_sb %s:[%s]" % (black, ret_json))
    return ret_json


@users_blueprint.route('/frs/<user_id>', methods=["GET"])
@login_required
def get_friends(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if current_user.user_id != user_id:
        if current_user.user_id != 'admin':
            app.logger.error("access deny for user not the true user")
            abort(400)

    user = User(user_id)
    ret = user.get_friends(user_id)

    ret_json = jsonify(ret)
    app.logger.info("black_sb %s:[%s]" % (user_id, ret_json))
    return ret_json



@users_blueprint.route('/follows/<user_id>/<limit>/<ordey>', methods=["GET"])
@login_required
def get_follows(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if current_user.user_id != user_id:
        if current_user.user_id != 'admin':
            app.logger.error("access deny for user not the true user")
            abort(400)

    user = User(user_id)
    ret = user.get_follows(user_id)

    ret_json = jsonify(ret)
    app.logger.info("black_sb %s:[%s]" % (user_id, ret_json))
    return ret_json


@users_blueprint.route('/followers/<user_id>/<limit>/<order>', methods=["GET"])
@login_required
def get_followers(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if current_user.user_id != user_id:
        if current_user.user_id != 'admin':
            app.logger.error("access deny for user not the true user")
            abort(400)

    user = User(user_id)
    ret = user.get_followers(user_id)

    ret_json = jsonify(ret)
    app.logger.info("black_sb %s:[%s]" % (user_id, ret_json))
    return ret_json


@users_blueprint.route('/blacks/<user_id>', methods=["GET"])
@login_required
def get_blacks(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    if current_user.user_id != user_id:
        if current_user.user_id != 'admin':
            app.logger.error("access deny for user not the true user")
            abort(400)

    user = User(user_id)
    ret = user.get_blocks(user_id)

    ret_json = jsonify(ret)
    app.logger.info("black_sb %s:[%s]" % (user_id, ret_json))
    return ret_json


@users_blueprint.route('/sdscore/<user_id>', methods=["GET"])
@login_required
def send_score(user_id):
    app.logger.info("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.info("current_user :%s" % current_user.user_id)

    user = User(current_user.user_id)
    ret = user.show_user()

    ret_json = jsonify(ret)
    app.logger.info("send_score %s:[%s]" % (user_id, ret_json))
    return ret_json

