"""
This module handles database operations for RUBIKTIMER. 
It provides functions for user management, solve tracking, 
and persistent storage using a JSON file.

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

import json
import os
from datetime import datetime
from zoneinfo import ZoneInfo
from app.config import DB_FILE


def initialize_db():
    """Creates the JSON database file if it does not exist.
    
    If the file does not exist, it initializes the database structure with 
    empty lists for users and solves, and counters for ID tracking.
    """
    if not os.path.exists(DB_FILE):
        print(f"DB file {DB_FILE} not found. Creating initial database.")
        data = {"users": [], "solves": [], "counters": {"user": 1, "solve": 1}}
        save_db_data(data)
    else:
        print(f"DB file {DB_FILE} found.")


def load_db_data():
    """Loads and returns the database data from the JSON file.
    
    Returns:
        dict: The current state of the database, including users, solves, 
              and counters for unique ID tracking.
    """
    with open(DB_FILE, "r") as f:
        return json.load(f)


def save_db_data(data):
    """Saves the given data dictionary into the JSON file and forces disk writing.
    
    Args:
        data (dict): The update database content to be written to the file.
    """
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)
        f.flush()  
        os.fsync(f.fileno())  
    new_data = load_db_data()
    print("save_db_data: contenido actualizado:", new_data)


def get_next_id(key: str):
    """Generates and returns the next unique ID for the specified key.
    
    Args:
        key (str): The key for which the next ID should be retrieved 
                   (e.g., "user" or "solve").
    
    Returns:
        int: The next available unique ID.
    """
    data = load_db_data()
    next_id = data["counters"].get(key, 1)
    data["counters"][key] = next_id + 1
    save_db_data(data)
    return next_id


def get_user_by_username(username: str):
    """Retrieves a user from the database by their username.
    
    Args:
        username (str): The username to search for.
    
    Returns:
        dict or None: The user dictionary if found, otherwise None.
    """
    data = load_db_data()
    for user in data["users"]:
        if user["username"] == username:
            return user
    return None


def create_user(username: str, hashed_password: str):
    """Creates a new user and stores their hashed password in the database.
    
    Args:
        username (str): The unique username for the new user.
        hashed_password (str): The hashed password for secure storage.
    
    Returns:
        dict: The newly created user entry.
    """
    data = load_db_data()
    user_id = get_next_id("user")  
    new_user = {"id": user_id, "username": username, "hashed_password": hashed_password}
    data["users"].append(new_user)
    save_db_data(data)
    return new_user


def add_solve(username: str, cube_type: str, solve_time: float):
    """Creates a new solve record and associates it with the specified user.
    
    Args:
        username (str): The username of the user who completed the solve.
        cube_type (str): The type of cube that was solved (e.g., "3x3", "2x2").
        solve_time (float): The time taken to complete the solve, in seconds.
    
    Returns:
        dict: The newly created solve entry.
    """
    data = load_db_data()
    solve_id = get_next_id("solve")
    new_solve = {
        "id": solve_id,
        "cube_type": cube_type,
        "solve_time": solve_time,
        "timestamp": datetime.now(ZoneInfo("America/Bogota")).isoformat(),
        "username": username,  
    }
    data["solves"].append(new_solve)
    save_db_data(data)
    return new_solve


def get_solves_for_user(username: str):
    """Retrieves all solves associated with a given username.
    
    Args:
        username (str): The username for which to fetch solve records.
    
    Returns:
        list: A list of solve records belonging to the specified user.
    """
    data = load_db_data()
    user_solves = [
        solve
        for solve in data.get("solves", [])
        if "username" in solve and solve["username"] == username
    ]
    return user_solves
