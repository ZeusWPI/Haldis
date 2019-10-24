"View used for debugging Haldis"
from flask import Blueprint
from flask import current_app as app
from flask import url_for
from flask_login import login_required

debug_bp = Blueprint("debug_bp", __name__)


@debug_bp.route("/routes")
@login_required
def list_routes() -> str:
    "List all routes of the application"
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
        print(rule.endpoint)
        methods = ",".join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote(
            "{:50s} {:20s} {}".format(rule.endpoint, methods, url)
        )
        output.append(line)

    string = ""
    for line in sorted(output):
        string += line + "<br/>"

    return string
