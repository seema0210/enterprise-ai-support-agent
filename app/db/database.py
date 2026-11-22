
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "data" / "chat_history.db"

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine( DATABASE_URL, connect_args={"check_same_thread": False} )
# create_engine():  Creates SQLAlchemy's database engine. It manages database connections when required.

SessionLocal = sessionmaker( # Creates database sessions for reading and writing records.
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)

class Base(DeclarativeBase):
    pass
