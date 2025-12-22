"""資料庫連線與 ORM 服務"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

# 資料庫連線字串（可根據實際需求修改）
DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """取得資料庫連線"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
