from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from app.config import supabase
from app.dependencies import get_current_user
from app.schemas import UserAuthRequest, TokenResponse, ErrorResponse

router = APIRouter()


@router.post(
    "/signup",
    status_code=status.HTTP_201_CREATED,
    responses={
        201: {"description": "User created successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input or signup failed"},
    },
)
async def signup(credentials: UserAuthRequest):
    """
    Register a new user with email and password using Supabase Auth.

    - **email**: Valid email address
    - **password**: Password string
    - **Returns**: 201 Created with Supabase User object on success.
    """
    if not credentials.email or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required"},
        )

    try:
        response = supabase.auth.sign_up(
            {
                "email": credentials.email,
                "password": credentials.password,
            }
        )
        if not response or not getattr(response, "user", None):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={"error": "Signup failed. User creation returned empty response."},
            )

        user_data = (
            response.user.model_dump()
            if hasattr(response.user, "model_dump")
            else response.user.__dict__
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=user_data)
    except HTTPException:
        raise
    except Exception as exc:
        error_msg = str(getattr(exc, "message", str(exc)))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": error_msg},
        )


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse,
    responses={
        200: {"model": TokenResponse, "description": "Login successful"},
        400: {"model": ErrorResponse, "description": "Missing required fields"},
        401: {"model": ErrorResponse, "description": "Invalid credentials"},
    },
)
async def login(credentials: UserAuthRequest):
    """
    Authenticate a user with email and password using Supabase Auth.

    - **email**: User email address
    - **password**: User password
    - **Returns**: 200 OK with access_token and refresh_token on success.
    """
    if not credentials.email or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "Email and password are required"},
        )

    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": credentials.email,
                "password": credentials.password,
            }
        )
        session = getattr(response, "session", None)
        if not session or not getattr(session, "access_token", None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid login credentials"},
            )

        return TokenResponse(
            access_token=session.access_token,
            refresh_token=session.refresh_token,
            token_type="bearer",
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid login credentials"},
        )


@router.post(
    "/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        204: {"description": "Sign out successful"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
    },
)
async def logout(user: Any = Depends(get_current_user)):
    """
    Sign out the authenticated user.

    - **Requires**: Bearer token in Authorization header.
    - **Returns**: 204 No Content on success.
    """
    try:
        supabase.auth.sign_out()
    except Exception:
        # Ignore sign_out remote errors if session token is already expired/cleared
        pass
    return Response(status_code=status.HTTP_204_NO_CONTENT)
