"""
This module contains the Solves router, handling solve submissions
and retrieval for authenticated users. It allows users to log their
solve times, retrieve their solve history, and calculate basic statistics.

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
from typing import List
from app import schemas, dependencies
from app.db import add_solve, get_solves_for_user

router = APIRouter(prefix="/solves", tags=["Solves"])


@router.post("/", response_model=schemas.SolveOut)
def create_solve(
    solve: schemas.SolveCreate,
    current_user: dict = Depends(dependencies.get_current_user),
):
    """Creates a new solve record for the authenticated user.
    
    Args:
        solve (schemas.SolveCreate): The solve data including cube type and solve time.
        current_user (dict): The authenticated user information.
    
    Returns:
        schemas.SolveOut: The newly created solve entry.
    """
    new_solve = add_solve(current_user["username"], solve.cube_type, solve.solve_time)
    return new_solve


@router.get("/", response_model=List[schemas.SolveOut])
def get_solves(current_user: dict = Depends(dependencies.get_current_user)):
    """Retrieves the list of solves for the authenticated user.
    
    Args:
        current_user (dict): The authenticated user information.
    
    Returns:
        List[schemas.SolveOut]: A list of solve records.
    """
    solves = get_solves_for_user(current_user["username"])
    return solves


@router.get("/stats", response_model=List[schemas.Stats])
def get_stats(current_user: dict = Depends(dependencies.get_current_user)):
    """Calculates and retrieves solve statistics for the authenticated user.
    
    Args:
        current_user (dict): The authenticated user information.
    
    Returns:
        List[schemas.Stats]: A list containing average and best solve times per cube type.
    """
    solves = get_solves_for_user(current_user["username"])
    cube_types = ["2x2", "3x3", "4x4"]
    stats_list = []
    for cube in cube_types:
        cube_solves = [s for s in solves if s["cube_type"] == cube]
        if cube_solves:
            times = [s["solve_time"] for s in cube_solves]
            avg_time = sum(times) / len(times)
            best_time = min(times)
            stats_list.append(
                schemas.Stats(
                    cube_type=cube, average_time=avg_time, best_time=best_time
                )
            )
    return stats_list
