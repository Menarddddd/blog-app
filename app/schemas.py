from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class LoginData(BaseModel):
    username: str
    password: str


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    password:str


class Token(BaseModel):
    access_token: str
    token_type: str


class CreatePost(BaseModel):
    caption: Optional[str] = None
    body: str


class HomeResponse(BaseModel):
    username: str
    caption: Optional[str] = None
    body: str
    date_created: datetime

    model_config = { "from_attributes": True}


class ProfileResponse(BaseModel):
    id: int
    caption: Optional[str] = None
    body: str
    date_created: datetime

    model_config = { "from_attributes": True}


class UpdatePost(BaseModel):
    caption: Optional[str] = None
    body: Optional[str] = None


