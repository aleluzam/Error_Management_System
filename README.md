# 🚨 Error Management System

API REST para gestión de incidentes en tiempo real con notificaciones WebSocket.

---

## ✨ Características

- ✅ Endpoints para agragar incidencias
- ✅ Autenticación con JWT
- ✅ Notificaciones en tiempo real (WebSocket)
- ✅ Clasificación por severidad (low, medium, high, critical)
- ✅ Sistema de resolución de incidentes para usuarios autenticados
- ✅ Documentación interactiva (Swagger/ReDoc)

---

## 🛠️ Tecnologías

- **Backend:** FastAPI 0.104+
- **Base de Datos:** PostgreSQL
- **ORM:** SQLAlchemy 2.0+
- **Autenticación:** JWT (PyJWT)
- **WebSockets:** FastAPI WebSocket
- **Validación:** Pydantic

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/aleluzam/incident_management_system.git
cd incident-management
```

### 2. Crear entorno virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

#### Crea un archivo .env en la raiz del proyecto

```bash
# Base de Datos
DATABASE_URL=postgresql://user:password@localhost:5432/incidents_db

# Seguridad
SECRET_KEY=tu_clave_secreta_super_segura_aqui
ALGORITHM=HS256

# CORS (URLs permitidas separadas por coma)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

```

### 5. Ejecutar el servidor

```bash
fastapi dev app/main.py
```

##### El servidor estara disponible en http://localhost:8080

---

## 📡 Endpoints - Resumen Simple

## 🔐 Autenticación

#### **POST /api/v1/register**

Registra un nuevo usuario

**Pide:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Devuelve:**

```json
{
  "message": "User registered successfully",
  "data": "username"
}
```

---

### **POST /api/v1/login**

Inicia sesión y devuelve un token

**Pide:**

```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Devuelve:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 📋 **Incidentes**

### **GET /api/v1/incidents**

Lista todos los incidentes

**Devuelve:**

```json
[
  {
    "title": "Servidor caído",
    "description": "El servidor no responde",
    "severity": "critical",
    "status": "open",
    "created_at": "2026-01-17T18:30:00"
  }
]
```

---

### **POST /api/v1/incidents**

Crea un nuevo incidente

**Pide:**

```json
{
  "title": "Servidor caído",
  "description": "El servidor no responde",
  "severity": "critical"
}
```

**Devuelve:**

```json
{
\  "title": "Servidor caído",
  "description": "El servidor no responde",
  "severity": "critical",
  "status": "open",
  "created_at": "2026-01-17T18:30:00"
}
```

---

### **PATCH /api/v1/incidents/{id}/resolve**

Marca un incidente como resuelto

**Pide:**

- Header: `Authorization: Bearer {token}`
- URL: ID del incidente

**Da:**

```json
{
  "message": "Incident resolved",
  "incident status": "resolved"
}
```

---

## 🔌 **WebSocket**

### **WS /api/v1/ws**

Conexión para recibir notificaciones en tiempo real

**Pide:** Conexión WebSocket

**Devuelve (cuando se crea un incidente):**

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

**Devuelve (cuando se resuelve un incidente):**

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
