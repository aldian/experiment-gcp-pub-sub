import base64
import logging
import os
import time

from flask import Flask
from googleapiclient.discovery import build


app = Flask(__name__)


@app.route('/')
def main():
    service = build('pubsub', 'v1')

    subscription_path = 'projects/{project_id}/subscriptions/{subscription_id}'.format(
        project_id=os.environ['GOOGLE_CLOUD_PROJECT'],
        subscription_id=os.environ['SUBSCRIPTION_ID'],
    )

    while True:
        response = service.projects().subscriptions().pull(
            subscription=subscription_path, body={
                "returnImmediately": False,
                "maxMessages": 10000,
            }
        ).execute()

        if not response:
            time.sleep(10)
            continue
        received_messages = response.get('receivedMessages')
        if not received_messages:
            time.sleep(10)
            continue

        response = service.projects().subscriptions().acknowledge(subscription=subscription_path, body={
            "ackIds": [message['ackId'] for message in received_messages]
        }).execute()
        if response:
            logging.info("ACKNOWLEDGEMENT ERROR: {}".format(response))

        for message in received_messages:
            body = message["message"]
            data = base64.b64decode(body["data"])
            publish_time = body["publishTime"]
            message_id = body["messageId"]
            logging.info("MESSAGE {}: {}".format(publish_time, data))

    return ''


@app.route('/_ah/start')
def start():
    return main()


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500