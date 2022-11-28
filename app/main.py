import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/api/auth/signin", response_model=schemas.User)
def google_signin(google_id: str, access_token: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_google_id(db, google_id=google_id)
    if db_user:
        return crud.update_acccess_token(db=db, google_id=google_id, access_token=access_token)
    return crud.create_user(db=db, google_id=google_id, access_token=access_token)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


@app.post("/api/todo", response_model=schemas.Todo)
def create_todo_for_user(
    user_id: int, db: Session = Depends(get_db)
):
    return crud.create_user_todo(db=db, user_id=user_id)


@app.get("/api/todo")
def read_todos(db: Session = Depends(get_db)):
    todos = crud.get_todos(db)
    return todos

if __name__ == '__main__':
    uvicorn.run(app)