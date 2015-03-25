# import sqlite3
from flask import Flask, request, render_template

# Config
DATABASE = '/db/foodbot.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'tetten'

app = Flask(__name__)
app.config.from_object(__name__)

 
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/stats/')
def stats():
    return render_template('stats.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    else:
        return render_template('login.html')

 
if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0')