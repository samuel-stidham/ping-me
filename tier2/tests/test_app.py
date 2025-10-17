import unittest
from unittest.mock import patch, MagicMock
from twilio.base.exceptions import TwilioRestException
import os
import sys

MOCK_ENV = {
    "TWILIO_ACCOUNT_SID": "FAKE_SID",
    "TWILIO_AUTH_TOKEN": "FAKE_TOKEN",
    "TWILIO_FROM_NUMBER": "+15005550006",
    "NOTIFICATION_PHONE_NUMBER": "+16065948708",
    "FLASK_SECRET_KEY": "TEST_SECRET",
}

with patch.dict("os.environ", MOCK_ENV):
    from src.tier2.app import app, TWILIO_CLIENT


class TwilioTest(unittest.TestCase):
    """Tests the / route logic, validation, and mocked Twilio interaction for Tier 2."""

    def setUp(self):
        self.client_patcher = patch("src.tier2.app.TWILIO_CLIENT")
        self.mock_twilio_client = self.client_patcher.start()

        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app.test_client()

        self.mock_twilio_client.messages.create.reset_mock()

        self.notification_number = MOCK_ENV["NOTIFICATION_PHONE_NUMBER"]

    def tearDown(self):
        self.client_patcher.stop()

    def test_send_success(self):
        """Test successful message send confirms the message body is used (Tier 2)."""

        self.mock_twilio_client.messages.create.return_value = MagicMock(
            sid="SM_MOCK_SUCCESS"
        )
        test_message = "This is a custom message for Tier 2 testing."

        response = self.app.post(
            "/",
            data={
                "message_body": test_message,
                "recipient_number": self.notification_number,
            },
            follow_redirects=True,
        )

        self.mock_twilio_client.messages.create.assert_called_once()
        sent_body = self.mock_twilio_client.messages.create.call_args[1]["body"]
        self.assertEqual(sent_body, test_message)

        self.assertIn(b"Success! Message sent", response.data)
        self.assertEqual(response.status_code, 200)

    def test_empty_message_rejection(self):
        """Test rejection of empty message (Tier 2 validation requirement)."""

        response = self.app.post(
            "/",
            data={
                "message_body": "   ",
                "recipient_number": self.notification_number,
            },
            follow_redirects=True,
        )

        self.mock_twilio_client.messages.create.assert_not_called()

        self.assertIn(b"Validation Error: Message cannot be empty.", response.data)
        self.assertEqual(response.status_code, 200)

    def test_message_truncation(self):
        """Test message body is truncated to 160 characters (Tier 2 validation requirement)."""

        long_message = "A" * 200

        self.mock_twilio_client.messages.create.return_value = MagicMock(
            sid="SM_TRUNCATED_TEST"
        )

        response = self.app.post(
            "/",
            data={
                "message_body": long_message,
                "recipient_number": self.notification_number,
            },
            follow_redirects=True,
        )

        self.mock_twilio_client.messages.create.assert_called_once()
        sent_body = self.mock_twilio_client.messages.create.call_args[1]["body"]
        self.assertEqual(len(sent_body), 160)

        self.assertIn(
            b"Warning: Message truncated to 160 characters to comply with carrier limits.",
            response.data,
        )
        self.assertEqual(response.status_code, 200)

    def test_send_failure_due_to_twilio_error(self):
        """Test that API errors are caught and reported as failures."""

        self.mock_twilio_client.messages.create.side_effect = TwilioRestException(
            status=400, uri="mock_uri", msg="Authentication Failed", code=20003
        )

        response = self.app.post(
            "/",
            data={
                "message_body": "Trigger Failure",
                "recipient_number": self.notification_number,
            },
            follow_redirects=True,
        )

        self.mock_twilio_client.messages.create.assert_called_once()

        self.assertIn(
            b"API Error: Message failed to send. Twilio Error: 400", response.data
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
