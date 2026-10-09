import logging
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)


@app.route("/emails/<user_id>", methods=["POST"])
def send_email(user_id):
    body = request.get_json(force=True) or {}
    app.logger.info("POST /emails/%s body=%s", user_id, body)
    return jsonify({"status": "sent", "user_id": user_id}), 200


if __name__ == "__main__":
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))