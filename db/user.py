from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base  # Import Base from base.py
from db.team import team_user_association


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    last_name = Column(String, index=True)
    username = Column(String, index=True, unique=True)
    password = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    salt = Column(String, index=True)

    tasks = relationship("Task", back_populates="user")

    team_id = Column(Integer, ForeignKey("teams.id"))

    teams = relationship("Team", secondary=team_user_association, back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', last_name='{self.last_name}', username='{self.username}', email='{self.email}',salt='{self.salt}')>"