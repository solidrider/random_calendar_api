from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    # return db.query(models.User).filter(models.User.id == user_id).first()
    return db.query(models.User).first()

def create_user(db: Session, google_id: int, access_token: str):
    db_user = models.User(google_id=google_id, access_token=access_token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_google_id(db: Session, google_id: int):
    return db.query(models.User).first()
    return db.query(models.User).filter(models.User.google_id == google_id).first()

def update_acccess_token(db: Session, google_id: str ,access_token: str):
    user = get_user_by_google_id(db, google_id)
    user.access_token = access_token
    db.commit()
    return user

def get_users(db: Session):
    return db.query(models.User).all()

def get_todos(db: Session):
    return db.query(models.Todo).all()
    # return db.query(models.Todo).filter(models.Todo.user_id == user_id).all()

def create_user_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo
