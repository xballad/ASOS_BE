
from sqlalchemy.orm import Session
from db.user import User


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


def delete_user(db: Session, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return db_user
    return None
