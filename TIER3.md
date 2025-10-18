# Tier 3 — "Ping Me 📲" Mobile App + Local Passthrough API

This is the **Tier 3** solution for the SNHU Coding United Club’s September 2025 Coding Challenge: **Ping Me**.  
It demonstrates a secure local passthrough API that connects a React Native (Expo) mobile app to Twilio for SMS delivery.

---

## Goal

Create a **mobile app** that sends a message to your own verified number via **Twilio**, but **without embedding secrets** inside the client.  
The app talks to a **local Flask API** running on the same network, which safely handles Twilio authentication and message dispatch.

---

## Architecture

### 1. [React Native App] → [Local Flask API] → [Twilio SMS Gateway]

- **Mobile app** built with Expo (React Native + TypeScript)
- **Local API** built with Flask + Twilio SDK
- **Secrets** stored in environment variables (`.env`)
- **Endpoints**
  - `/health` — sanity check
  - `/send-ping` — POST endpoint to send SMS messages
- **Security**
  - CORS enabled for local testing
  - Only one verified phone number allowed (Twilio trial restriction)
  - Secrets never exposed to the mobile app

---

## Local Setup

### 1. Clone the repo

```bash
git clone https://github.com/<your-repo>/ping-me.git
cd ping-me
```

### 2. Environment variables

Create `local_api/.env` with:

```
TWILIO_ACCOUNT_SID=ACXXXXXXXXXXXXXXXXXXXXXXXXXXXX
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_FROM_NUMBER=+15005550006
NOTIFICATION_PHONE_NUMBER=+1XXXXXXXXXX
```

### 3. Start the local API

```bash
cd local_api
poetry install
poetry run python src/local_api/app.py
```

Should display:

```bash
Running on http://127.0.0.1:5001
Running on http://192.168.1.200:5001
```

### 4. Test the API

```bash
curl http://127.0.0.1:5001/health
```

→ `{"ok": true, "status": "healthy"}`

---

## Running the Mobile App

### 1. Configure Expo

In `mobile-app/app.json`:

```json
"extra": {
  "API_BASE": "http://192.168.1.200:5001"
}
```

_(Use your local IP.)_

### 2. Start Expo

```bash
cd mobile-app
npx expo start -c
```

Scan the QR code with **Expo Go** on your Android device.

### 3. Test connectivity

If Flask’s `/health` works in your browser on your mobile device, the app will display the same success message.

Once A2P registration completes in Twilio, pressing Send will trigger a real SMS.

You'll have to register a local phone number in Twilio and go through the A2P registration process.

---

## Unit Tests

All API endpoints except `/health` are covered by unit tests in `local_api/tests/test_app.py`. Tests mock the Twilio client to avoid real network calls.

Run them with:

```bash
poetry run pytest
```
