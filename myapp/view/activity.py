# encoding: utf-8
"""
    zuohaoshi view
    Good man is well
"""

from flask import Blueprint, request, abort

from myapp.models.db import Activity
from myapp import app

activity_blueprint = Blueprint('activity', __name__, url_prefix='/v1/activity')

@activity_blueprint.route("/hello", methods=["GET", "POST"])
def hello():
    app.logger.info("Test for activity")
    return "hello activity_blueprint"
