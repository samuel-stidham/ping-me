import os
import sys
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from twilio.rest import Client

FIXED_MESSAGE = "Hello from Samuel Stidham CLI/Web App - Tier 1 Complete!"

TWILIO_CLIENT = None
TWILIO_FROM_NUMBER = None
NOTIFICATION_PHONE_NUMBER = None
FLASK_DEBUG_MODE = True

# Load environment variables
load_dotenv()

try:
    # Load all required variables (will raise KeyError if missing)
    FLASK_SECRET_KEY = os.environ["FLASK_SECRET_KEY"]
    NOTIFICATION_PHONE_NUMBER = os.environ["NOTIFICATION_PHONE_NUMBER"]
    TWILIO_ACCOUNT_SID = os.environ["TWILIO_ACCOUNT_SID"]
    TWILIO_AUTH_TOKEN = os.environ["TWILIO_AUTH_TOKEN"]
    TWILIO_FROM_NUMBER = os.environ["TWILIO_FROM_NUMBER"]

    # Initialize the TWilio REST Client
    TWILIO_CLIENT = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
except KeyError as e:
    print(
        f"FATAL ERROR: Required environment variable {e} is not set.", file=sys.stderr
    )
    print(
        "Please check your .env file and ensure all required variables are loaded.",
        file=sys.stderr,
    )
    sys.exit(1)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = FLASK_SECRET_KEY


@app.route("/", methods=["GET", "POST"])
def index():

    context = {"NOTIFICATION_PHONE_NUMBER": NOTIFICATION_PHONE_NUMBER}

    if request.method == "POST":
        message_body = FIXED_MESSAGE
        recipient_number = request.form.get("recipient_number")

        if TWILIO_CLIENT is None:
            flash(
                "Configuration Error: Twilio credentials missing or client failed to initialize.",
                "error",
            )
            return redirect(url_for("index"))

        try:
            message = TWILIO_CLIENT.messages.create(
                to=recipient_number,
                from_=TWILIO_FROM_NUMBER,
                body=message_body,
            )
            flash(
                f"Success! Message sent to {NOTIFICATION_PHONE_NUMBER}. SID: {message.sid}",
                "success",
            )
        except Exception as e:
            print(f"Twilio Error: {e}", file=sys.stderr)
            flash(f"API Error: Message failed to send. {e}", "error")

        return redirect(url_for("index"))

    return render_template("index.html", **context)


if __name__ == "__main__":
    app.run(debug=FLASK_DEBUG_MODE)
