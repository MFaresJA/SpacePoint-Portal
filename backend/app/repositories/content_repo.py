from __future__ import annotations

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


def create_content_item(
    db: Session,
    *,
    key: str,
    title: str,
    url: str,
    is_active: bool = True,
) -> ContentItem:
    row = ContentItem(
        key=key,
        title=title,
        url=url,
        is_active=is_active,
    )
    db.add(row)
    db.commit()
    db.refresh(row)
    return row


def list_content_items(
    db: Session,
    *,
    limit: int = 50,
    offset: int = 0,
    key: str | None = None,
    is_active: bool | None = None,
):
    q = db.query(ContentItem)

    if key:
        q = q.filter(ContentItem.key == key)
    if is_active is not None:
        q = q.filter(ContentItem.is_active == is_active)

    total = q.count()
    items = (
        q.order_by(ContentItem.created_at.desc(), ContentItem.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return total, items


def get_content_item_by_id(db: Session, content_id: int) -> ContentItem | None:
    return db.query(ContentItem).filter(ContentItem.id == content_id).first()


def update_content_item(
    db: Session,
    item: ContentItem,
    *,
    key: str | None = None,
    title: str | None = None,
    url: str | None = None,
    is_active: bool | None = None,
) -> ContentItem:
    if key is not None:
        item.key = key
    if title is not None:
        item.title = title
    if url is not None:
        item.url = url
    if is_active is not None:
        item.is_active = is_active

    db.add(item)
    db.commit()
    db.refresh(item)
    return item




def list_content_access_logs(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 50,
    user_id: int | None = None,
    content_key: str | None = None,
):
    q = db.query(ContentAccessLog)

    if user_id is not None:
        q = q.filter(ContentAccessLog.user_id == user_id)

    if content_key:
        q = q.filter(ContentAccessLog.content_key == content_key)

    total = q.count()
    items = (
        q.order_by(ContentAccessLog.accessed_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, items