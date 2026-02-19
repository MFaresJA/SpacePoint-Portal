from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(50), nullable=False, index=True)  # e.g. "intro-slides", "advanced-slides"
    title = Column(String(200), nullable=False)
    url = Column(String(500), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ContentAccessLog(Base):
    __tablename__ = "content_access_logs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)
    content_key = Column(String(50), nullable=False, index=True)

    accessed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")
