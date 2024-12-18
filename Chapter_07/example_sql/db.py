from sqlalchemy import create_engine, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, DeclarativeBase, mapped_column, Mapped

DATABASE_URL = "postgresql+psycopg2://postgres:567234@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


class Note(Base):
    __tablename__ = "notes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(String(250))
    done: Mapped[bool] = mapped_column(Boolean, default=False)


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()