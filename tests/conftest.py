"""
Pytest configuration file.
"""
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_fogis_client():
    """Create a mock FogisApiClient."""
    mock_client = MagicMock()
    mock_client.get_cookies.return_value = {"cookie1": "value1"}
    mock_client.validate_cookies.return_value = True
    return mock_client
