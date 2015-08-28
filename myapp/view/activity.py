# encoding: utf-8
"""
    zuohaoshi view
    Good man is well
"""

from flask import Blueprint, request, abort

from myapp.models.activity import Activity
from myapp import app

activity_blueprint = Blueprint('activity', __name__, url_prefix='/v1/activity')

@activity_blueprint.route("/hello", methods=["GET", "POST"])
def hello():
    activity = Activity()
    app.logger.info("Test for activity")
    return "hello activity_blueprint"
