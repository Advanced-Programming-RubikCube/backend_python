"""
This module provides authentication-related dependencies for the FastAPI application. 
It includes functions for password hashing, verification, token generation, and user 
authentication using JWT tokens.

Author: Santiago Andrés Benavides Coral <sabenavidesc@udistrital.edu.co>

This file is part of RUBIKTIMER.

RUBIKTIMER is free software: you can redistribute it and/or modify it under the 
terms of the GNU General Public License as published by the Free Software Foundation, 
either version 3 of the License, or (at your option) any later version.

RUBIKTIMER is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; 
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with RUBIKTIMER. 
If not, see <https://www.gnu.org/licenses/>.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app import config, schemas
from app.db import get_user_by_username

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies that a given plaintext password matches its hashed version.
    
    Args:
        plain_password (str): The plaintext password provided by the user.
        hashed_password (str): The hashed version of the stored password.
    
    Returns:
        bool: True if the password matches, False otherwise.
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generates a hashed version of the provided password using bcrypt.
    
    Args:
        password (str): The plaintext password to be hashed.
    
    Returns:
        str: The hashed password string.
    """
    from passlib.context import CryptContext

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Generates a new JWT access token with an optional expiration time.
    
    Args:
        data (dict): The data to be included in the token payload.
        expires_delta (timedelta, optional): The duration before the token expires. 
                                             Defaults to the configured expiration time.
    
    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        from datetime import timedelta

        expire = datetime.utcnow() + timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Retrieves the authenticated user based on the provided JWT token.
    
    Args:
        token (str): The JWT token provided by the user.
    
    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    
    Returns:
        dict: The authenticated user's information.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user
