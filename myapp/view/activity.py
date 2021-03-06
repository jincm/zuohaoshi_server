# encoding: utf-8
"""
    zuohaoshi view
    Good man is well
"""
import os
from  datetime import date
import time

from bson import ObjectId, json_util

from flask import Blueprint, request, abort, jsonify
from flask.ext.login import login_required, current_user
from werkzeug.utils import secure_filename

from myapp.models.activity import Activity
from myapp.models.user import User
from myapp.ext.file_oss import oss_upload_file as upload_file_to_store
from myapp import app

activity_blueprint = Blueprint('activity', __name__, url_prefix='/api/v1/activity')  # activity


@activity_blueprint.route("/<post_type>/post", methods=["POST"])
@login_required
def post_activity(post_type):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:%s,current_user:%s\n" % (post_type, current_user.user_id))
    post_data = request.json
    if post_data is None:
        app.logger.error("missing parameters:%s" % post_data)
        abort(400)

    # post activity
    if "token" in post_data:
        try:
            del post_data["token"]
        except Exception, e:
            app.logger.error("del key error:%s", e)

    if 'uid' not in post_data:
        post_data['uid'] = current_user.user_id

    ret = Activity.post_activity(current_user.user_id, post_type, post_data, post_id=None)

    app.logger.debug("post activity ret [%s]\n" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/<post_id>/upload_imgs", methods=["POST"])
@login_required
def post_activity_upload_imgs(post_type, post_id):
    app.logger.debug("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.debug("current_user :%s" % current_user.user_id)
    app.logger.debug("start upload file")

    # upload new head portrait to store and update post's url
    app.logger.debug("files :%s" % request.files)
    if request.files is None:
        app.logger.error("missing something:file key is lost")
        abort(400)

    img_info = dict()
    img_urls = []
    for one_file in request.files.getlist('file'):
        post_file = one_file # request.files.get(one_file)

        # get file and save it to local tmp
        fname = secure_filename(post_file.filename)
        ext_name = fname.split('.')[-1]
        obj_id = str(ObjectId())
        pic_name = '%s.%s' % (obj_id, ext_name)

        localfile = os.path.join(app.config['UPLOAD_FOLDER'], pic_name)
        app.logger.debug("start upload file to local store:[%s],[%s]" % (pic_name, localfile))
        post_file.save(localfile)

        # upload file to oss
        pic_url = 'zuohaoshi/%s/%s' % (post_type, post_id)

        file_url = upload_file_to_store(pic_url, pic_name, localfile)
        if file_url is None:
            app.logger.error("file upload failed")
            abort(400)

        app.logger.debug("end upload file to store:%s\n" % file_url)
        # delete local tmp file
        os.remove(localfile)

        img_urls.append(file_url)

    if img_urls:
        # update post's info
        img_info['img_urls'] = img_urls
        ret = Activity.post_activity(current_user.user_id, post_type, img_info, post_id)
        app.logger.debug("modify post image %s:[%s]\n" % (post_id, ret))
        return jsonify(ret)

# add for only upload file
@activity_blueprint.route("/upload_imgs", methods=["POST"])
@login_required
def upload_imgs():
    app.logger.debug("request:[%s],[%s],[%s]" % (request.headers, request.args, request.json))
    app.logger.debug("current_user :%s" % current_user.user_id)
    app.logger.debug("start upload file")

    # upload new head portrait to store and update post's url
    app.logger.debug("files :%s" % request.files)
    if request.files is None:
        app.logger.error("missing something:file key is lost")
        abort(400)
    if request.files.getlist('file') is None:
        app.logger.error("missing something:file key is lost")
        abort(400)

    d = date.today()
    month = '%d%02d' % (d.year, d.month)

    img_urls = []
    for one_file in request.files.getlist('file'):
        post_file = one_file  # request.files.get(one_file)

        # get file and save it to local tmp
        fname = secure_filename(post_file.filename)

        # ext_name = fname.split('.')[-1]
        # obj_id = str(ObjectId())
        # pic_name = '%s.%s' % (obj_id, ext_name)
        # app.logger.debug("fname:%s,pic_name:%s\n" % (fname, pic_name))

        pic_name = fname

        localfile = os.path.join(app.config['UPLOAD_FOLDER'], pic_name)
        app.logger.debug("start upload file to local store:[%s],[%s]" % (pic_name, localfile))
        post_file.save(localfile)

        # upload file to oss
        pic_url = 'zuohaoshi/%s/%s' % (current_user.user_id, month)

        file_url = upload_file_to_store(pic_url, pic_name, localfile)
        if file_url is None:
            app.logger.error("file upload failed")
            abort(400)

        app.logger.debug("end upload file to store:%s\n" % file_url)
        # delete local tmp file
        os.remove(localfile)

        img_urls.append(file_url)

    if img_urls:
        # update post's info
        # img_info['img_urls'] = img_urls
        # ret = Activity.post_activity(current_user.user_id, post_type, img_info, post_id)
        app.logger.debug("upload images %s [%s]\n" % (current_user.user_id, img_urls))
        return jsonify({'img_urls': img_urls})

@activity_blueprint.route("/<post_type>/<post_id>", methods=['GET'])
@login_required
def get_activity(post_type, post_id):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.get_one_activity()
    app.logger.debug("get_activity:%s" % ret)

    return jsonify(ret)

# comment or praise
@activity_blueprint.route("/<post_type>/<post_id>/comment", methods=["POST"])
@login_required
def post_activity_comment(post_type, post_id):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    comment = request.json
    if comment is None:
        app.logger.error("missing parameters content:%s" % post_id)
        abort(400)

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.post_comment(comment)
    app.logger.debug("post_activity_comment:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/<post_id>/<comment_id>", methods=['DELETE'])
@login_required
def del_activity_comment(post_type, post_id, comment_id):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s,%s,%s],user:%s\n" % (post_type, post_id, comment_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.del_comment(comment_id)
    app.logger.debug("post_activity_comment:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/<post_id>", methods=['DELETE'])
@login_required
def del_activity(post_type, post_id):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.del_activity()
    app.logger.debug("get_activity:%s" % ret)
    return jsonify(ret)

@activity_blueprint.route("/<user_id>/<post_type>/posts", methods=['GET'])
@login_required
def get_sb_activities(user_id, post_type):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s]user:[%s],current_user:%s\n" % (post_type, user_id, current_user.user_id))

    limit = request.args.get("limit")
    offset = request.args.get("offset")
    if not limit:
        limit = 50
    if not offset:
        offset = 0

    activity = Activity(current_user.user_id, post_type)
    ret = activity.get_sb_activity(user_id, int(limit), int(offset))
    ret_json = jsonify(ret)
    app.logger.debug("get_sb_activities:%s\n%s" % (ret, ret_json))
    return ret_json


@activity_blueprint.route("/search/<post_type>", methods=['POST'])
def search_activity(post_type):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s]\n" % post_type)
    limit = 20
    offset = 0
    fields = None
    args = dict()
    for one in request.json:
        if one == "limit":
            limit = int(request.args.get("limit"))
        elif one == "offset":
            offset = int(request.args.get("offset"))
        elif one == "fields":
            fields = request.args.get("fields")
        else:
            args['%s' % one] = request.args.get(one)

    # search posts by some conditions, example pos/time/read_nums/
    activity = Activity(post_type=post_type)
    ret = activity.activity_search(args, fields, limit, offset)

    app.logger.debug("search_activity:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/lost/face_match", methods=['POST'])
@login_required
def lost_face_match():
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    img1 = request.json.get('img1')
    img2 = request.json.get('img2')
    if img1 is None or img2 is None:
        app.logger.error("missing parameters img:%s" % request.json)
        abort(400)

    activity = Activity(current_user.user_id, "lost")
    ret = activity.lost_face_match(img1, img2)
    app.logger.debug("lost_face_match:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_type>/<post_id>/track", methods=['POST'])
@login_required
def track_activity(post_type, post_id):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    track = request.json.get("track")
    if track is None:
        app.logger.error("missing parameters track:%s" % track)
        abort(400)

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.track_activity(track)
    app.logger.debug("track_activity:%s" % ret)
    return jsonify(ret)

@activity_blueprint.route("/<post_type>/<post_id>/share", methods=['POST'])
@login_required
def share_activity(post_type, post_id):
    app.logger.debug("request:[%s],[%s],[%s]\n" % (request.headers, request.args, request.json))
    app.logger.debug("type:[%s,%s],current_user:%s\n" % (post_type, post_id, current_user.user_id))

    activity = Activity(current_user.user_id, post_type, post_id)
    ret = activity.share_one_activity()
    app.logger.debug("share_activity:%s" % ret)
    return jsonify(ret)




