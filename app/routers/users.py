"""
This module contains the Users router, which handles retrieving user data
for debugging purposes in the RUBIKTIMER application.

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

from fastapi import APIRouter
from typing import List
from app.schemas import UserOut
from app.db import load_db_data

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[UserOut])
def get_all_users():
    """Retrieves all registered users in the system.

    This method loads user data from the database and returns a list 
    containing user details such as ID, username, and hashed password.

    Args:
        None

    Returns:
        List[UserOut]: A list of all registered users in the system.
    """
    data = load_db_data()
    return data.get("users", [])
