from __future__ import annotations

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, func, UniqueConstraint
from sqlalchemy.orm import relationship

from app.db.base import Base


class PointsLedger(Base):
    __tablename__ = "points_ledger"
    __table_args__ = (
        UniqueConstraint("entity_type", "entity_id", "reason", name="uq_points_once_per_entity_reason"),
    )
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, index=True)

    points = Column(Integer, nullable=False)
    reason = Column(String(200), nullable=False)

    entity_type = Column(String(50), nullable=True)
    entity_id = Column(Integer, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    user = relationship("User")