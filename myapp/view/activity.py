# encoding: utf-8
"""
    zuohaoshi view
    Good man is well
"""
import os
import time

from flask import Blueprint, request, abort, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename

from myapp.models.activity import Activity
from myapp.models.user import User
from myapp.ext.file_oss import oss_upload_file as upload_file_to_store
from myapp import app

activity_blueprint = Blueprint('activity', __name__, url_prefix='/1/ay')  # activity


@activity_blueprint.route("/<post_type>/post", methods=["POST"])
@login_required
def post_activity(post_type):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:%s,current_user:%s\n" % (post_type, current_user.user_id))
    token = request.args.get("token")
    info = request.json
    if token is None or info is None:
        app.logger.error("missing parameters:%s,%s" % (token, info))
        abort(400)

    # if it has files, save them into aliyun, and make the url
    f = request.files['file']
    fname = secure_filename(f.filename)
    localfile = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    app.logger.info("start upload file to store:%s,%s" % (fname, localfile))
    f.save(localfile)
    res = upload_file_to_store('zuohaoshi/2015/beijing', fname, localfile)
    app.logger.info("end upload file to store:%s,%s" % (res.status, res.read()))

    # post activity
    ret = Activity.post_activity(current_user.user_id, post_type, info)

    app.logger.info("post activity ret [%s]\n" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<user_id>/posts", methods=['GET'])
@login_required
def get_sb_activities(user_id):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, user_id))

    limit = request.args.get("limit")
    offset = request.args.get("offset")
    if not limit:
        limit = 10
    if not offset:
        offset = 0

    # activities = User(user_id).get_sb_activities()
    user = User(user_id)
    user_info = user.show_user()

    activities = user_info

    app.logger.info("get_sb_activities:%s" % activities)
    for one in activities:
        activity = Activity(post_id, current_user.user_id)
        ret = activity.get_one_activity()

    app.logger.info("get_sb_activities:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/<post_id>", methods=['GET'])
@login_required
def get_activity(post_type, post_id):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.get_one_activity()
    app.logger.info("get_activity:%s" % ret)

    return jsonify(ret)

@activity_blueprint.route("/<post_type>/<post_id>", methods=['DELETE'])
@login_required
def del_activity(post_type, post_id):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.del_activity()
    app.logger.info("get_activity:%s" % ret)
    return jsonify(ret)


# comment or praise
@activity_blueprint.route("/<post_type>/<post_id>/comment", methods=["POST"])
@login_required
def post_activity_comment(post_type, post_id):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    comment = request.json.get("comment")
    if comment is None:
        app.logger.error("missing parameters content:%s" % comment)
        abort(400)

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.post_comment(comment)
    app.logger.info("post_activity_comment:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/<post_id>/<comment_id>", methods=['DELETE'])
@login_required
def del_activity_comment(post_type, post_id, comment_id):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:[%s,%s,%s],user:%s\n" % (post_type, post_id, comment_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.del_comment(comment_id)
    app.logger.info("post_activity_comment:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/<post_id>/track", methods=['POST'])
@login_required
def track_activity(post_type, post_id):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    track = request.json.get("track")
    if track is None:
        app.logger.error("missing parameters track:%s" % track)
        abort(400)

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.track_activity(track)
    app.logger.info("track_activity:%s" % ret)
    return jsonify(ret)

@activity_blueprint.route("/<post_type>/<post_id>/share", methods=['POST'])
@login_required
def share_activity(post_type, post_id):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.share_one_activity()
    app.logger.info("share_activity:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/search", methods=['POST'])
@login_required
def search_activity(post_type):
    app.logger.info("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.info("type:[%s],current_user:%s\n" % (post_type, current_user.user_id))
    search = request.json.get("search")
    if search is None:
        app.logger.error("missing parameters track:%s" % search)
        abort(400)

    activity = Activity(current_user.user_id, post_type)
    ret = activity.activity_search(search)
    app.logger.info("search_activity:%s" % ret)
    return jsonify(ret)

