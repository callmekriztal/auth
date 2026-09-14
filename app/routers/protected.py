from typing import Any
from fastapi import APIRouter, Depends, status
from app.dependencies import get_current_user
from app.schemas import UserProfileResponse, DashboardResponse, DashboardUser, ErrorResponse

router = APIRouter()


@router.get(
    "/profile",
    status_code=status.HTTP_200_OK,
    response_model=UserProfileResponse,
    responses={
        200: {"model": UserProfileResponse, "description": "User profile retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized access token missing or invalid"},
    },
)
async def get_profile(user: Any = Depends(get_current_user)):
    """
    Retrieve authenticated user profile details.

    - **Auth Required**: Bearer Token in Authorization header
    - **Returns**: 200 OK with user id, email, and created_at.
    """
    user_id = str(getattr(user, "id", ""))
    email = str(getattr(user, "email", ""))
    created_at = str(getattr(user, "created_at", ""))

    return UserProfileResponse(
        id=user_id,
        email=email,
        created_at=created_at,
    )


@router.get(
    "/dashboard",
    status_code=status.HTTP_200_OK,
    response_model=DashboardResponse,
    responses={
        200: {"model": DashboardResponse, "description": "Dashboard data retrieved successfully"},
        401: {"model": ErrorResponse, "description": "Unauthorized access token missing or invalid"},
    },
)
async def get_dashboard(user: Any = Depends(get_current_user)):
    """
    Protected dashboard endpoint demonstrating reusable auth dependency.

    - **Auth Required**: Bearer Token in Authorization header
    - **Returns**: 200 OK with confirmation message and authenticated user info.
    """
    user_id = str(getattr(user, "id", ""))
    email = str(getattr(user, "email", ""))

    return DashboardResponse(
        message="Dashboard access granted",
        user=DashboardUser(id=user_id, email=email),
    )
