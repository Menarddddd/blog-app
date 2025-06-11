from fastapi.security import OAuth2PasswordBearer
from .config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

