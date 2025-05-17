# backend/auth.py
from fastapi import HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
import jwt

# Secret key for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


# 自定义用户名和密码
def authenticate_user(username: str, password: str):
    # 设置默认的用户名和密码
    valid_username = "Leo_Ricap"
    valid_password = "011115"

    # 检查输入的用户名和密码是否匹配
    if username == valid_username and password == valid_password:
        return True  # 验证成功
    return False  # 验证失败


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
