from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from server.database import Base


class Strategy(Base):
    __tablename__ = "Strategy"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)