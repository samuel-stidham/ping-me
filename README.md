# 📲 Ping Me! - SNHU Coding United Challenge

This repository contains my solutions for the "Ping Me 📲" coding challenge presented by the SNHU Coding United club. The challenge is designed to explore APIs, UI development, and system design by building a tiny messaging application in escalating tiers.

---

### Ground Rules & Constraints

- **Privacy:** Only send messages to your own verified number using a Twilio trial account.
- **Secrets:** All API credentials (e.g., `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`) are stored as environment variables. **No secrets are hardcoded.**
- **Deliverables:**
  - `README.md`: This file, explaining the project.
  - A 30–60 second screen capture for each successful tier.
  - Short notes on what I learned in each tier's specific directory.

---

### Repository Structure

Each tier's solution is contained within its own directory, representing a complete, independent application. This structure allows for a clear progression from a simple command-line tool to a complex, distributed mobile application.

```sh
$ tree
.
├── hosted-api
├── local-api
├── mobile-app
├── README.md
├── tier1
└── tier2
```

---

### Tier 1: Easy ("Desktop ping-me")

A command-line interface (CLI) application that sends a fixed message to my verified number using the Twilio REST API.

- **Technology:** [e.g., Python, Node.js, Go]
- **Key Learnings:** Handling environment variables, making basic REST API calls, and robust error handling for missing credentials.

---

### Tier 2: Medium ("Custom message to self")

A simple desktop or web application with a user interface (UI) to type and send a custom message.

- **Technology:** [e.g., HTML/CSS/JS, a desktop framework]
- **Key Learnings:** Building a basic UI, client-side input validation (message length, empty input), and providing user feedback (e.g., "sending" status, success/failure).

---

### Tier 3: Hard ("Mobile app + local passthrough API")

This tier consists of two parts that work together: a **mobile application** and a **local passthrough API**. The mobile app sends a message to the local API, which then securely forwards the request to Twilio. The mobile app does not directly interact with Twilio or my secrets.

- **Mobile App Technology:** [e.g., React Native/Expo, Flutter]
- **Local API Technology:** [e.g., Node.js with Express, Python with Flask]
- **Key Learnings:** Client-server communication, isolating API keys and secrets from the client, and foundational network architecture.

---

### Tier 4: LEET ("Mobile app + hosted API")

An extension of Tier 3, this tier moves the passthrough API from my local machine to a cloud service. The mobile app is updated to call the hosted API URL. This tier also adds a basic authentication layer using a static API key in the request header.

- **Cloud Hosting:** [e.g., Heroku, Render, Fly.io]
- **Key Learnings:** Deploying a web service, API design for production, client-side authentication, and managing hosted environments.

---

### Get Started

To run any of the tiers, you will need a Twilio account and a verified phone number. Ensure you have the required environment variables set for each tier's application. Refer to the individual `README.md` file within each directory for specific setup and usage instructions.
