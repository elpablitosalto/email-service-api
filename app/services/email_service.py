from aiosmtplib import SMTP
from email.message import EmailMessage
from app.core.config import settings
from typing import List

class EmailService:
    @staticmethod
    async def send_email(from_addr: str, to_addrs: List[str], subject: str, body: str):
        message = EmailMessage()
        message["From"] = from_addr
        message["To"] = ", ".join(to_addrs)
        message["Subject"] = subject
        message.set_content(body, subtype="html")

        smtp = SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT)
        await smtp.connect()
        await smtp.send_message(message)
        await smtp.quit()

    @staticmethod
    async def fetch_incoming_emails():
        # TODO: Реализовать получение писем через IMAP
        return [] 