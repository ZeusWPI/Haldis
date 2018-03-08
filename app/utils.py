# -*- coding: utf-8 -*-

from datetime import datetime
from flask import render_template

from app import app
from login import login_manager

__author__ = 'feliciaan'

@app.template_filter('euro')
def euro(value):
    result = '€' + str(value/100)
    return result

@app.template_filter('countdown')
def countdown(value, only_positive=True, show_text=True):
    delta = value - datetime.now()
    if delta.total_seconds() < 0 and only_positive:
        return "closed"
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    time = '%02d:%02d:%02d' % (hours, minutes, seconds)
    if show_text:
        return 'closes in ' + time
    return time

@app.template_filter('year')
def current_year(value):
    return str(datetime.now().year)

@app.errorhandler(404)
def handle404(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(401)
def handle401(e):
    return render_template('errors/401.html'), 401


class AnonymouseUser:
    id = None

    def is_active(self):
        return False

    def is_authenticated(self):
        return False

    def is_anonymous(self):
        return True

    def is_admin(self):
        return False

    def get_id(self):
        return None

login_manager.anonymous_user = AnonymouseUser