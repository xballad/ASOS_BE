
from sqlalchemy.orm import Session
from db.user import User
from db.task import Task
from db.team import Team
from db.comment import Comment
from db.task_spec import TaskSpec
def create_user(db: Session, name: str, last_name: str, username: str, password: str, email: str, salt: str):
    db_user = User(name=name, last_name=last_name, username=username, password=password, email=email, salt=salt)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def update_user_name(db: Session, user_id: int, name: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.name = name
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def update_user_last_name(db: Session, user_id: int, last_name: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.last_name = last_name
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def update_user_email(db: Session, user_id: int, email: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.email = email
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def update_user_username(db: Session, user_id: int, username: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.username = username
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def update_user_password(db: Session, user_id: int, password: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.password = password
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

def update_user_salt(db: Session, user_id: int, salt: str):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.salt = salt
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None


def create_team(db: Session, name: str):
    db_team = Team(name=name)
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team


def get_teams(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Team).offset(skip).limit(limit).all()


def get_team_by_id(db: Session, team_id: int):
    return db.query(Team).filter(Team.id == team_id).first()


def update_team_name(db: Session, team_id: int, name: str):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team:
        db_team.name = name
        db.commit()
        db.refresh(db_team)
        return db_team
    return None


def delete_team(db: Session, team_id: int):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team:
        db.delete(db_team)
        db.commit()
        return db_team
    return None


def add_user_to_team(db: Session, user_id: int, team_id: int):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_team and db_user:
        db_team.users.append(db_user)
        db.commit()
        db.refresh(db_team)
        return db_team
    return None



def remove_user_from_team(db: Session, user_id: int, team_id: int):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    db_user = db.query(User).filter(User.id == user_id).first()

    if db_team and db_user:
        db_team.users.remove(db_user)
        db.commit()
        db.refresh(db_team)
        return db_team
    return None



def get_users_in_team(db: Session, team_id: int):
    db_team = db.query(Team).filter(Team.id == team_id).first()
    if db_team:
        return db_team.users
    return None


def create_task(db: Session, title: str, status_task: str, user_id: int = None, team_id: int = None):
    task = Task(title=title, status_task=status_task, user_id=user_id, team_id=team_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task_status(db: Session, task_id: int, new_status: str,skip: int = 0, limit: int = 100):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.status_task = new_status
        db.commit()
        db.refresh(db_task)
        return db_task
    return None

def get_tasks_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.user_id == user_id).offset(skip).limit(limit).all()

def get_tasks_by_team(db: Session, team_id: int, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.team_id == team_id).offset(skip).limit(limit).all()

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()

def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
    return None
def create_task_spec(db: Session, task_id: int, description: str):
    db_task_spec = TaskSpec(task_id=task_id, description=description)
    db.add(db_task_spec)
    db.commit()
    db.refresh(db_task_spec)
    return db_task_spec


def get_task_specs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TaskSpec).offset(skip).limit(limit).all()


def get_task_spec_by_id(db: Session, task_spec_id: int):
    return db.query(TaskSpec).filter(TaskSpec.id == task_spec_id).first()

def get_task_spec_by_task_id(db: Session, task_id: int):
    return db.query(TaskSpec).filter(TaskSpec.task_id == task_id).first()


def update_task_spec(db: Session, task_spec_id: int, description: str):
    db_task_spec = db.query(TaskSpec).filter(TaskSpec.id == task_spec_id).first()
    if db_task_spec:
        db_task_spec.description = description
        db.commit()
        db.refresh(db_task_spec)
        return db_task_spec
    return None


def delete_task_spec(db: Session, task_spec_id: int):
    db_task_spec = db.query(TaskSpec).filter(TaskSpec.id == task_spec_id).first()
    if db_task_spec:
        db.delete(db_task_spec)
        db.commit()
        return db_task_spec
    return None


def create_comment(db: Session, text: str, task_spec_id: int, user_username: str):
    new_comment = Comment(text=text, task_spec_id=task_spec_id, user_username=user_username)
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


def get_comments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Comment).offset(skip).limit(limit).all()


def get_comment_by_id(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()


def get_comment_by_id(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()



def update_comment_text(db: Session, comment_id: int, new_text: str):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        comment.text = new_text
        db.commit()
        db.refresh(comment)
        return comment
    return None



def delete_comment(db: Session, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if comment:
        db.delete(comment)
        db.commit()
        return comment
    return None


def get_comments_by_username(db: Session, username: str, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.user_username == username).offset(skip).limit(limit).all()

def get_teams_for_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    return user.teams  # Access the 'teams' relationship