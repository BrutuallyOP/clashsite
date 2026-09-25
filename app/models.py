from app.database import Base
from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import uuid


def _utcnow() -> datetime:
    # Naive UTC, deliberately. SQLite has no real timezone-aware datetime
    # type — it round-trips everything as naive — so storing aware
    # datetimes here just means every read comes back naive anyway and
    # later comparisons against an aware "now" blow up. Keeping both the
    # stored values and the comparison value naive-but-UTC avoids that
    # entirely. If you migrate to Postgres later, switch this back to
    # timezone-aware and use DateTime() consistently.
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _uuid_str() -> str:
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid_str)
    username: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    level: Mapped[int] = mapped_column(Integer(), nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=_utcnow)

    shared: Mapped[List["Layout"]] = relationship(back_populates="owner")
    consumer: Mapped["Tracker"] = relationship(back_populates="consumer")

class Layout(Base):
    __tablename__ = "layouts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid_str)
    th_level: Mapped[int] = mapped_column(Integer(), index=True)
    thumbnail_path: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    url: Mapped[str] = mapped_column(String(75), unique=True, nullable=False)
    uploader: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(), default=_utcnow)

    owner: Mapped["User"] = relationship(back_populates="shared")
    base: Mapped["Tracker"] = relationship(back_populates="layout")

class Tracker(Base):
    __tablename__ = "tracker"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    layout_id: Mapped[str] = mapped_column(String(36), ForeignKey("layouts.id"), index=True)
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    layout: Mapped["Layout"] = relationship(back_populates="base")
    consumers: Mapped[List["User"]] = relationship(back_populates="consumer")
