import copy
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from app.modules.treatment.models.treatment_model import Treatment
from app.modules.treatment.repositories import treatment_repository

STEPS_BY_DISEASE: dict[str, list[str]] = {
    "ferrugem": [
        "Aplicar fungicida sistêmico (triazol ou estrobilurina)",
        "Aguardar 7 dias e monitorar as manchas",
        "Reaplicar fungicida se as manchas persistirem",
        "Verificar o surgimento de novas folhas afetadas",
        "Realizar nova análise para confirmar o controle",
    ],
    "cercospora": [
        "Aplicar fungicida à base de cobre nas folhas afetadas",
        "Melhorar a ventilação entre as plantas",
        "Evitar excesso de irrigação nas folhas",
        "Aguardar 10 dias monitorando a evolução",
        "Realizar nova análise para confirmar o controle",
    ],
    "bicho_mineiro": [
        "Aplicar inseticida sistêmico ou biológico (Bacillus thuringiensis)",
        "Realizar poda leve para reduzir o microclima favorável",
        "Aguardar 5 dias",
        "Monitorar a expansão das minas nas folhas",
        "Realizar nova análise para confirmar o controle",
    ],
}

DEFAULT_STEPS: list[str] = [
    "Consultar um agrônomo para orientações específicas",
    "Seguir o plano de manejo recomendado",
    "Monitorar a evolução da planta",
    "Realizar nova análise após o tratamento",
]


def start(db: Session, disease: str, severity: str) -> Treatment:
    descriptions = STEPS_BY_DISEASE.get(disease.lower(), DEFAULT_STEPS)
    steps = [
        {"description": d, "status": "em_andamento" if i == 0 else "pendente"}
        for i, d in enumerate(descriptions)
    ]
    treatment = treatment_repository.create_treatment(db, disease, severity, steps)
    db.commit()
    db.refresh(treatment)
    return treatment


def list_treatments(db: Session) -> list[Treatment]:
    return treatment_repository.list_treatments(db)


def get_treatment(db: Session, treatment_id: UUID) -> Treatment | None:
    return treatment_repository.get_treatment(db, treatment_id)


def complete_step(db: Session, treatment_id: UUID, index: int) -> Treatment | None:
    treatment = treatment_repository.get_treatment(db, treatment_id)
    if not treatment:
        return None

    steps: list[dict] = copy.deepcopy(treatment.steps)

    if index < 0 or index >= len(steps):
        return None

    steps[index]["status"] = "concluida"

    if index + 1 < len(steps):
        steps[index + 1]["status"] = "em_andamento"

    if all(s["status"] == "concluida" for s in steps):
        treatment.status = "concluido"

    treatment.steps = steps
    flag_modified(treatment, "steps")
    treatment_repository.save_treatment(db, treatment)
    db.commit()
    db.refresh(treatment)
    return treatment
