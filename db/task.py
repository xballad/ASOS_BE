# db/task.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    datetime_of_creation = Column(DateTime, default=datetime.utcnow)
    status_task = Column(String, index=True)
    # Foreign key for User (optional)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    # Foreign key for Team (optional)
    team_id = Column(Integer, ForeignKey('teams.id'), nullable=True)

    # Relationship to User
    user = relationship("User", back_populates="tasks", foreign_keys=[user_id], uselist=False)

    # Relationship to Team
    team = relationship("Team", back_populates="tasks", foreign_keys=[team_id], uselist=False)


    task_spec = relationship("TaskSpec", back_populates="task", uselist=False)
    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', team_id='{self.team_id}')>"


