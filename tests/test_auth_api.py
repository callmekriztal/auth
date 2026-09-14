import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_public_info():
    """Verify public endpoint returns 200 OK without authentication."""
    response = client.get("/public/info")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome stranger! This info is public."}


def test_signup_empty_payload():
    """Verify 400 Bad Request when signup email or password is empty."""
    response = client.post("/auth/signup", json={"email": "", "password": ""})
    assert response.status_code == 400
    assert "error" in response.json()


def test_signup_missing_fields():
    """Verify 400 Bad Request when signup body is missing fields."""
    response = client.post("/auth/signup", json={})
    assert response.status_code == 400
    assert "error" in response.json()


def test_login_empty_payload():
    """Verify 400 Bad Request when login email or password is empty."""
    response = client.post("/auth/login", json={"email": "", "password": ""})
    assert response.status_code == 400
    assert "error" in response.json()


def test_login_missing_fields():
    """Verify 400 Bad Request when login body is missing fields."""
    response = client.post("/auth/login", json={})
    assert response.status_code == 400
    assert "error" in response.json()


def test_protected_profile_missing_token():
    """Verify 401 Unauthorized with 'Access token required' when header is missing."""
    response = client.get("/protected/profile")
    assert response.status_code == 401
    assert response.json() == {"error": "Access token required"}


def test_protected_profile_invalid_token():
    """Verify 401 Unauthorized with 'Invalid or expired token' when token is invalid."""
    response = client.get(
        "/protected/profile",
        headers={"Authorization": "Bearer invalid.jwt.token"},
    )
    assert response.status_code == 401
    assert response.json() == {"error": "Invalid or expired token"}


def test_protected_dashboard_missing_token():
    """Verify 401 Unauthorized with 'Access token required' on dashboard when header is missing."""
    response = client.get("/protected/dashboard")
    assert response.status_code == 401
    assert response.json() == {"error": "Access token required"}


def test_protected_dashboard_invalid_token():
    """Verify 401 Unauthorized with 'Invalid or expired token' on dashboard when token is invalid."""
    response = client.get(
        "/protected/dashboard",
        headers={"Authorization": "Bearer invalid.jwt.token"},
    )
    assert response.status_code == 401
    assert response.json() == {"error": "Invalid or expired token"}


def test_logout_missing_token():
    """Verify 401 Unauthorized when logging out without token."""
    response = client.post("/auth/logout")
    assert response.status_code == 401
    assert response.json() == {"error": "Access token required"}


@patch("app.routers.auth.supabase")
def test_login_invalid_credentials(mock_supabase):
    """Verify 401 Unauthorized with 'Invalid login credentials' on failed login."""
    mock_supabase.auth.sign_in_with_password.side_effect = Exception("Auth failed")
    response = client.post(
        "/auth/login",
        json={"email": "wrong@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json() == {"error": "Invalid login credentials"}


@patch("app.routers.auth.supabase")
def test_signup_success(mock_supabase):
    """Verify 201 Created with Supabase user object on successful signup."""
    mock_user = MagicMock()
    mock_user.model_dump.return_value = {
        "id": "user-123",
        "email": "new@example.com",
        "created_at": "2026-09-14T12:00:00Z",
    }
    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_supabase.auth.sign_up.return_value = mock_response

    response = client.post(
        "/auth/signup",
        json={"email": "new@example.com", "password": "SecretPassword123"},
    )
    assert response.status_code == 201
    assert response.json()["id"] == "user-123"
    assert response.json()["email"] == "new@example.com"


@patch("app.routers.auth.supabase")
def test_login_success(mock_supabase):
    """Verify 200 OK with access_token and refresh_token on successful login."""
    mock_session = MagicMock()
    mock_session.access_token = "valid_access_token"
    mock_session.refresh_token = "valid_refresh_token"
    mock_response = MagicMock()
    mock_response.session = mock_session
    mock_supabase.auth.sign_in_with_password.return_value = mock_response

    response = client.post(
        "/auth/login",
        json={"email": "valid@example.com", "password": "SecretPassword123"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "access_token": "valid_access_token",
        "refresh_token": "valid_refresh_token",
        "token_type": "bearer",
    }


@patch("app.dependencies.supabase")
def test_protected_profile_success(mock_supabase):
    """Verify 200 OK with profile data when valid Bearer token is provided."""
    mock_user = MagicMock()
    mock_user.id = "user-456"
    mock_user.email = "valid@example.com"
    mock_user.created_at = "2026-09-14T10:00:00Z"
    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_supabase.auth.get_user.return_value = mock_response

    response = client.get(
        "/protected/profile",
        headers={"Authorization": "Bearer valid_access_token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "user-456",
        "email": "valid@example.com",
        "created_at": "2026-09-14T10:00:00Z",
    }


@patch("app.dependencies.supabase")
def test_protected_dashboard_success(mock_supabase):
    """Verify 200 OK with dashboard data when valid Bearer token is provided."""
    mock_user = MagicMock()
    mock_user.id = "user-789"
    mock_user.email = "dash@example.com"
    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_supabase.auth.get_user.return_value = mock_response

    response = client.get(
        "/protected/dashboard",
        headers={"Authorization": "Bearer valid_access_token"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "message": "Dashboard access granted",
        "user": {"id": "user-789", "email": "dash@example.com"},
    }


@patch("app.routers.auth.supabase")
@patch("app.dependencies.supabase")
def test_logout_success(mock_dependencies_supabase, mock_auth_supabase):
    """Verify 204 No Content on successful logout."""
    mock_user = MagicMock()
    mock_user.id = "user-789"
    mock_user.email = "dash@example.com"
    mock_response = MagicMock()
    mock_response.user = mock_user
    mock_dependencies_supabase.auth.get_user.return_value = mock_response

    response = client.post(
        "/auth/logout",
        headers={"Authorization": "Bearer valid_access_token"},
    )
    assert response.status_code == 204
    assert response.content == b""
