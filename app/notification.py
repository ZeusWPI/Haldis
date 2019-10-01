import json
import typing
from datetime import datetime
from threading import Thread

import requests
from flask import current_app as app
from flask import url_for
from models.order import Order


def webhook_text(order_item: Order) -> typing.Optional[str]:
    if "Testlocation" in order_item.location.name:
        return None

    if order_item.courrier is not None:
        return "<!channel|@channel> {3} is going to {1}, order <{0}|here>! Deadline in {2} minutes!".format(
            url_for("order_bp.order", id=order_item.id, _external=True),
            order_item.location.name,
            remaining_minutes(order_item.stoptime),
            order_item.courrier.username.title(),
        )

    return "<!channel|@channel> New order for {}. Deadline in {} minutes. <{}|Open here.>".format(
        order_item.location.name,
        remaining_minutes(order_item.stoptime),
        url_for("order_bp.order", id=order_item.id, _external=True),
    )


def post_order_to_webhook(order_item: Order) -> None:
    message = webhook_text(order_item)
    if message:
        webhookthread = WebhookSenderThread(message, app.config["SLACK_WEBHOOK"])
        webhookthread.start()


class WebhookSenderThread(Thread):
    def __init__(self, message: str, url: str) -> None:
        super(WebhookSenderThread, self).__init__()
        self.message = message
        self.url = url

    def run(self) -> None:
        self.slack_webhook()

    def slack_webhook(self) -> None:
        if self.url:
            requests.post(self.url, json={"text": self.message})
        else:
            print(self.message)


def remaining_minutes(value) -> str:
    delta = value - datetime.now()
    if delta.total_seconds() < 0:
        return "0"
    minutes = delta.total_seconds() // 60
    return "%02d" % minutes
