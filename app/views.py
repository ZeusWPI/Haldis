from flask import Blueprint, request, jsonify, redirect, url_for


from app import app
from login import before_request


@app.route('/')
def home():
   return render_template('home.html')


@app.route('/about/')
def about():
   return render_template('about.html')


@app.route('/stats/')
def stats():
   return render_template('stats.html')


if app.debug:  # add route information
    @app.route('/routes')
    def list_routes(self):
        import urllib
        output = []
        for rule in app.url_map.iter_rules():
            options = {}
            for arg in rule.arguments:
                options[arg] = "[{0}]".format(arg)

            methods = ','.join(rule.methods)
            url = url_for(rule.endpoint, **options)
            line = urllib.unquote(
                "{:50s} {:20s} {}".format(rule.endpoint, methods, url))
            output.append(line)

        string = ''
        for line in sorted(output):
            string += line + "<br/>"

        return string
