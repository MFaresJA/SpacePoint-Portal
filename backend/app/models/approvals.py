from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from app.db.base import Base


class Approval(Base):
    __tablename__ = "approvals"

    id = Column(Integer, primary_key=True, index=True)

    # polymorphic reference to entity
    entity_type = Column(String(50), nullable=False)  # "quiz" or "scenario"
    entity_id = Column(Integer, nullable=False)

    decision = Column(String(20), nullable=False)  # "APPROVED" or "REJECTED"
    reason = Column(String(500), nullable=True)

    approved_by_user_id = Column(
        Integer,
        ForeignKey("users.user_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    approved_by = relationship("User")
