from fastapi import HTTPException, status


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
   
