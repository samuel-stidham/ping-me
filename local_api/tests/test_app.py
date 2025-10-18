import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

MOCK_ENV = {
    "TWILIO_ACCOUNT_SID": "FAKE_SID",
    "TWILIO_AUTH_TOKEN": "FAKE_TOKEN",
    "TWILIO_FROM_NUMBER": "+15005550006",
    "NOTIFICATION_PHONE_NUMBER": "+16065948708",
}

with patch.dict("os.environ", MOCK_ENV):
    with patch("local_api.app.Client") as MockTwilioClientClass:
        import local_api.app

        app = local_api.app.app
        TWILIO_CLIENT = local_api.app.TWILIO_CLIENT


class ApiTest(unittest.TestCase):
    """Tests the /send-ping API route logic and mocked Twilio interaction."""

    def setUp(self):
        self.client_patcher = patch("local_api.app.TWILIO_CLIENT")
        self.mock_twilio_client = self.client_patcher.start()

        app.config["TESTING"] = True
        self.app = app.test_client()

        self.mock_twilio_client.messages.create.reset_mock()
        self.notification_number = MOCK_ENV["NOTIFICATION_PHONE_NUMBER"]

    def tearDown(self):
        self.client_patcher.stop()

    def test_send_ping_success(self):
        """Test successful message send and checks for 200 status."""

        self.mock_twilio_client.messages.create.return_value = MagicMock(
            sid="SM_API_SUCCESS"
        )

        response = self.app.post(
            "/send-ping",
            data=json.dumps({"message_body": "Hello from the mobile app."}),
            content_type="application/json",
        )

        self.mock_twilio_client.messages.create.assert_called_once()

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["sid"], "SM_API_SUCCESS")

    def test_reject_empty_message(self):
        """Test that the API rejects requests with empty or whitespace-only messages."""

        response = self.app.post(
            "/send-ping",
            data=json.dumps({"message_body": "   "}),
            content_type="application/json",
        )

        self.mock_twilio_client.messages.create.assert_not_called()

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "fail")
        self.assertIn("content cannot be empty", data["message"])

    def test_message_truncation(self):
        """Test that messages over 160 characters are truncated before sending."""

        long_message = "A" * 200
        mock_sid = "SM_TRUNCATED"

        self.mock_twilio_client.messages.create.return_value = MagicMock(sid=mock_sid)

        response = self.app.post(
            "/send-ping",
            data=json.dumps({"message_body": long_message}),
            content_type="application/json",
        )

        self.mock_twilio_client.messages.create.assert_called_once()
        sent_body = self.mock_twilio_client.messages.create.call_args[1]["body"]
        self.assertEqual(len(sent_body), 160)

        self.assertEqual(response.status_code, 200)

    def test_handle_invalid_json(self):
        """Test that the API gracefully handles non-JSON or malformed requests."""

        response = self.app.post(
            "/send-ping", data="This is not JSON", content_type="application/json"
        )

        self.mock_twilio_client.messages.create.assert_not_called()

        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "error")
        self.assertIn("Invalid JSON format", data["message"])

    def test_handle_twilio_api_error(self):
        """Test that the API catches Twilio exceptions and returns a 500 error."""

        self.mock_twilio_client.messages.create.side_effect = Exception(
            "Mock Auth Failure (Error 20003)"
        )

        response = self.app.post(
            "/send-ping",
            data=json.dumps({"message_body": "Trigger failure"}),
            content_type="application/json",
        )

        self.mock_twilio_client.messages.create.assert_called_once()

        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertEqual(data["status"], "error")
        self.assertIn("Twilio API rejected the message", data["message"])
        self.assertIn("Error 20003", data["message"])


if __name__ == "__main__":
    unittest.main()
