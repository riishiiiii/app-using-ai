
from fastapi import APIRouter, HTTPException
import json
from pydantic import BaseModel

router = APIRouter()

class User(BaseModel):
    username: str
    password: str

class ResponseMessage(BaseModel):
    message: str

from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

import uuid

@router.post("/register", response_model=ResponseMessage)
async def register_user(user: User):
    user_data = user.dict()
    user_data["password"] = get_password_hash(user.password)
    user_data["user_id"] = str(uuid.uuid4())
    try:
        with open("data/users.json", "r+") as file:
            users = json.load(file)
            if user.username in users:
                raise HTTPException(status_code=400, detail="Username already exists")
            users[user.username] = user_data
            file.seek(0)
            json.dump(users, file, indent=4)
            return {"message": "User registered successfully"}
    except FileNotFoundError:
        with open("data/users.json", "w") as file:
            json.dump({user.username: user_data}, file, indent=4)
            return {"message": "User registered successfully"}
    except json.JSONDecodeError:
        with open("data/users.json", "w") as file:
            json.dump({user.username: user_data}, file, indent=4)
            return {"message": "User registered successfully"}

@router.post("/login", response_model=ResponseMessage)
async def login_user(user: User):
    try:
        with open("data/users.json", "r") as file:
            users = json.load(file)
            if user.username not in users or not verify_password(user.password, users[user.username]["password"]):
                raise HTTPException(status_code=400, detail="Invalid username or password")
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
            return {"message": "Login successful", "access_token": access_token, "token_type": "bearer"}
    except FileNotFoundError:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid username or password")

@router.get("/user/{username}", response_model=User)
async def get_user(username: str):
    try:
        with open("data/users.json", "r") as file:
            users = json.load(file)
            if username in users:
                return users[username]
            else:
                raise HTTPException(status_code=404, detail="User not found")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=404, detail="User not found")
