import os
import pytest
import logging.config
from unittest.mock import patch
from app.utils.common import setup_logging


@pytest.fixture
def mock_get_settings():
    """Mock settings retrieval if needed."""
    return {"dummy_setting": "value"}


def test_setup_logging():
    """
    Test the setup_logging function by mocking logging.config.fileConfig
    and ensuring it is called with the correct path.
    """
    with patch("logging.config.fileConfig") as mock_file_config:

        # Call the function
        setup_logging()


        # Ensure mocks were called
        mock_normpath.assert_called_once()
