import unittest
from unittest.mock import patch, MagicMock
import os
import sys

MOCK_ENV = {
    'TWILIO_ACCOUNT_SID': 'FAKE_SID',
    'TWILIO_AUTH_TOKEN': 'FAKE_TOKEN',
    'TWILIO_FROM_NUMBER': '+15005550006',
    'NOTIFICATION_PHONE_NUMBER': '+16065948708', 
    'FLASK_SECRET_KEY': 'TEST_SECRET'
}

FIXED_MESSAGE = "Hello from Samuel Stidham CLI/Web App - Tier 1 Complete!"

with patch.dict('os.environ', MOCK_ENV):
    from src.tier1.app import app, TWILIO_CLIENT


class TwilioTest(unittest.TestCase):
    """Tests the / route logic and mocked Twilio interaction for Tier 1."""

    def setUp(self):
        self.client_patcher = patch('src.tier1.app.TWILIO_CLIENT')
        self.mock_twilio_client = self.client_patcher.start()
        
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        self.mock_twilio_client.messages.create.reset_mock()
        self.notification_number = MOCK_ENV['NOTIFICATION_PHONE_NUMBER']
        
    def tearDown(self):
        self.client_patcher.stop()

    def test_send_success_sends_fixed_message(self):
        """Test successful message send confirms the required fixed message was sent."""
        
        self.mock_twilio_client.messages.create.return_value = MagicMock(sid='SM_TIER1_SUCCESS')

        response = self.app.post('/', data={
            'message_body': 'Any message content here is ignored by Tier 1 logic.',
            'recipient_number': self.notification_number
        }, follow_redirects=True)

        self.mock_twilio_client.messages.create.assert_called_once()
        sent_body = self.mock_twilio_client.messages.create.call_args[1]['body']
        self.assertEqual(sent_body, FIXED_MESSAGE)
        
        self.assertIn(b'Success! Message sent', response.data)
        self.assertIn(b'SM_TIER1_SUCCESS', response.data)
        self.assertEqual(response.status_code, 200)

    def test_send_failure_due_to_twilio_error(self):
        """Test that API errors are caught and reported as failures."""
        
        self.mock_twilio_client.messages.create.side_effect = Exception("Mock Authentication Failed")
        
        response = self.app.post('/', data={
            'message_body': 'Ignored message',
            'recipient_number': self.notification_number
        }, follow_redirects=True)
        
        self.mock_twilio_client.messages.create.assert_called_once()
        
        self.assertIn(b'API Error: Message failed to send.', response.data)
        self.assertIn(b'Mock Authentication Failed', response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
