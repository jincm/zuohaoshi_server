#!/usr/bin/env python
# encoding: utf-8
import os

from myapp.app import create_app
from flask.ext.script import Manager, Shell

import unittest
#import coverage

#from flask.ext.migrate import Migrate, MigrateCommand

app = create_app()
manager = Manager(app)


def make_shell_context():
  return dict(app=app)

manager.add_command("shell", Shell(make_context=make_shell_context))
@manager.command
def deploy():
  """Run deployment tasks."""
  pass


# migrations
# manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    else:
        return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(branch=True, include='project/*')
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report()
    basedir = os.path.abspath(os.path.dirname(__file__))
    covdir = os.path.join(basedir, 'tmp/coverage')
    cov.html_report(directory=covdir)
    print('HTML version: file://%s/index.html' % covdir)
    cov.erase()

'''
@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()
@manager.command
def drop_db():
    """Drops the db tables."""
    db.drop_all()
@manager.command
def create_admin():
    """Creates the admin user."""
    db.session.add(User("ad@min.com", "admin"))
    db.session.commit()
'''

if __name__ == '__main__':
    manager.run()

