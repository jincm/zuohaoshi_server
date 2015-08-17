#!/usr/bin/env python

# coding = "utf-8"

__author__ = 'jincm1'

from flask import make_response
from flask import request



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


from yourapplication.database import db_session

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()