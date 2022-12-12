import uvicorn

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from fastapi_utils.session import FastAPISessionMaker
from fastapi_utils.tasks import repeat_every

# database_uri = f"sqlite:///./test.db?check_same_thread=False"
# sessionmaker = FastAPISessionMaker(database_uri)

from typing import List
from . import crud, models, schemas
from .database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def remove_expired_tokens(db: Session) -> None:
    """ Pretend this function deletes expired tokens from the database """
    pass


@app.on_event("startup")
@repeat_every(seconds=1)
def remove_expired_tokens_task() -> None:
    print("JAPAN WIN!!")
    # with sessionmaker.context_session() as db:
    #     remove_expired_tokens(db=db)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_event():
    pass


@app.post("/api/auth/signin")
def google_signin(access_token: str, db: Session = Depends(get_db)):
    return crud.google_signin(db, access_token)

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