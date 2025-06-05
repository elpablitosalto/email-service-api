from sqlalchemy.future import select
from sqlalchemy import and_, or_, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime
from app.models.email import Email

class EmailRepository:
    @staticmethod
    async def create(session: AsyncSession, email: Email) -> Email:
        session.add(email)
        await session.commit()
        await session.refresh(email)
        return email

    @staticmethod
    async def get_emails(
        session: AsyncSession,
        from_addr: Optional[str] = None,
        to_addr: Optional[str] = None,
        subject: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        direction: Optional[str] = None,
    ) -> List[Email]:
        query = select(Email)
        filters = []
        if from_addr:
            filters.append(Email.from_addr == from_addr)
        if to_addr:
            filters.append(to_addr == any_(Email.to_addrs))
        if subject:
            filters.append(Email.subject.ilike(f"%{subject}%"))
        if date_from:
            filters.append(Email.created_at >= date_from)
        if date_to:
            filters.append(Email.created_at <= date_to)
        if direction:
            filters.append(Email.direction == direction)
        if filters:
            query = query.where(and_(*filters))
        result = await session.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_stats(
        session: AsyncSession,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
    ):
        query = select(
            Email.direction,
            func.count(Email.id)
        )
        filters = []
        if date_from:
            filters.append(Email.created_at >= date_from)
        if date_to:
            filters.append(Email.created_at <= date_to)
        if filters:
            query = query.where(and_(*filters))
        query = query.group_by(Email.direction)
        result = await session.execute(query)
        stats = {row[0]: row[1] for row in result.all()}
        return stats 