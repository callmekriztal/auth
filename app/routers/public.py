from fastapi import APIRouter, status
from app.schemas import PublicInfoResponse

router = APIRouter()


@router.get(
    "/info",
    status_code=status.HTTP_200_OK,
    response_model=PublicInfoResponse,
    responses={
        200: {"model": PublicInfoResponse, "description": "Public info retrieved successfully"}
    },
)
async def public_info():
    """
    Public information endpoint.

    - **Auth Required**: None
    - **Returns**: 200 OK with public greeting message.
    """
    return PublicInfoResponse(message="Welcome stranger! This info is public.")
