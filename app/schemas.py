from typing import Union

from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    title: str
    user_id: int
    class Config:
        orm_mode = True

class TodoCreate(BaseModel):
    title: str
    user_id: int

class TodoDelete(BaseModel):
    id: int
    user_id: int

class User(BaseModel):
    id: int
    access_token: str
    google_id: str
    todos: list[Todo] = []

    class Config:
        orm_mode = True

class UserSignIn(BaseModel):
    access_token: str
    google_id: str

class UserSignOut(BaseModel):
    google_id: str