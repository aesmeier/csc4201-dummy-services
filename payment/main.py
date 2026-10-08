import logging
import uuid
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/charges", methods=["POST"])
def charge():
    body = request.get_json(force=True) or {}
    app.logger.info("POST /charges body=%s", body)

    amount = body.get("amount")
    card = body.get("card", {})
    card_number = str(card.get("number", ""))

    if not amount or amount <= 0:
        return jsonify({"error": "invalid amount"}), 400
    if not card_number or len(card_number) < 12:
        return jsonify({"error": "invalid card"}), 402
    if card_number.endswith("0000"):
        return jsonify({"error": "card declined"}), 402

    transaction_id = str(uuid.uuid4())
    return jsonify({"transaction_id": transaction_id}), 200


if __name__ == "__main__":
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))