"""
This module initializes the FastAPI application for the Rubik Timer API.
It sets up middleware, database initialization, and includes various routers 
for authentication, solving records, user management, and scrambles.

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

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, solves, users, scramble
from app.db import initialize_db

# Initialize FastAPI application
app = FastAPI(title="Rubik Timer API")

# Configure CORS settings
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allowed origins for frontend communication
    allow_credentials=True,
    allow_methods=["*"],    # Allow all HTTP methods
    allow_headers=["*"],    # Allow all headers
)

# Initialize the database
initialize_db()

# Include API routers
app.include_router(auth.router)     # Authentication routes
app.include_router(solves.router)   # Solve record management routes
app.include_router(users.router)    # User management routes
app.include_router(scramble.router) # Scramble generation routes


@app.get("/")
def read_root():
    """Root endpoint that returns a welcome message.
    
    Returns:
        dict: A message indicating the API is running.
    """
    return {"message": "Welcome to the Rubik Timer API"}
