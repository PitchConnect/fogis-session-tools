import unittest
from unittest.mock import MagicMock, patch

# Mock the FogisApiClient import
with patch("fogis_session_tools.fogis_session_keeper.FogisApiClient") as mock_fogis_api_client:
    # Now import the SessionKeeper
    from fogis_session_tools.fogis_session_keeper import SessionKeeper


class TestSessionKeeper(unittest.TestCase):
    """Tests for the SessionKeeper class."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = MagicMock()
        self.mock_client.get_cookies.return_value = {"cookie1": "value1"}
        self.mock_client.validate_cookies.return_value = True
        
        # Reset the mock for each test
        mock_fogis_api_client.reset_mock()
        mock_fogis_api_client.return_value = self.mock_client

    def test_init_with_client(self):
        """Test initializing with a client."""
        keeper = SessionKeeper(client=self.mock_client)
        self.assertEqual(keeper.client, self.mock_client)

    def test_init_with_credentials(self):
        """Test initializing with credentials."""
        keeper = SessionKeeper(username="test_user", password="test_pass")
        mock_fogis_api_client.assert_called_once_with(username="test_user", password="test_pass")
        self.assertEqual(keeper.client, self.mock_client)

    def test_init_with_cookies(self):
        """Test initializing with cookies."""
        cookies = {"cookie1": "value1"}
        keeper = SessionKeeper(cookies=cookies)
        mock_fogis_api_client.assert_called_once_with(cookies=cookies)
        self.assertEqual(keeper.client, self.mock_client)

    def test_get_client(self):
        """Test getting the client."""
        keeper = SessionKeeper(client=self.mock_client)
        self.assertEqual(keeper.get_client(), self.mock_client)

    @patch("fogis_session_tools.fogis_session_keeper.threading.Thread")
    def test_start_stop(self, mock_thread):
        """Test starting and stopping the session keeper."""
        mock_thread_instance = MagicMock()
        mock_thread.return_value = mock_thread_instance

        keeper = SessionKeeper(client=self.mock_client)
        
        # Mock the validate_cookies method
        keeper.client.validate_cookies.return_value = True
        
        keeper.start()

        self.assertTrue(keeper.running)
        mock_thread.assert_called_once()
        mock_thread_instance.start.assert_called_once()

        keeper.stop()
        self.assertFalse(keeper.running)


if __name__ == "__main__":
    unittest.main()
