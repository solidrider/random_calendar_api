import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from typing import List
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


@app.post("/api/auth/signin")
def google_signin(user: schemas.UserSignIn, db: Session = Depends(get_db)):
    return crud.google_signin(db, user)

@app.post("/api/auth/signout")
def google_signout(user: schemas.UserSignOut, db: Session = Depends(get_db)):
    return crud.google_signout(db, user)

@app.post("/api/todo", response_model=schemas.Todo)
def create_user_todo(
    todo: schemas.TodoCreate, db: Session = Depends(get_db)
):
    return crud.create_user_todo(db, todo)


@app.get("/api/todo", response_model=List[schemas.Todo])
def get_todos( user_id: int, db: Session = Depends(get_db)):
    todos = crud.get_todos(db, user_id)
    return todos

@app.delete("/api/todo")
def delete_user_todo( todo: schemas.TodoDelete, db: Session = Depends(get_db)):
    return crud.delete_user_todo(db, todo)

if __name__ == '__main__':
    uvicorn.run(app)