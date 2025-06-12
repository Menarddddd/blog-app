from datetime import datetime, timezone
from typing import List
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import UpdatePost
from .models import Post, User
from .hashing import get_hash_password, verify_password
from .oauth import create_access_token


def check_name(name):
    if len(name) < 3:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name must be at least 3 characters.")
    return 

def check_username(username):
    if len(username) < 7:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username must be at least 7 characters.")
    return 

def check_password(password):
    if len(password) < 7:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 7 characters.")
    return any(char.isdigit() for char in password)
   

def login_token_service(loginData, db: Session):
    user = db.query(User).filter(User.username == loginData.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not found")
    auth_pwd = verify_password(loginData.password, user.password)
    if not auth_pwd:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is incorrect")
    
    access_token = create_access_token(data={"sub": loginData.username})

    return {"access_token": access_token, "token_type": "bearer"}


def create_account_service(registerData, db: Session):
    user = db.query(User).filter(User.username == registerData.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already use, please choose different one")
    
    check_name(registerData.first_name)
    check_name(registerData.last_name)
    check_username(registerData.username)
    result_password = check_password(registerData.password)

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


def home_service(db, current_user):
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


def profile_service(db, current_user):
    all_post: List = []

    posts = db.query(Post).all()
    for post in posts:
        if post.user_id == current_user.id:
            all_post.append(post)

    return all_post


def create_post_service(postData, db: Session, current_user: User):
    post = Post(
        caption = postData.caption,
        body = postData.body,
        date_created = datetime.now(timezone.utc).replace(second=0, microsecond=0),
        user_id = current_user.id
    )
    db.add(post)    
    db.commit()
    return "Post has been created"


def update_post_service(id: int, updateData: UpdatePost, db: Session, current_user: User):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="That post is not yours for you to update")

    newUpdatedData = updateData.model_dump(exclude_unset=True)
    for key, value in newUpdatedData.items():
        setattr(post, key, value)   

    db.commit()
    db.refresh(post)
    return post


def delete_post_service(id: int, db: Session, current_user: User):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post is not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="That post is not yours for you to delete")

    db.delete(post)
    db.commit()
