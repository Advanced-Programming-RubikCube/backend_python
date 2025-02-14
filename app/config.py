"""
This module contains configuration settings for the application, 
including security parameters, token expiration time, and database file location.

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

import os

# Secret key used for encoding and decoding JWT tokens
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")

# Algorithm used for JWT token encryption
ALGORITHM = "HS256"

# Access token expiration time (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Absolute path to the database file (JSON format)
DB_FILE = os.getenv("DB_FILE", "/data/db.json")

# Log the database file location for debugging purposes
print(f"Using DB_FILE: {DB_FILE}")
