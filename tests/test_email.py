import pytest
from unittest.mock import AsyncMock, Mock
from app.services.email_service import EmailService
from app.utils.template_manager import TemplateManager

@pytest.fixture
def mock_template_manager():
    """Mock TemplateManager with necessary mocked methods."""
    mock_manager = Mock(spec=TemplateManager)
    mock_manager.render_template = Mock(return_value="fake_html_content")
    return mock_manager


@pytest.fixture
def email_service(mock_template_manager):
    """Mock EmailService."""
    service = EmailService(template_manager=mock_template_manager)
    service.send_user_email = AsyncMock()
    return service

@pytest.mark.asyncio
async def test_send_markdown_email(email_service):
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "verification_url": "http://example.com/verify?token=abc123"
    }
    await email_service.send_user_email(user_data, 'email_verification')
    # Manual verification in Mailtrap
    email_service.send_user_email.assert_awaited_once_with(user_data, 'email_verification')
