import json
from datetime import datetime
from threading import Thread

import requests
from flask import current_app as app
from flask import url_for


def post_order_to_webhook(order_item):
    message = ""
    if order_item.courrier is not None:
        message = "<!channel|@channel> {3} is going to {1}, order <{0}|here>! Deadline in {2} minutes!".format(
            url_for("order_bp.order", id=order_item.id, _external=True),
            order_item.location.name,
            remaining_minutes(order_item.stoptime),
            order_item.courrier.username.title(),
        )
    else:
        message = "<!channel|@channel> New order for {}. Deadline in {} minutes. <{}|Open here.>".format(
            order_item.location.name,
            remaining_minutes(order_item.stoptime),
            url_for("order_bp.order", id=order_item.id, _external=True),
        )
    webhookthread = WebhookSenderThread(message)
    webhookthread.start()


class WebhookSenderThread(Thread):
    def __init__(self, message):
        super(WebhookSenderThread, self).__init__()
        self.message = message

    def run(self):
        self.slack_webhook()

    def slack_webhook(self):
        js = json.dumps({"text": self.message})
        url = app.config["SLACK_WEBHOOK"]
        if len(url) > 0:
            requests.post(url, data=js)
        else:
            app.logger.info(str(js))


def remaining_minutes(value):
    delta = value - datetime.now()
    if delta.total_seconds() < 0:
        return "0"
    minutes, _ = divmod(delta.total_seconds(), 60)
    return "%02d" % minutes
