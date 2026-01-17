from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from database import get_db
from models import IncidentsTable
from schemas import IncidentResponse
from websockets_mannager import mannager


def get_all_incidents(db: Session):
    try:
        result = db.execute(select(IncidentsTable).order_by(IncidentsTable.created_at.desc()))
        incidents = result.scalars().all()
        return [IncidentResponse.model_validate(i) for i in incidents]
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error ocurred"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error ocurred"
        )


async def post_new_incident(db: Session, new_incident):
    try:
        new_incident = new_incident.model_dump(exclude_unset=True)
        
        new_incident["severity"] = new_incident["severity"].value
        incident = IncidentsTable(**new_incident)
        
        db.add(incident)
        db.commit()
        db.refresh(incident)
        
        message = {
            "type": "added",
            "data": {
                "title": incident.title,
                "description": incident.description,
                "severity": incident.severity
            }
        }
        await mannager.broadcast(message)
        
        return IncidentResponse.model_validate(incident)
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error ocurred"
        )
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error ocurred"
        )


async def resolve_incident(db: Session, id:int):
    try:
        result = db.execute(select(IncidentsTable).where(IncidentsTable.id == id))
        incident_to_resolve = result.scalar_one_or_none()
        if not incident_to_resolve:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No incident with id {id} found"
            )
        if incident_to_resolve.status == "resolved":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Incident is already resolved"
            )
        incident_to_resolve.status = "resolved"
        db.commit()
        db.refresh(incident_to_resolve)
        
        message = {
            "type": "resolved",
            "data": {
                "title": incident_to_resolve.title,
                "description": incident_to_resolve.description,
                "severity": incident_to_resolve.severity
            }
        }
        
        await mannager.broadcast(message)
        
        return {"message": "Incident resolved",
                "incident status": incident_to_resolve.status}
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error ocurred"
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error ocurred"
        )
