from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class AnalysisResult(BaseModel):
    filename: str
    disease: str
    confidence: float
    confidence_level: str
    area_percentage: float
    severity: str
    treatment: str | None = None
    image_url: str | None = None


class AnalyzeResponse(BaseModel):
    results: list[AnalysisResult]


class AnalysisOut(BaseModel):
    id: UUID
    user_id: UUID
    filename: str
    disease: str
    confidence: float
    confidence_level: str
    area_percentage: float
    severity: str
    treatment: str | None = None
    image_url: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


class HistoryResponse(BaseModel):
    total: int
    analyses: list[AnalysisOut]
