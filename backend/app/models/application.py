from __future__ import annotations

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Application(Base):
    __tablename__ = "applications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    # "intern" or "instructor" (you used varchar(20) in the DB)
    track: Mapped[str] = mapped_column(String(20), nullable=False)

    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    university: Mapped[str] = mapped_column(String(255), nullable=False)
    highest_degree: Mapped[str] = mapped_column(String(50), nullable=False)

    city_of_residence: Mapped[str] = mapped_column(String(50), nullable=False)

    deliver_cities: Mapped[list] = mapped_column(JSON, nullable=False)     # list[str]
    background_areas: Mapped[list] = mapped_column(JSON, nullable=False)   # list[str]

    video1_summary: Mapped[str] = mapped_column(Text, nullable=False)
    video2_summary: Mapped[str] = mapped_column(Text, nullable=False)
    video3_summary: Mapped[str] = mapped_column(Text, nullable=False)

    space_terms_pdf_path: Mapped[str] = mapped_column(String(500), nullable=False)
    cv_pdf_path: Mapped[str] = mapped_column(String(500), nullable=False)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="SUBMITTED")
    admin_notes: Mapped[str | None] = mapped_column(String(1000), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("User")