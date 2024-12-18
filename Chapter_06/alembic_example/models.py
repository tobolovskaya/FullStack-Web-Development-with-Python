from datetime import datetime

from sqlalchemy import ForeignKey, Table, Column, Integer, PrimaryKeyConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


# Таблиця для зв'язку many-to-many між таблицями notes та tags
note_m2m_tag = Table(
    "note_m2m_tag",
    Base.metadata,
    Column("note_id", Integer, ForeignKey("notes.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
    PrimaryKeyConstraint("note_id", "tag_id"),
)


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    created: Mapped[datetime] = mapped_column(default=func.now())
    records: Mapped[list["Record"]] = relationship(
        cascade="all, delete", back_populates="note"
    )
    tags: Mapped[list["Tag"]] = relationship(
        secondary=note_m2m_tag, back_populates="notes"
    )


class Record(Base):
    __tablename__ = "records"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(nullable=False)
    done: Mapped[bool] = mapped_column(default=False)
    note_id: Mapped[int] = mapped_column(ForeignKey("notes.id", ondelete="CASCADE"))
    note: Mapped["Note"] = relationship(back_populates="records")


class Tag(Base):
    __tablename__ = "tags"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    notes: Mapped[list["Note"]] = relationship(
        secondary=note_m2m_tag, back_populates="tags"
    )