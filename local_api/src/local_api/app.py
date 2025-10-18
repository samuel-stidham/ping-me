import os
import sys
import json
from twilio.rest import Client
from dotenv import load_dotenv
from flask import Flask, request, jsonify, redirect, url_for, flash
from flask_cors import CORS


load_dotenv()

TWILIO_CLIENT = None
TWILIO_FROM_NUMBER = None
NOTIFICATION_PHONE_NUMBER = None

try:
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
    TWILIO_FROM_NUMBER = os.environ["TWILIO_FROM_NUMBER"]
    NOTIFICATION_PHONE_NUMBER = os.environ["NOTIFICATION_PHONE_NUMBER"]

    # Initialize the Twilio REST Client
    TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
except KeyError as e:
    print(
        f"FATAL API ERROR: Missing required environment variable {e}.", file=sys.stderr
    )
    print("API will not be able to send messages.", file=sys.stderr)

app = Flask(__name__)
CORS(app)


@app.route("/send-ping", methods=["POST"])
def send_ping():
    """Receives JSON from the mobile app and forwards the request to Twilio."""

    if TWILIO_CLIENT is None:
        return (
            jsonify(
                {
                    "status": "error",
                    "message": "Server configuration error: Twilio client failed to initialize.",
                }
            ),
            500,
        )

    try:
        data = request.get_json()
    except Exception:
        return jsonify({"status": "error", "message": "Invalid JSON format."}), 400

    message_body = data.get("message_body", "").strip()
    recipient_number = NOTIFICATION_PHONE_NUMBER

    if not message_body:
        return (
            jsonify({"status": "fail", "message": "Message content cannot be empty."}),
            400,
        )

    if len(message_body) > 160:
        message_body = message_body[:160]

    try:
        message = TWILIO_CLIENT.messages.create(
            to=recipient_number,
            from_=TWILIO_FROM_NUMBER,
            body=message_body,
        )

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "SMS successfully queued by Twilio.",
                    "sid": message.sid,
                }
            ),
            200,
        )

    except Exception as e:
        print(f"Twilio API Error: {e}", file=sys.stderr)
        return (
            jsonify(
                {
                    "status": "error",
                    "message": f"Twilio API rejected the message: {str(e)}",
                }
            ),
            500,
        )


@app.route("/health")
def health():
    return jsonify({"ok": True, "status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
