from typing import Union

from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    user_id: int
    title: str
    class Config:
        orm_mode = True

class TodoCreate(Todo):
    pass

class User(BaseModel):
    id: int
    access_token: str
    google_id: str
    # todos: list[Todo] = []

    class Config:
        orm_mode = True
