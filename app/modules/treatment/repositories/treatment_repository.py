from uuid import UUID
from sqlalchemy.orm import Session
from app.modules.treatment.models.treatment_model import Treatment


def create_treatment(db: Session, disease: str, severity: str, steps: list[dict]) -> Treatment:
    record = Treatment(disease=disease, severity=severity, steps=steps)
    db.add(record)
    db.flush()
    return record


def get_treatment(db: Session, treatment_id: UUID) -> Treatment | None:
    return db.query(Treatment).filter(Treatment.id == treatment_id).first()


def list_treatments(db: Session) -> list[Treatment]:
    return db.query(Treatment).order_by(Treatment.started_at.desc()).all()


def save_treatment(db: Session, treatment: Treatment) -> Treatment:
    db.add(treatment)
    db.flush()
    return treatment
