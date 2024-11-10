from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from db.base import Base
from datetime import datetime


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    datetime_of_creation = Column(DateTime, default=datetime.utcnow)
    task_spec_id = Column(Integer, ForeignKey("task_specs.id"))
    user_username = Column(String)

    task_spec = relationship("TaskSpec", back_populates="comments", uselist=False)

    def __repr__(self):
        return f"<Comment(id={self.id}, task_spec_id='{self.task_spec_id}', text='{self.text}',user='{self.user_username}' )>"
