from sqlalchemy.orm import Session
from app.models.role import Role

DEFAULT_ROLES = ["admin", "instructor", "ambassador", "intern"]

def seed_roles(db: Session) -> None:
    existing = {r.name for r in db.query(Role).all()}
    for name in DEFAULT_ROLES:
        if name not in existing:
            db.add(Role(name=name))
    db.commit()
