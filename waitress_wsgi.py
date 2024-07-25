import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from waitress import serve

from app.app import create_app
from app.config import Configuration

if __name__ == "__main__":
    if Configuration.SENTRY_DSN:
        sentry_sdk.init(dsn=Configuration.SENTRY_DSN, integrations=[FlaskIntegration()])

    app = create_app()
    serve(app, host="0.0.0.0", port=8000)
