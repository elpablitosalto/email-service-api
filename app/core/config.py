import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "email_service")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "email_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "email_pass")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "db")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", 5432))

    SMTP_HOST: str = os.getenv("SMTP_HOST", "mailhog")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", 1025))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")

    IMAP_HOST: str = os.getenv("IMAP_HOST", "mailhog")
    IMAP_PORT: int = int(os.getenv("IMAP_PORT", 143))
    IMAP_USER: str = os.getenv("IMAP_USER", "")
    IMAP_PASSWORD: str = os.getenv("IMAP_PASSWORD", "")

    APP_ENV: str = os.getenv("APP_ENV", "development")

settings = Settings() 