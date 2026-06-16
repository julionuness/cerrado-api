import io
import os
import uuid
from PIL import Image
from ultralytics import YOLO
from sqlalchemy.orm import Session
from uuid import UUID
from app.core.config import settings
from app.modules.analysis.repositories import analysis_repository
from app.modules.analysis.schemas.analysis_schema import AnalysisResult
from app.modules.analysis.models.analysis_model import Analysis

TREATMENTS: dict[str, dict[str, str]] = {
    "ferrugem": {
        "leve":     "Monitorar evolução da doença e registrar foco.",
        "moderada": "Intensificar monitoramento e avaliar necessidade de controle.",
        "grave":    "Iniciar medidas de controle e inspecionar todo o talhão.",
        "severa":   "Intervenção urgente recomendada e monitoramento intensivo.",
    },
    "cercospora": {
        "leve":     "Monitorar manchas e verificar estado nutricional.",
        "moderada": "Intensificar acompanhamento e avaliar deficiência nutricional.",
        "grave":    "Adotar medidas de controle e avaliar extensão da doença.",
        "severa":   "Necessidade de intervenção rápida e avaliação completa da área.",
    },
    "bicho_mineiro": {
        "leve":     "Monitorar surgimento de novas minas nas folhas.",
        "moderada": "Aumentar frequência das inspeções na lavoura.",
        "grave":    "Implementar medidas de controle e mapear focos.",
        "severa":   "Intervenção imediata recomendada e monitoramento contínuo.",
    },
}

_DISEASE_PT: dict[str, str] = {"not_detected": "nao_detectado"}


class AnalysisService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._model = YOLO(settings.MODEL_PATH)
        return cls._instance

    def analyze(self, db: Session, user_id: UUID, filename: str, file_bytes: bytes) -> AnalysisResult:
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

        prediction = self._run_model(image)
        disease_pt = _DISEASE_PT.get(prediction["disease"], prediction["disease"])
        area = self._calculate_area(prediction["boxes"], prediction["img_width"], prediction["img_height"])
        confidence_level = self._calculate_confidence_level(prediction["confidence"])
        severity = self._calculate_severity(prediction["disease"], area)
        treatment = TREATMENTS.get(prediction["disease"], {}).get(severity)
        image_url = self._save_image(filename, file_bytes)

        analysis_repository.create_analysis(
            db,
            user_id=user_id,
            filename=filename,
            disease=disease_pt,
            confidence=prediction["confidence"],
            confidence_level=confidence_level,
            area_percentage=area,
            severity=severity,
            treatment=treatment,
            image_url=image_url,
        )

        return AnalysisResult(
            filename=filename,
            disease=disease_pt,
            confidence=prediction["confidence"],
            confidence_level=confidence_level,
            area_percentage=area,
            severity=severity,
            treatment=treatment,
            image_url=image_url,
        )

    @staticmethod
    def _save_image(original_filename: str, file_bytes: bytes) -> str:
        upload_dir = settings.UPLOAD_DIR
        os.makedirs(upload_dir, exist_ok=True)
        ext = original_filename.rsplit(".", 1)[-1].lower() if "." in original_filename else "jpg"
        saved_name = f"{uuid.uuid4()}.{ext}"
        with open(os.path.join(upload_dir, saved_name), "wb") as f:
            f.write(file_bytes)
        return f"/uploads/{saved_name}"

    def _run_model(self, image: Image.Image) -> dict:
        results = self._model(image)[0]

        if len(results.boxes) == 0:
            return {
                "disease": "not_detected",
                "confidence": 0.0,
                "boxes": [],
                "img_width": image.width,
                "img_height": image.height,
            }

        best = max(results.boxes, key=lambda b: float(b.conf))
        best_class = int(best.cls)

        class_boxes = [
            b.xyxy[0].tolist()
            for b in results.boxes
            if int(b.cls) == best_class
        ]

        return {
            "disease": results.names[best_class],
            "confidence": round(float(best.conf), 4),
            "boxes": class_boxes,
            "img_width": image.width,
            "img_height": image.height,
        }

    @staticmethod
    def _calculate_confidence_level(confidence: float) -> str:
        if confidence >= 0.90:
            return "alta"
        elif confidence >= 0.75:
            return "boa"
        elif confidence >= 0.50:
            return "moderada"
        return "baixa"

    @staticmethod
    def _calculate_area(boxes: list, img_width: int, img_height: int) -> float:
        img_area = img_width * img_height
        if img_area == 0 or not boxes:
            return 0.0
        total = sum((x2 - x1) * (y2 - y1) for x1, y1, x2, y2 in boxes)
        return round((total / img_area) * 100, 2)

    @staticmethod
    def _calculate_severity(disease: str, area_percentage: float) -> str:
        if disease == "saudavel":
            return "saudavel"

        if disease == "not_detected":
            return "nao_detectado"

        if disease in ("ferrugem", "cercospora"):
            if area_percentage == 0:
                return "nao_detectado"
            elif area_percentage < 5:
                return "leve"
            elif area_percentage < 15:
                return "moderada"
            elif area_percentage < 30:
                return "grave"
            return "severa"

        if disease == "bicho_mineiro":
            if area_percentage == 0:
                return "nao_detectado"
            elif area_percentage < 10:
                return "leve"
            elif area_percentage < 25:
                return "moderada"
            elif area_percentage < 50:
                return "grave"
            return "severa"

        return "desconhecido"


    def get_analysis(self, db: Session, analysis_id: UUID) -> Analysis | None:
        return analysis_repository.get_analysis(db, analysis_id)

    def get_history(self, db: Session, skip: int, limit: int) -> tuple[int, list[Analysis]]:
        return analysis_repository.get_history(db, skip=skip, limit=limit)


analysis_service = AnalysisService()
