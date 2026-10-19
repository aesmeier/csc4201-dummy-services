import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
from logging_helper import log_event

app = Flask(__name__)
CORS(app, origins=[
    os.environ.get('CORS_LOCALHOST', 'http://localhost:5173'),
    os.environ.get('CORS_URL', 'https://frontend-service-887823769496.us-central1.run.app')
])
logging.basicConfig(level=logging.INFO)


@app.route("/emails/<user_id>", methods=["POST"])
def send_email(user_id):
    body = request.get_json(force=True) or {}
    log_event(app.logger, f"POST /emails/{user_id} body={body}")
    return jsonify({"status": "sent", "user_id": user_id}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))