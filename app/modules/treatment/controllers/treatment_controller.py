from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.treatment.schemas.treatment_schema import StartTreatmentIn, TreatmentOut
from app.modules.treatment.services import treatment_service

router = APIRouter(prefix="/treatments", tags=["treatments"])


@router.get("", response_model=list[TreatmentOut])
def list_treatments(db: Session = Depends(get_db)):
    return treatment_service.list_treatments(db)


@router.post("", response_model=TreatmentOut, status_code=201)
def start_treatment(body: StartTreatmentIn, db: Session = Depends(get_db)):
    return treatment_service.start(db, body.disease, body.severity)


@router.get("/{treatment_id}", response_model=TreatmentOut)
def get_treatment(treatment_id: UUID, db: Session = Depends(get_db)):
    t = treatment_service.get_treatment(db, treatment_id)
    if not t:
        raise HTTPException(status_code=404, detail="Treatment not found")
    return t


@router.patch("/{treatment_id}/steps/{index}", response_model=TreatmentOut)
def complete_step(treatment_id: UUID, index: int, db: Session = Depends(get_db)):
    t = treatment_service.complete_step(db, treatment_id, index)
    if not t:
        raise HTTPException(status_code=404, detail="Treatment or step not found")
    return t
