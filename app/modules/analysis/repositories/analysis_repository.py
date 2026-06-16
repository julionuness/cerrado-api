from uuid import UUID
from sqlalchemy.orm import Session
from app.modules.analysis.models.analysis_model import Analysis


def create_analysis(
    db: Session,
    user_id: UUID,
    filename: str,
    disease: str,
    confidence: float,
    confidence_level: str,
    area_percentage: float,
    severity: str,
    treatment: str | None = None,
    image_url: str | None = None,
) -> Analysis:
    record = Analysis(
        user_id=user_id,
        filename=filename,
        disease=disease,
        confidence=confidence,
        confidence_level=confidence_level,
        area_percentage=area_percentage,
        severity=severity,
        treatment=treatment,
        image_url=image_url,
    )
    db.add(record)
    return record


def get_analysis(db: Session, analysis_id: UUID) -> Analysis | None:
    return db.query(Analysis).filter(Analysis.id == analysis_id).first()


def get_history(db: Session, skip: int = 0, limit: int = 10) -> tuple[int, list[Analysis]]:
    total = db.query(Analysis).count()
    records = (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return total, records
