import os
import logging
import uuid
from flask import Flask, jsonify, request
from flask_cors import CORS
from logging_helper import log_event

app = Flask(__name__)
CORS(app, origins=[
    os.environ.get('CORS_LOCALHOST', 'http://localhost:5173'),
    os.environ.get('CORS_URL', 'https://frontend-service-887823769496.us-central1.run.app')
])
logging.basicConfig(level=logging.INFO)


@app.route("/charges", methods=["POST"])
def charge():
    body = request.get_json(force=True) or {}
    log_event(app.logger, f"POST /charges body={body}")

    amount = body.get("amount")
    card = body.get("card", {})
    card_number = str(card.get("number", ""))

    if not amount or amount <= 0:
        log_event(app.logger, "charge rejected: invalid amount")
        return jsonify({"error": "invalid amount"}), 400
    if not card_number or len(card_number) < 12:
        log_event(app.logger, "charge rejected: invalid card")
        return jsonify({"error": "invalid card"}), 402
    if card_number.endswith("0000"):
        log_event(app.logger, "charge declined")
        return jsonify({"error": "card declined"}), 402

    transaction_id = str(uuid.uuid4())
    log_event(app.logger, f"charge succeeded, transaction_id={transaction_id}")
    return jsonify({"transaction_id": transaction_id}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))