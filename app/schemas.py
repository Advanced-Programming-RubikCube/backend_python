"""
This module defines the Pydantic schemas used for data validation 
and serialization in the Rubik Timer API.

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

from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema for creating a new user.
    
    Attributes:
        username (str): The username of the new user.
        password (str): The password for the new user.
    """
    username: str
    password: str


class Token(BaseModel):
    """Schema for representing an authentication token.
    
    Attributes:
        access_token (str): The generated access token.
        token_type (str): The type of token (e.g., Bearer).
    """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for storing token-related user data.
    
    Attributes:
        username (Optional[str]): The username extracted from the token, if available.
    """
    username: Optional[str] = None


class SolveCreate(BaseModel):
    """Schema for creating a new solve record.
    
    Attributes:
        cube_type (str): The type of cube used in the solve (e.g., 3x3, 4x4).
        solve_time (float): The recorded time for the solve.
    """
    cube_type: str
    solve_time: float


class SolveOut(BaseModel):
    """Schema for returning solve records to the user.
    
    Attributes:
        id (int): The unique identifier for the solve record.
        cube_type (str): The type of cube used in the solve.
        solve_time (float): The recorded solve time.
        timestamp (datetime): The date and time when the solve was recorded.
        username (str): The username of the user who performed the solve.
    """
    id: int
    cube_type: str
    solve_time: float
    timestamp: datetime
    username: str

    class Config:
        """
        Configuration for Pydantic ORM mode.

        This enables compatibility with ORMs by allowing attribute access.
        """
        orm_mode = True


class Stats(BaseModel):
    """Schema for storing statistical data about solves.
    
    Attributes:
        cube_type (str): The type of cube the statistics apply to.
        average_time (float): The average solve time for the given cube type.
        best_time (float): The best recorded solve time for the given cube type.
    """
    cube_type: str
    average_time: float
    best_time: float


class UserOut(BaseModel):
    """Schema for returning user information.
    
    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        hashed_password (str): The hashed password of the user.
    """
    id: int
    username: str
    hashed_password: str

    class Config:
        """
        Configuration for Pydantic ORM mode.

        This enables compatibility with ORMs by allowing attribute access.
        """
        orm_mode = True
