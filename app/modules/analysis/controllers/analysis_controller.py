from uuid import UUID
from typing import Annotated, List
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.modules.user.controllers.user_controller import get_default_user
from app.modules.user.models.user_model import User
from app.modules.analysis.services.analysis_service import analysis_service
from app.modules.analysis.schemas.analysis_schema import AnalyzeResponse, AnalysisOut, HistoryResponse

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    files: Annotated[List[UploadFile], File(description="One or more leaf images")],
    db: Session = Depends(get_db),
    user: User = Depends(get_default_user),
):
    results = [
        analysis_service.analyze(db, user.id, file.filename, await file.read())
        for file in files
    ]
    db.commit()
    return AnalyzeResponse(results=results)


@router.get("/analysis/{analysis_id}", response_model=AnalysisOut)
def get_analysis(analysis_id: UUID, db: Session = Depends(get_db)):
    record = analysis_service.get_analysis(db, analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return record


@router.get("/analysis", response_model=HistoryResponse)
def history(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    total, records = analysis_service.get_history(db, skip=skip, limit=limit)
    return HistoryResponse(total=total, analyses=records)
