from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    MODEL_PATH: str = "models/best.pt"
    DETECTION_MODEL_PATH: str = "models/best_detection.pt"
    UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"


settings = Settings()
