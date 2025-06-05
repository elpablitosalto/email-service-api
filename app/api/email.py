from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.models.email import EmailCreate, EmailRead, Email
from app.core.database import get_db
from app.repository.email_repository import EmailRepository
from app.services.email_service import EmailService
from app.core.config import settings

router = APIRouter(prefix="/emails", tags=["emails"])

@router.post("/send", response_model=EmailRead)
async def send_email(
    email: EmailCreate,
    db: AsyncSession = Depends(get_db),
):
    from_addr = settings.SMTP_USER or "noreply@example.com"
    await EmailService.send_email(from_addr, email.to, email.subject, email.body)
    db_email = Email(
        from_addr=from_addr,
        to_addrs=email.to,
        subject=email.subject,
        body=email.body,
        direction="out",
    )
    saved = await EmailRepository.create(db, db_email)
    return saved

@router.get("", response_model=List[EmailRead])
async def get_emails(
    from_addr: Optional[str] = None,
    to_addr: Optional[str] = None,
    subject: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    direction: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    emails = await EmailRepository.get_emails(
        db, from_addr, to_addr, subject, date_from, date_to, direction
    )
    return emails

@router.get("/stats")
async def get_stats(
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db),
):
    stats = await EmailRepository.get_stats(db, date_from, date_to)
    return stats 