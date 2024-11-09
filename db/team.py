# db/team.py
from sqlalchemy import Column, Integer, String,Table,ForeignKey
from sqlalchemy.orm import relationship

from db.base import Base

# Association table for many-to-many relationship between Team and User
team_user_association = Table(
    'team_user_association', Base.metadata,
    Column('team_id', Integer, ForeignKey('teams.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    tasks = relationship("Task", back_populates="team")
    # Many-to-Many relationship with User
    users = relationship("User", secondary=team_user_association, back_populates="teams")

    def __repr__(self):
        return f"<Team(id={self.id}, name='{self.name}')>"
