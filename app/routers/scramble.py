"""
This module defines an API route for generating random scrambles for Rubik's cubes of different sizes (2x2, 3x3, 4x4).
It ensures that consecutive moves do not occur on the same face and provides a configurable scramble length.

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

from fastapi import APIRouter, HTTPException, Query
import random

# Create the API router with a prefix and tag for categorization.
router = APIRouter(prefix="/scramble", tags=["Scramble"])

# Define the faces and modifiers for the moves.
faces = ["U", "D", "L", "R", "F", "B"]
modifiers = ["", "'", "2"]


def generate_scramble(cube_type: str, length: int = 20) -> str:
    """Generates a random scramble sequence for a given cube type and length.
    
    Args:
        cube_type (str): Type of cube (2x2, 3x3, 4x4).
        length (int): Length of the scramble sequence.
    
    Returns:
        str: A string representing the generated scramble.
    
    Raises:
        ValueError: If the cube type is unsupported.
    """
    if cube_type not in ["2x2", "3x3", "4x4"]:
        raise ValueError("Unsupported cube type")
    scramble = []
    last_face = None
    for _ in range(length):
        # Avoid consecutive moves on the same face.
        possible_faces = [f for f in faces if f != last_face]
        move_face = random.choice(possible_faces)
        move_modifier = random.choice(modifiers)
        scramble.append(move_face + move_modifier)
        last_face = move_face
    return " ".join(scramble)


@router.get("/")
def get_scramble(
    cube_type: str = Query("3x3", regex="^(2x2|3x3|4x4)$"), length: int = 20
):
    """API endpoint to retrieve a random scramble sequence for a specified cube type.
    
    Args:
        cube_type (str): The type of cube (default is 3x3). Must be one of 2x2, 3x3, or 4x4.
        length (int): The desired length of the scramble sequence (default is 20 moves).
    
    Returns:
        dict: A dictionary containing the generated scramble sequence.
    
    Raises:
        HTTPException: If an unsupported cube type is requested.
    """
    try:
        scramble = generate_scramble(cube_type, length)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"scramble": scramble}
