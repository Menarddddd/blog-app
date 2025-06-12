from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import CreatePost, CreateUser, HomeResponse, Token
from .models import Post, User
from . import services
from datetime import datetime, timezone
from .hashing import get_hash_password, verify_password
from .oauth import create_access_token, get_current_user


route = APIRouter()

@route.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_token(loginData: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == loginData.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not found")
    auth_pwd = verify_password(loginData.password, user.password)
    if not auth_pwd:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect")
    
    access_token = create_access_token(data={"sub": loginData.username})

    return {"access_token": access_token, "token_type": "bearer"}


@route.post("/register", status_code=status.HTTP_201_CREATED)
def create_account(registerData: CreateUser, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == registerData.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already use, please choose different one")
    
    services.check_name(registerData.first_name)
    services.check_name(registerData.last_name)
    services.check_username(registerData.username)
    result_password = services.check_password(registerData.password)

    if not result_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least a number")

    hashed_pwd = get_hash_password(registerData.password)

    new_user = User(
        first_name = registerData.first_name,
        last_name = registerData.last_name,
        username = registerData.username,
        password = hashed_pwd
    )

    db.add(new_user)
    db.commit()
    return f"User {registerData.username} has been created!"


@route.get("/home", status_code=status.HTTP_200_OK, response_model=List[HomeResponse])
def home(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    posts = db.query(Post).all()
    return [
        {
            "username": post.author.username,
            "id": post.id,
            "caption": post.caption,
            "body": post.body,
            "date_created": post.date_created
        }
        for post in posts
    ] 


@route.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(postData: CreatePost, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    post = Post(
        caption = postData.caption,
        body = postData.body,
        date_created = datetime.now(timezone.utc).replace(second=0, microsecond=0),
        user_id = current_user.id
    )
    db.add(post)    
    db.commit()
    return "Post has been created"
