# Tier 1: "Desktop Ping-Me" (Upgraded to Local Web App)

This directory contains the solution for the Tier 1 challenge, which was upgraded from a Command Line Interface (CLI) to a **single-page local web application** using Python and Flask. This approach provides an immediate "tiny UI," laying the groundwork for Tier 2, while still adhering to all Tier 1 core objectives.

### Core Objectives

| Objective | Status | Implementation Detail |
| :--- | :--- | :--- |
| **Send Fixed Message** | ✅ Complete | The app sends the message "Hello from [Your Name] CLI/Web App - Tier 1 Complete!" |
| **Use Environment Variables** | ✅ Complete | Twilio credentials and phone numbers are loaded via `python-dotenv` from the ignored `.env` file. |
| **Clear Error Message** | ✅ Complete | If required environment variables are missing, the app logs a fatal error and displays an "Configuration Error" message on the web page. |
| **No Hardcoded Secrets** | ✅ Complete | All secrets are isolated to the server-side Python environment. |

---

### Setup and Configuration

This project uses **Poetry** for dependency management.

#### 1. Install Dependencies

Ensure you have Poetry installed, then install the project dependencies:

```bash
# From the ping-me/tier1/ directory
poetry install
```

#### 2. Configure Environment Variables

Create a file named `.env` inside the `ping-me/tier1/` directory. Do not commit this file.

It must contain the following variables:

```
# .env
# --- Twilio Credentials ---
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token_here

# --- Phone Numbers (E.164 format: +12223334444) ---
TWILIO_FROM_NUMBER=+15555551234
NOTIFICATION_PHONE_NUMBER=+15558675310 

# --- Flask Secret Key (Required for 'flash' messages) ---
FLASK_SECRET_KEY=a_random_key_for_local_testing
```

#### 3. Run the Application

Start the Flask development server using Poetry's run command, which executes the script within the isolated virtual environment:

```bash
poetry run python src/tier1/app.py
```

#### How to Run

1. Open your web browser to the displayed address (usually http://127.0.0.1:5000/).
2. Click the "Ping Me" button.
3. The Python console will log the API call, and the UI will display a success or failure message.

#### What I Learned

- **Secure Credential Loading**: Successfully implemented `python-dotenv` and confirmed environment variables are loaded securely into the Flask application context.
- **Centralized Error Handling**: Created a robust initial check to ensure all four required environment variables are present before attempting to instantiate the Twilio client, providing a clear error message as required.
- **Web Framework Basics**: Established a minimal, functional Flask application that handles routing (`/`), form submission (`POST`), and displays real-time status updates using Bootstrap 5 and Flask's `flash` messaging system.
