from flask import render_template

from app import app
__author__ = 'feliciaan'

@app.template_filter('euro')
def euro(value):
    result = '€' + str(value/100)
    return result

@app.errorhandler(404)
def handle404(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(401)
def handle401(e):
    return render_template('errors/401.html'), 401