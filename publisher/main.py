import json
import os
import flask
from flask import Flask
from google.cloud import pubsub_v1


app = Flask(__name__)


@app.route('/')
def main():
    message = flask.request.args.get("message") 
    if not message:
        return "Please provide message", 400

    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(os.environ['GOOGLE_CLOUD_PROJECT'], os.environ['TOPIC_ID'])
    future = publisher.publish(topic_path, message.encode())
    future.result()
    return ''


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
