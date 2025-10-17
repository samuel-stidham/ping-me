# Tier 2: "Custom Message to Self" (Web UI + Validation)

This directory implements the Tier 2 challenge by upgrading the Tier 1 web application to handle custom user input, validating the message content before attempting to send an SMS via Twilio.

### Core Objectives

| Objective                         | Status      | Implementation Detail                                                                                                     |
| :-------------------------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------ |
| **Custom Message Input**          | ✅ Complete | Replaced the fixed message with an editable `<textarea>` to capture user input.                                           |
| **Reject Empty Messages**         | ✅ Complete | The Flask application logic performs a server-side `.strip()` check and flashes an error if the message is empty.         |
| **Trim >160 Chars**               | ✅ Complete | Messages over 160 characters are truncated before the Twilio API call, and a warning is flashed to the user.              |
| **Show "Sending → Success/Fail"** | ✅ Complete | Uses Flask's `flash` messaging system to provide immediate status feedback (success, validation warning, or API failure). |
| **Secrets Isolation**             | ✅ Complete | All Twilio credentials remain securely isolated on the server-side Python environment.                                    |

---

### Setup and Configuration

This solution uses the same Python/Poetry environment as Tier 1.

#### 1. Configure Environment Variables

The application requires the same set of environment variables in the **`.env`** file placed in this directory:

```
# .env
# --- Twilio Credentials ---
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here
TWILIO_FROM_NUMBER=+15555551234
NOTIFICATION_PHONE_NUMBER=+15558675310

# --- Flask Secret Key (Required for web app security) ---
FLASK_SECRET_KEY=a_random_key_for_local_testing
```

#### 2. Run the Application

Start the Flask development server:

```bash
# From the ping-me/tier2/ directory
poetry install
poetry run python src/tier2/app.py

```

---

### What I Learned

- **Input Validation Logic:** Successfully implemented server-side validation to enforce message rules (non-empty, truncation), which is critical for robust external API consumption.

- **User Feedback (UX):** Improved the user experience by using Flask's flash messages to clearly communicate the result of the `POST` request, whether it was a validation error, a successful send, or an API failure.

- **Testing Decoupling:** Wrote unit tests that fully mock the Twilio API, confirming the application's validation and routing logic works perfectly without relying on an active external service or production credentials.
