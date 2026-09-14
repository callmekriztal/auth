from typing import Optional, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import supabase

# Configure HTTPBearer security scheme with auto_error=False for OpenAPI docs support
security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme),
) -> Any:
    """
    Reusable FastAPI auth dependency.

    1. Extracts and validates the Authorization: Bearer <token> header.
    2. Verifies the token against Supabase via supabase.auth.get_user(token).
    3. Raises 401 HTTPException with specific JSON error body if missing/invalid.
    4. Returns verified user object on success.
    """
    if not credentials or not credentials.credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"},
        )

    token: str = credentials.credentials.strip()
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Access token required"},
        )

    try:
        response = supabase.auth.get_user(jwt=token)
        if not response or not getattr(response, "user", None):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": "Invalid or expired token"},
            )
        return response.user
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "Invalid or expired token"},
        )
