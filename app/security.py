from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

from database import get_db
from models import UserTable
from schemas import UserBase, UserValidate
from config import config


SECRET_KEY = config.secret_key
ALGORITHM = config.algorithm

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def hash_password(password):
    return password_hash.hash(password=password)

def verify_password(hashed_password, password):
   return password_hash.verify(password=password, hash=hashed_password)
    

### JWT
def encode_jwt(payload: dict):
    if not  isinstance(payload, dict):
        raise ValueError("Payload must be a dictionary")
    if not SECRET_KEY:
        raise ValueError("SECRET KEY must be configurated")
    
    return jwt.encode(payload, SECRET_KEY, ALGORITHM)


def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
    
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired, login again",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials cant be validated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="System internal error"
        )
        
def validate_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials cant be validated",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload =  decode_jwt(token=token)
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
        
    except JWTError:
        raise credentials_exception
    
    result = db.execute(select(UserTable).where(UserTable.username == username))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception
        
    user = UserBase.model_validate(user)
    return user

def register(data: UserValidate, db: Session):
    try:
        result = db.execute(select(UserTable).where(UserTable.username == data.username))
        existed_username = result.scalar_one_or_none()
        if existed_username:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                 detail="Username already exists, please try another")
        
        password_hashed = hash_password(data.password)
        
        new_user = UserTable(
            username = data.username,
            password_hashed = password_hashed
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {"message": "User created",
                "data": UserBase.model_validate(new_user)}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error occurred"
    )        

    
    
def login(data: UserValidate, db: Session):
    validation_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                     detail="Incorrect username or password",
                                     headers={"WWW-Authenticate": "Bearer"})
    try:
        result = db.execute(select(UserTable).where(UserTable.username == data.username))
        verify_username = result.scalar_one_or_none()
        if not verify_username:
            raise validation_error

        password_is_correct = verify_password(password=data.password, hashed_password=verify_username.password_hashed)
        if not password_is_correct:
            raise validation_error

        payload = {
            "sub": str(verify_username.id),
            "username": verify_username.username,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)   
        }
        
        token = encode_jwt(payload)
        
        return {"access_token": token,
                "token_type": "bearer"}
        
        
    except SQLAlchemyError as e:
        raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database error occurred"
    )        
        

        
            
    
        
        
            
            