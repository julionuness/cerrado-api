from uuid import uuid4
from datetime import datetime
from sqlalchemy import Column, String, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base


class Treatment(Base):
    __tablename__ = "treatments"

    id         = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    disease    = Column(String, nullable=False)
    severity   = Column(String, nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    status     = Column(String, nullable=False, default="em_andamento")
    steps      = Column(JSON, nullable=False)
