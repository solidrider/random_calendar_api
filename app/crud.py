from sqlalchemy.orm import Session

from . import models, schemas
from . import config

from google.oauth2 import id_token
from google.auth.transport import requests


def create_user(db: Session, google_id: str, access_token: str):
    db_user = models.User(
        google_id=google_id,
        access_token=access_token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def google_signin(db: Session, access_token: str):
    try:
        idinfo = id_token.verify_oauth2_token(access_token, requests.Request(), config.Settings().CLIENT_ID)
        google_id = idinfo['sub']
        db_user = db.query(models.User).filter(models.User.google_id == google_id).first()
        if db_user:
            db_user.access_token = access_token
            db.commit()
            return {'message': 'トークンの更新に成功'}
        return create_user(db, google_id, access_token)
    except ValueError:
         # Invalid token
        pass

def google_signout(db: Session, request: schemas.UserSignOut):
    user = db.query(models.User).filter(models.User.google_id == request.google_id).first()
    user.access_token = ''
    db.commit()
    return {'message': 'サインアウト完了'}

def get_users(db: Session):
    return db.query(models.User).all()

def get_todos(db: Session, user_id: int):
    return db.query(models.Todo).filter(models.Todo.user_id == user_id).all()

def create_user_todo(db: Session, request: schemas.TodoCreate):
    new_todo = models.Todo(
        title = request.title,
        user_id = request.user_id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def delete_user_todo(db: Session, request: schemas.TodoDelete):
    todo = db.query(models.Todo).filter(models.Todo.id == request.id).first()
    if(todo.user_id == request.user_id):
        db.delete(todo)
        db.commit()
        return {'message': '削除に成功しました。'}
    return {'message': '削除に失敗しました。'}  
