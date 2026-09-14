# FastAPI Supabase Auth API

A production-ready authentication API built with **Python 3.10+**, **FastAPI**, and **Supabase Auth** as the identity provider.

## Overview

This project provides a clean, modular authentication backend with user registration, authentication, sign-out, public information access, and JWT Bearer token-protected endpoints.

### Key Features
- **Supabase Auth Integration**: Seamless user signup, signin, token verification, and signout.
- **Reusable Auth Dependency**: A single FastAPI `Depends(get_current_user)` function enforcing Bearer token extraction and verification.
- **Swagger UI (`/docs`) Support**: Integrated `HTTPBearer` security scheme allowing token authorization directly inside Swagger UI interactive documentation.
- **Strict HTTP Status Codes & Custom Error Formats**: Uniform JSON error responses matching API specs.

---

## Project Structure

```
app/
  main.py            # FastAPI app instance, router includes, startup log & exception handlers
  config.py          # Loads .env and initializes Supabase client
  dependencies.py    # Auth dependency (Bearer token extraction & verification)
  routers/
    auth.py          # /auth/signup, /auth/login, /auth/logout
    public.py        # /public/info
    protected.py      # /protected/profile, /protected/dashboard
  schemas.py         # Pydantic models for request & response bodies
.env.example         # Environment variables template
.gitignore          # Git ignore rules (.env, .venv, pycache)
requirements.txt     # Pinned Python package dependencies
README.md            # Project documentation & API reference
```

---

## Environment Configuration

Create a `.env` file in the root directory based on `.env.example`:

```bash
cp .env.example .env
```

Set your Supabase credentials and port configuration:

```ini
SUPABASE_URL=https://your_supabase_project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
PORT=8000
```

> **Note**: `.env` is listed in `.gitignore` to prevent committing sensitive keys to version control.

---

## Setup & Running the Server

### 1. Create a Virtual Environment & Install Dependencies

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Start the Server

Run the server using the single command:

```bash
uvicorn app.main:app --reload --port 8000
```

Upon successful startup, the server will log:
```
INFO:     Server running and connected to Supabase
```

---

## Interactive Swagger UI Documentation

Access the interactive OpenAPI documentation at:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Using Swagger UI with Protected Endpoints
1. Open `http://127.0.0.1:8000/docs` in your browser.
2. Click the **Authorize** button at the top right (or click the padlock icon next to any protected route).
3. Paste your JWT access token (obtained from `/auth/login`) into the **Value** field and click **Authorize**.
4. Test `/protected/profile` or `/protected/dashboard` via **Try it out**.

> **Swagger UI Screenshot Placeholder**:
> ![Swagger UI Screenshot](https://via.placeholder.com/800x450.png?text=Swagger+UI+Authorize+and+Protected+Endpoints)
> *(Replace with actual screenshot of your Swagger UI showing padlock authorization)*

---

## API Reference

| Endpoint | Method | Auth Required | Success Status | Error Statuses & Descriptions |
|---|---|---|---|---|
| `/auth/signup` | `POST` | No | `201 Created` | `400 Bad Request` (Missing/empty fields or Supabase error) |
| `/auth/login` | `POST` | No | `200 OK` | `400 Bad Request` (Missing fields), `401 Unauthorized` (`Invalid login credentials`) |
| `/auth/logout` | `POST` | Yes (Bearer) | `204 No Content` | `401 Unauthorized` (`Access token required` / `Invalid or expired token`) |
| `/public/info` | `GET` | No | `200 OK` | N/A |
| `/protected/profile` | `GET` | Yes (Bearer) | `200 OK` | `401 Unauthorized` (`Access token required` / `Invalid or expired token`) |
| `/protected/dashboard` | `GET` | Yes (Bearer) | `200 OK` | `401 Unauthorized` (`Access token required` / `Invalid or expired token`) |

### Example Request Bodies

#### Signup & Login (`POST /auth/signup`, `POST /auth/login`)
```json
{
  "email": "user@example.com",
  "password": "SecurePassword123!"
}
```

#### Protected Request Header (`GET /protected/profile`)
```http
Authorization: Bearer <access_token>
```
