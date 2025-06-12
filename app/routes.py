from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import CreatePost, CreateUser, HomeResponse, ProfileResponse, Token, UpdatePost
from .models import Post, User
from . import services
from datetime import datetime, timezone
from .hashing import get_hash_password, verify_password
from .oauth import create_access_token, get_current_user
from .services import create_account_service, create_post_service, delete_post_service, home_service, login_token_service, profile_service, update_post_service



route = APIRouter()

@route.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_token(loginData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return login_token_service(loginData, db)


@route.post("/register", status_code=status.HTTP_201_CREATED)
def create_account(registerData: CreateUser, db: Session = Depends(get_db)):
    return create_account_service(registerData, db)


@route.get("/home", status_code=status.HTTP_200_OK, response_model=List[HomeResponse])
def home(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return home_service(db, current_user)


@route.get("/profile", status_code=status.HTTP_200_OK, response_model=List[ProfileResponse])
def profile(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return profile_service(db, current_user)



@route.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(postData: CreatePost, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return create_post_service(postData, db, current_user)



@route.put("/update_post/{id}", status_code=status.HTTP_200_OK, response_model=ProfileResponse)
def update_post(id: int, updateData: UpdatePost, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return update_post_service(id, updateData, db, current_user)

@route.delete("/delete_post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    delete_post_service(id, db, current_user)
    return 
