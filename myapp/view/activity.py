# encoding: utf-8
"""
    zuohaoshi view
    Good man is well
"""
from flask import Blueprint, request, abort, jsonify
from flask.ext.login import login_required, current_user

from myapp.models.activity import Activity
from myapp.models.user import User
from myapp import app

activity_blueprint = Blueprint('activity', __name__, url_prefix='/1/ay')#activity

@activity_blueprint.route("/post", methods=["POST"])
@login_required
def post_activity():
    app.logger.info("post activity:%s,%s" % (request.headers, request.json))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))
    token = request.args.get("token")
    content = request.json.get("content")
    if token is None or content is None:
        app.logger.error("missing parameters:%s,%s" % (token,content))
        abort(400)

    #if it has files
    f = request.files['file']
    fname = secure_filename(f.filename)
    localfile = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    app.logger.info("start upload file to store:%s,%s" % (fname, localfile))

    f.save(localfile)
    res = upload_file_to_store('zuohaoshi/2015/beijing', fname, localfile)
    app.logger.info("end upload file to store:%s,%s" % (res.status, res.read()))
    #return jsonify({'file': fname})

    #activity = Activity()
    ret = Activity.post_activity(current_user.user_id, content)

    app.logger.info("post activity:%s" % ret)
    return jsonify(ret)

@activity_blueprint.route("/<post_id>", methods=['GET'])
@login_required
def get_activity(post_id):
    app.logger.info("get activity:%s,%s,%s" % (post_id, request.headers, request.args))

    #token = request.args.get("token")
    #app.logger.info("token:%s" % token)
    #if not token:
    #    app.logger.error("token:%s" % token)
    #    abort(400)
    #user = User.get_user_fromtoken(token)
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    activity = Activity(post_id, current_user.user_id)
    ret = activity.get_one_activity()
    app.logger.info("get_activity:%s" % ret)

    return jsonify(ret)

@activity_blueprint.route("/search", methods=['GET'])
@login_required
def search_activity():
    app.logger.info("get activity:%s,%s" % (request.headers, request.args))

@activity_blueprint.route("/<post_id>", methods=['DELETE'])
@login_required
def del_activity(post_id):
    app.logger.info("get activity:%s,%s,%s" % (post_id, request.headers, request.args))

    #token = request.args.get("token")
    #app.logger.info("token:%s" % token)
    #if not token:
    #    app.logger.error("token:%s" % token)
    #    abort(400)
    #user = User.get_user_fromtoken(token)
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    activity = Activity(post_id, current_user.user_id)
    ret = activity.get_one_activity()
    app.logger.info("get_activity:%s" % ret)

    return jsonify(ret)


#comment
@activity_blueprint.route("/post_cm", methods=["POST"])
@login_required
def post_activity_comment(<post_id>):
    app.logger.info("post activity:%s,%s" % (request.headers, request.json))
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))
    token = request.args.get("token")
    content = request.json.get("content")
    if token is None or content is None:
        app.logger.error("missing parameters:%s,%s" % (token,content))
        abort(400)

    #if it has files
    f = request.files['file']
    fname = secure_filename(f.filename)
    localfile = os.path.join(app.config['UPLOAD_FOLDER'], fname)
    app.logger.info("start upload file to store:%s,%s" % (fname, localfile))

    f.save(localfile)
    res = upload_file_to_store('zuohaoshi/2015/beijing', fname, localfile)
    app.logger.info("end upload file to store:%s,%s" % (res.status, res.read()))
    #return jsonify({'file': fname})

    #activity = Activity()
    ret = Activity.post_activity(current_user.user_id, content)

    app.logger.info("post activity:%s" % ret)
    return jsonify(ret)


@activity_blueprint.route("/<post_id>/<comment_id>", methods=['DELETE'])
@login_required
def del_activity_comment(post_id,comment_id):
    app.logger.info("get activity:%s,%s,%s" % (post_id, request.headers, request.args))

    #token = request.args.get("token")
    #app.logger.info("token:%s" % token)
    #if not token:
    #    app.logger.error("token:%s" % token)
    #    abort(400)
    #user = User.get_user_fromtoken(token)
    app.logger.info("current_user :%s,%s" % (current_user, current_user.user_id))

    activity = Activity(post_id, current_user.user_id)
    ret = activity.get_one_activity()
    app.logger.info("get_activity:%s" % ret)

    return jsonify(ret)