# Error Management System

A robust REST API for real-time incident management with WebSocket notifications. Built with FastAPI and PostgreSQL, this system enables teams to create, track, and resolve incidents with live updates.

---

## Overview

Error Management System is a backend API designed for incident tracking and management. It provides a complete solution for:

- Creating and managing incidents with severity classification
- Real-time notifications via WebSocket when incidents are added or resolved
- Secure JWT-based authentication for protected operations
- Interactive API documentation for easy integration

---

## Features

| Feature | Description |
|---------|-------------|
| **Incident Management** | Create, list, and resolve incidents with full CRUD operations |
| **Severity Classification** | Four levels: `low`, `medium`, `high`, `critical` |
| **JWT Authentication** | Secure token-based authentication for protected endpoints |
| **Real-time Notifications** | WebSocket broadcasting for instant incident updates |
| **Input Validation** | Pydantic-based validation with clear error messages |
| **Interactive Documentation** | Swagger UI and ReDoc for API exploration |

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Framework** | FastAPI 0.128.0 |
| **Database** | PostgreSQL |
| **ORM** | SQLAlchemy 2.0.45 |
| **Authentication** | JWT (python-jose) |
| **WebSockets** | FastAPI WebSocket |
| **Validation** | Pydantic 2.12.5 |
| **Password Hashing** | pwdlib |
| **Server** | Uvicorn 0.40.0 |

---

## Project Structure

```
backend/
├── app/
│   ├── main.py                  # FastAPI application entry point
│   ├── config.py                # Configuration (SECRET_KEY, ALGORITHM)
│   ├── database.py              # Database connection and session management
│   ├── models.py                # SQLAlchemy ORM models
│   ├── schemas.py               # Pydantic schemas for data validation
│   ├── endpoints.py             # API routes and endpoints
│   ├── crud.py                  # Database CRUD operations
│   ├── security.py              # Authentication functions
│   └── websockets_manager.py    # WebSocket connection manager
├── .env                         # Environment variables
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

---

## Installation

### Prerequisites

- Python 3.10+
- PostgreSQL database

### Steps

#### 1. Clone the repository

```bash
git clone https://github.com/aleluzam/incident_management_system.git
cd incident-management
```

#### 2. Create and activate virtual environment

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure environment variables

Create a `.env` file in the project root:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/incidents_db

# Security
SECRET_KEY=your_super_secure_secret_key_here
ALGORITHM=HS256

# CORS (comma-separated URLs)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

#### 5. Run the server

```bash
fastapi dev app/main.py
```

The server will be available at: **http://localhost:8080**

---

## API Endpoints

### Authentication

#### Register User

```
POST /api/v1/register
```

Register a new user in the system.

**Request Body:**

```json
{
  "username": "admin",
  "password": "Admin123!"
}
```

**Password Requirements:**
- At least 5 characters
- At least one uppercase letter
- At least one number
- At least one special character

**Response (201 Created):**

```json
{
  "message": "User registered successfully",
  "data": "admin"
}
```

---

#### Login

```
POST /api/v1/login
```

Authenticate and receive a JWT token.

**Request Body:**

```json
{
  "username": "admin",
  "password": "Admin123!"
}
```

**Response (200 OK):**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

### Incidents

#### List All Incidents

```
GET /api/v1/incidents
```

Retrieve all incidents ordered by creation date (newest first).

**Response (200 OK):**

```json
[
  {
    "id": 1,
    "title": "Server Down",
    "description": "The main server is not responding to requests",
    "severity": "critical",
    "status": "open",
    "created_at": "2026-02-24T10:30:00"
  },
  {
    "id": 2,
    "title": "Slow Response Time",
    "description": "API response time has increased significantly",
    "severity": "medium",
    "status": "resolved",
    "created_at": "2026-02-23T15:45:00"
  }
]
```

---

#### Create Incident

```
POST /api/v1/incidents
```

Create a new incident. No authentication required.

**Request Body:**

```json
{
  "title": "Database Connection Failure",
  "description": "Unable to establish connection to primary database",
  "severity": "critical"
}
```

**Severity Options:** `low`, `medium`, `high`, `critical`

**Response (201 Created):**

```json
{
  "id": 3,
  "title": "Database Connection Failure",
  "description": "Unable to establish connection to primary database",
  "severity": "critical",
  "status": "open",
  "created_at": "2026-02-24T12:00:00"
}
```

---

#### Resolve Incident

```
PATCH /api/v1/incidents/{id}/resolve
```

Mark an incident as resolved. **Authentication required.**

**Headers:**

```
Authorization: Bearer <your_jwt_token>
```

**Response (200 OK):**

```json
{
  "message": "Incident resolved",
  "incident_status": "resolved"
}
```

---

### WebSocket

#### Real-time Notifications

```
WS /api/v1/ws
```

Connect to WebSocket for real-time incident updates.

**Connection:**

```javascript
const ws = new WebSocket('ws://localhost:8080/api/v1/ws');
```

**Message Types:**

When an incident is created:

```json
{
  "type": "added",
  "data": {
    "id": 3,
    "title": "Database Connection Failure",
    "description": "Unable to establish connection to primary database",
    "severity": "critical",
    "status": "open",
    "created_at": "2026-02-24T12:00:00"
  }
}
```

When an incident is resolved:

```json
{
  "type": "resolved",
  "data": {
    "id": 3,
    "title": "Database Connection Failure",
    "description": "Unable to establish connection to primary database",
    "severity": "critical",
    "status": "resolved",
    "created_at": "2026-02-24T12:00:00"
  }
}
```

---

## Interactive Documentation

Once the server is running, access the interactive API documentation:

| Documentation | URL |
|--------------|-----|
| **Swagger UI** | http://localhost:8080/docs |
| **ReDoc** | http://localhost:8080/redoc |

---

## Error Responses

The API returns appropriate HTTP status codes:

| Status Code | Description |
|-------------|-------------|
| `200` | Success |
| `201` | Created |
| `400` | Bad Request - Invalid input |
| `401` | Unauthorized - Invalid or missing token |
| `404` | Not Found - Resource doesn't exist |
| `422` | Validation Error |

---

## License

MIT License

---

## Author

Developed by [Alejandro Luzardo](https://github.com/aleluzam)
