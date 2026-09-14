from typing import Optional
from pydantic import BaseModel, Field, field_validator


class UserAuthRequest(BaseModel):
    """Request model for user signup and login."""
    email: str = Field(..., description="User email address")
    password: str = Field(..., description="User password")

    @field_validator("email", "password")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Field cannot be empty or whitespace only")
        return value.strip()


class TokenResponse(BaseModel):
    """Response model for successful authentication login."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field("bearer", description="Token type")


class UserProfileResponse(BaseModel):
    """Response model for protected user profile information."""
    id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email address")
    created_at: str = Field(..., description="Account creation ISO timestamp")


class PublicInfoResponse(BaseModel):
    """Response model for public information endpoint."""
    message: str = Field(..., description="Public message payload")


class DashboardUser(BaseModel):
    """Nested user model for dashboard payload."""
    id: str = Field(..., description="Unique user identifier")
    email: str = Field(..., description="User email address")


class DashboardResponse(BaseModel):
    """Response model for protected dashboard endpoint."""
    message: str = Field(..., description="Dashboard confirmation message")
    user: DashboardUser = Field(..., description="Authenticated user context")


class ErrorResponse(BaseModel):
    """Standardized error response model."""
    error: str = Field(..., description="Error message description")
