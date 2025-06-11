from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import CreateUser
from .models import User
from . import services
from .hashing import get_hash_password


route = APIRouter()

@route.get("/token")
def login_token():
    return "Token!"


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
