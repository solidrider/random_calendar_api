from sqlalchemy.orm import Session

from . import models, schemas


def create_user(db: Session, request: schemas.UserSignIn):
    db_user = models.User(
        google_id=request.google_id,
        access_token=request.access_token
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def google_signin(db: Session, request: schemas.UserSignIn):
    db_user = db.query(models.User).filter(models.User.google_id == request.google_id).first()
    if db_user:
        user = db.query(models.User).filter(models.User.google_id == request.google_id).first()
        user.access_token = request.access_token
        db.commit()
        return {'message': 'トークンの更新に成功'}
    return create_user(db, request)

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
