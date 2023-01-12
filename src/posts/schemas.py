from typing import Optional
from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    text: str


class PostEdit(BaseModel):
    title: Optional[str]
    text: Optional[str]


class ErrorMessage(BaseModel):
    message: str


class Like(BaseModel):
    pass
