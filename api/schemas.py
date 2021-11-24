from typing import Optional

from pydantic import BaseModel


class Article(BaseModel):
    title: str
    description: str


class ArticleResponseDTO(Article):
    id: int


class User(BaseModel):
    username: str
    password: str


class UserResponseDTO(BaseModel):
    id: int
    username: str


class LoginDetails(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    username: Optional[str] = None
