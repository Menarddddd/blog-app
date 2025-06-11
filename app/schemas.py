from pydantic import BaseModel


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