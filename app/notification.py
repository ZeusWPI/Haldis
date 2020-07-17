"Script that handles Haldis notifications on chat platforms"
import json
import typing
from datetime import datetime
from threading import Thread

import requests
from flask import current_app as app
from flask import url_for
from models.order import Order


def webhook_text(order: Order) -> typing.Optional[str]:
    "Function that makes the text for the notification"
    if order.location_id == "test":
        return None

    if order.courier is not None:
        # pylint: disable=C0301
        return "<!channel|@channel> {3} is going to {1}, order <{0}|here>! Deadline in {2} minutes!".format(
            url_for("order_bp.order_from_id", order_id=order.id, _external=True),
            order.location_name,
            remaining_minutes(order.stoptime),
            order.courier.username.title(),
        )

    return "<!channel|@channel> New order for {}. Deadline in {} minutes. <{}|Open here.>".format(
        order.location_name,
        remaining_minutes(order.stoptime),
        url_for("order_bp.order_from_id", order_id=order.id, _external=True),
    )


def post_order_to_webhook(order: Order) -> None:
    "Function that sends the notification for the order"
    message = webhook_text(order)
    if message:
        webhookthread = WebhookSenderThread(message, app.config["SLACK_WEBHOOK"])
        webhookthread.start()


class WebhookSenderThread(Thread):
    "Extension of the Thread class, which sends a webhook for the notification"

    def __init__(self, message: str, url: str) -> None:
        super(WebhookSenderThread, self).__init__()
        self.message = message
        self.url = url

    def run(self) -> None:
        self.slack_webhook()

    def slack_webhook(self) -> None:
        "The webhook for the specified chat platform"
        if self.url:
            requests.post(self.url, json={"text": self.message})
        else:
            print(self.message)


def remaining_minutes(value) -> str:
    "Return the remaining minutes until the deadline of and order"
    delta = value - datetime.now()
    if delta.total_seconds() < 0:
        return "0"
    minutes = delta.total_seconds() // 60
    return "%02d" % minutes
