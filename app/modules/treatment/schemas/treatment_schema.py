from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class StepOut(BaseModel):
    description: str
    status: str


class StartTreatmentIn(BaseModel):
    disease: str
    severity: str


class TreatmentOut(BaseModel):
    id: UUID
    disease: str
    severity: str
    started_at: datetime
    status: str
    steps: list[StepOut]

    model_config = {"from_attributes": True}
