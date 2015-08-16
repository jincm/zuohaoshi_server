#!/usr/bin/env python

# coding = "utf-8"

__author__ = 'jincm1'

from flask import make_response
from flask import request



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)