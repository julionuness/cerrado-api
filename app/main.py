import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import get_db
from app.modules.analysis.controllers.analysis_controller import router as analysis_router
from app.modules.treatment.controllers.treatment_controller import router as treatment_router
from app.modules.user.services import user_service

app = FastAPI(title="Cerrado Scan API", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(analysis_router)
app.include_router(treatment_router)


@app.on_event("startup")
def seed_default_user():
    db = next(get_db())
    try:
        user_service.get_or_create_default_user(db)
    finally:
        db.close()
