# db/task_spec.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime


class TaskSpec(Base):
    __tablename__ = "task_specs"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    timestamp_of_change = Column(DateTime, default=datetime.utcnow)
    task_id = Column(Integer, ForeignKey("tasks.id"))

    task = relationship("Task", back_populates="task_spec", uselist=False)
    comments = relationship("Comment", back_populates="task_spec")

    def __repr__(self):
        return f"<TaskSpec(id={self.id}, task_id='{self.task_id}', description='{self.description}')>"
