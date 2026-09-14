import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.requests import Request
from app.routers import auth, public, protected

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auth_api")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Logs startup message on server launch.
    """
    logger.info("Server running and connected to Supabase")
    print("Server running and connected to Supabase")
    yield


app = FastAPI(
    title="FastAPI Supabase Auth API",
    description="Authentication API using FastAPI and Supabase Auth as the identity provider.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    """Custom HTTP exception handler to format error dicts cleanly."""
    if isinstance(exc.detail, dict):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)
    return JSONResponse(status_code=exc.status_code, content={"error": str(exc.detail)})


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Custom validation exception handler to return 400 Bad Request on invalid payload."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"error": "Email and password are required"},
    )


# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(public.router, prefix="/public", tags=["Public Info"])
app.include_router(protected.router, prefix="/protected", tags=["Protected Features"])
