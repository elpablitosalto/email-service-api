from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Text, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = "emails"
    id = Column(Integer, primary_key=True, index=True)
    from_addr = Column(String, nullable=False)
    to_addrs = Column(ARRAY(String), nullable=False)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    direction = Column(String, nullable=False)  # 'in' or 'out'
    created_at = Column(DateTime, default=datetime.utcnow)

class EmailCreate(BaseModel):
    to: List[EmailStr]
    subject: str
    body: str

class EmailRead(BaseModel):
    id: int
    from_addr: EmailStr
    to_addrs: List[EmailStr]
    subject: str
    body: str
    direction: str
    created_at: datetime

    class Config:
        orm_mode = True 