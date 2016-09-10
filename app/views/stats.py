from app import app
from flask import render_template


@app.route('/stats/')
def stats():
    return render_template('stats.html')
