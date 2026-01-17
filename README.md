# Error Management System

REST API for real-time incident management with WebSocket notifications.

---

## Features

- ✅ Endpoints for adding incidents
- ✅ JWT Authentication
- ✅ Real-time notifications (WebSocket)
- ✅ Severity classification (low, medium, high, critical)
- ✅ Incident resolution system for authenticated users
- ✅ Interactive documentation (Swagger/ReDoc)

---

## Technologies

- **Backend:** FastAPI 0.104+
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy 2.0+
- **Authentication:** JWT (PyJWT)
- **WebSockets:** FastAPI WebSocket
- **Validation:** Pydantic

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/aleluzam/incident_management_system.git
cd incident-management
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

#### Create a .env file in the project root

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/incidents_db

# Security
SECRET_KEY=your_super_secure_secret_key_here
ALGORITHM=HS256

# CORS (Allowed URLs separated by comma)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

```

### 5. Run the server

```bash
fastapi dev app/main.py
```

##### The server will be available at http://localhost:8080

---

## Endpoints - Simple Summary

## Authentication

#### **POST /api/v1/register**

Register a new user

**Request:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**

```json
{
  "message": "User registered successfully",
  "data": "username"
}
```

---

### **POST /api/v1/login**

Login and returns a token

**Request:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## **Incidents**

### **GET /api/v1/incidents**

List all incidents

**Response:**

```json
[
  {
    "title": "Server down",
    "description": "The server is not responding",
    "severity": "critical",
    "status": "open",
    "created_at": "2026-01-17T18:30:00"
  }
]
```

---

### **POST /api/v1/incidents**

Create a new incident

**Request:**

```json
{
  "title": "Server down",
  "description": "The server is not responding",
  "severity": "critical"
}
```

**Response:**

```json
{
  "title": "Server down",
  "description": "The server is not responding",
  "severity": "critical",
  "status": "open",
  "created_at": "2026-01-17T18:30:00"
}
```

---

### **PATCH /api/v1/incidents/{id}/resolve**

Mark an incident as resolved

**Request:**

- Header: `Authorization: Bearer {token}`
- URL: Incident ID

**Response:**

```json
{
  "message": "Incident resolved",
  "incident status": "resolved"
}
```

---

## **WebSocket**

### **WS /api/v1/ws**

Connection to receive real-time notifications

**Request:** WebSocket Connection

**Response (when an incident is created):**

```json
{
  "type": "added",
  "data": {
    "title": "New incident",
    "description": "Incident description",
    "severity": "low"
  }
}
```

**Response (when an incident is resolved):**

```json
{
  "type": "resolved",
  "data": {
    "title": "New incident",
    "description": "Incident description",
    "severity": "low"
  }
}
```
