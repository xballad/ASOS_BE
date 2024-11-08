from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base  # Import Base from base.py

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
def init_db():
    from db.user import User  # Import models here to ensure they're registered with Base
    Base.metadata.create_all(bind=engine)