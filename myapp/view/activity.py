
# coding = "utf-8"

"""
    zuohaoshi view
    Good man is well
"""

from flask import Blueprint, request, abort
from myapp.models.db import Haoshi_User


activity_blueprint = Blueprint('activity', __name__, url_prefix='/v1/activity')

@activity_blueprint.route("/hello", methods=["GET", "POST"])
def hello():
    print "hello activity_blueprint"