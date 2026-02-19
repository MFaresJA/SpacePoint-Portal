from sqlalchemy.orm import Session

from app.models.content import ContentAccessLog, ContentItem


def get_active_items_by_key(db: Session, key: str) -> list[ContentItem]:
    return (
        db.query(ContentItem)
        .filter(ContentItem.key == key, ContentItem.is_active == True)  # noqa: E712
        .order_by(ContentItem.id.asc())
        .all()
    )


def log_access(db: Session, user_id: int, content_key: str) -> ContentAccessLog:
    row = ContentAccessLog(user_id=user_id, content_key=content_key)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
