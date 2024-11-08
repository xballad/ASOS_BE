from sqlalchemy import Column, Integer, String
from db.base import Base  # Import Base from base.py

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    email = Column(String, unique=True, index=True)

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', last_name='{self.last_name}', username='{self.username}', email='{self.email}')>"