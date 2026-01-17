from pydantic import BaseModel, Field, ConfigDict, field_validator
from datetime import datetime
from enum import Enum as PyEnum


##### INCIDENCIAS ####

class SeverityEnum(PyEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL= "critical"

class IncidentBase(BaseModel):
    title: str = Field(min_length=5, max_length=20)
    description: str = Field(min_length=20, max_length=250)

class IncidentCreate(IncidentBase):
    severity: SeverityEnum

class IncidentResponse(IncidentBase):
    severity: str
    created_at: datetime
    status: str
    
    model_config = ConfigDict(from_attributes=True)



#### USERS ####
class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=30)
    
    model_config = ConfigDict(from_attributes=True)

class UserValidate(UserBase):
    password: str = Field(min_length=10, max_length=30)
    
    @field_validator('password')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not any(char.isdigit() for char in v):
            raise ValueError("La contraseña debe tener al menos un número")
        if not any(char.isupper() for char in v):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula")
        special_chars = "!@#$%^&*()_+-=[]{|};:,.<>?"
        if not any(char in special_chars for char in v):
            raise ValueError("La contraseña debe contener al menos un caracter especial")
        return v

