# email_service.py
import asyncio
from builtins import ValueError, dict, str
from settings.config import settings
from app.utils.smtp_connection import SMTPClient
from app.utils.template_manager import TemplateManager
from app.models.user_model import User

class EmailService:
    def __init__(self, template_manager: TemplateManager):
        self.smtp_client = SMTPClient(
            server=settings.smtp_server,
            port=settings.smtp_port,
            username=settings.smtp_username,
            password=settings.smtp_password
        )
        self.template_manager = template_manager

    async def send_user_email(self, user_data: dict, email_type: str):
        subject_map = {
            'email_verification': "Verify Your Account",
            'password_reset': "Password Reset Instructions",
            'account_locked': "Account Locked Notification"
        }

        if email_type not in subject_map:
            raise ValueError("Invalid email type")

        html_content = self.template_manager.render_template(email_type, **user_data)
        self.smtp_client.send_email(subject_map[email_type], html_content, user_data['email'])

    async def send_verification_email(self, user: User, max_retries: int = 3):
        """
        Send a verification email with retry logic.

        Args:
            user (User): The user to whom the email is sent.
            max_retries (int): Maximum number of retry attempts.
        """
        verification_url = f"{settings.server_base_url}verify-email/{user.id}/{user.verification_token}"
        user_data = {
            "name": user.first_name,
            "verification_url": verification_url,
            "email": user.email
        }

        for attempt in range(1, max_retries + 1):
            try:
                await self.send_user_email(user_data, 'email_verification')
                print(f"Verification email sent successfully to {user.email}")
                break  # Exit the loop if successful
            except Exception as e:
                print(f"Attempt {attempt}: Failed to send email to {user.email} - {str(e)}")
                if attempt == max_retries:
                    raise Exception(f"Failed to send verification email after {max_retries} attempts") from e
                await asyncio.sleep(2 ** attempt)  # Exponential backoff before retrying
