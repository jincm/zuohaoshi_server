#!/usr/bin/env python
# coding = "utf-8"

"""
    wsgi app for test
    Be a good man
"""


from werkzeug.serving import run_simple

if __name__ == "__main__":
    run_simple('0.0.0.0', 8000)