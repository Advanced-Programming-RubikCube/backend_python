"""
This module contains authentication routes for user signup and login.
It handles user registration, password hashing, authentication, and token generation.

Author: Santiago Andrés Benavides Coral <sabenavidesc@udistrital.edu.co>

This file is part of RUBIKTIMER.

RUBIKTIMER is free software: you can redistribute it and/or 
modify it under the terms of the GNU General Public License as 
published by the Free Software Foundation, either version 3 of 
the License, or (at your option) any later version.

RUBIKTIMER is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU 
General Public License for more details.

You should have received a copy of the GNU General Public License 
along with RUBIKTIMER. If not, see <https://www.gnu.org/licenses/>.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, config, dependencies
from app.db import get_user_by_username, create_user

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=schemas.Token)
def signup(user_create: schemas.UserCreate):
    """Registers a new user by checking for existing username,
    hashing the password, storing user data, and returning an access token.

    Args:
        user_create (schemas.UserCreate): User registration data including username and password.
    
    Returns:
        dict: Access token and token type.
    """
    existing_user = get_user_by_username(user_create.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = dependencies.get_password_hash(user_create.password)
    new_user = create_user(user_create.username, hashed_password)
    access_token = dependencies.create_access_token(
        data={"sub": new_user["username"]},
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Authenticates an existing user by verifying credentials and returning an access token.
    
    Args:
        form_data (OAuth2PasswordRequestForm): User login credentials (username and password).
    
    Returns:
        dict: Access token and token type if authentication is successful.
    """
    user = get_user_by_username(form_data.username)
    if not user or not dependencies.verify_password(
        form_data.password, user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = dependencies.create_access_token(
        data={"sub": user["username"]},
        expires_delta=timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
