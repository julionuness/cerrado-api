# Cerrado Scan API

API de detecção de doenças e pragas em folhas de café do cerrado usando visão computacional com YOLOv8.



## Integrantes da Equipe

| Nome |
|------|
| Julio Cesar Nunes |
| Gustavo Vitor Ferreira |
| Thales Silveira |
| Joao Vitor Mathias |



## Tema e Tarefa YOLO

**Tema:** Detecção de doenças em folhas de cafeeiro cultivado no cerrado.

**Tarefa YOLO utilizada:** `segment` — segmentação de instâncias. O modelo localiza, classifica e delimita com máscara poligonal as regiões da folha que apresentam sintomas de doenças, permitindo calcular a área afetada com precisão em pixels.



## Modelo Base

**Modelo:** `yolov8s-seg.pt` (YOLOv8 Small — Segmentação)

**Justificativa:** A tarefa de segmentação foi escolhida em relação à detecção por permitir calcular a área real afetada pela doença através da máscara gerada, em vez de usar o bounding box que superestima a área. O `yolov8s-seg` oferece o melhor equilíbrio entre velocidade de inferência e precisão para o tamanho do dataset, atingindo mAP50 de 98% nas máscaras.



## Dataset

| Atributo | Valor |
|---|---|
| Origem | Dataset público adaptado (imagens de domínio público de doenças de cafeeiro) |
| Total de imagens | 596 (391 originais + 205 oversample da classe `saudavel`) |
| Ferramenta de anotação | Label Studio |
| Split | 80% treino / 20% validação |

---

**Classes segmentadas:**

| Classe | Anotações originais |
|---|---|
| `ferrugem` | 526 |
| `bicho_mineiro` | 280 |
| `cercospora` | 250 |
| `saudavel` | 103 (309 com oversample) |

> A classe `saudavel` recebeu oversample (3×) para corrigir desequilíbrio no dataset e melhorar a confiança do modelo em folhas saudáveis.



## Resultados do Treino

**Configuração:** 40 epochs · resolução 640×640 · `yolov8s-seg.pt`

**Métricas finais (época 40):**

| Métrica | Box | Mask |
|---|---|---|
| Precision | **0.958** | **0.954** |
| Recall | **0.940** | **0.934** |
| mAP50 | **0.980** | **0.975** |
| mAP50-95 | **0.742** | **0.668** |

### Curvas de treino

![Results](docs/results.png)

### Matriz de confusão normalizada

![Confusion Matrix](docs/confusion_matrix_normalized.png)


## Arquitetura da Aplicação

![Arquitetura da Aplicação](docs/cerradoscandiagrama.png)



## Endpoints da API

### Análise de imagens

| Método | Rota | Entrada | Saída |
|---|---|---|---|
| `POST` | `/analyze` | `multipart/form-data` — campo `files` com uma ou mais imagens | Lista de resultados com doença, confiança, severidade, área afetada e URL da imagem |
| `GET` | `/analysis` | Query params `skip` (int, default 0) e `limit` (int, default 10) | Histórico paginado de análises |
| `GET` | `/analysis/{id}` | UUID da análise | Detalhes de uma análise específica |

**Exemplo — `POST /analyze`:**
```json
{
  "results": [
    {
      "filename": "folha.jpg",
      "disease": "ferrugem",
      "confidence": 0.91,
      "confidence_level": "alta",
      "area_percentage": 12.5,
      "severity": "moderada",
      "treatment": "Aplicar fungicida sistêmico (triazol ou estrobilurina).",
      "image_url": "/uploads/abc123.jpg"
    }
  ]
}
```

### Tratamentos

| Método | Rota | Entrada | Saída |
|---|---|---|---|
| `GET` | `/treatments` | — | Lista de todos os tratamentos |
| `POST` | `/treatments` | `{ "disease": "ferrugem", "severity": "moderada" }` | Tratamento criado com plano de etapas |
| `GET` | `/treatments/{id}` | UUID do tratamento | Detalhes e etapas do tratamento |
| `PATCH` | `/treatments/{id}/steps/{index}` | Índice da etapa (0-based na URL) | Tratamento atualizado com a etapa marcada como concluída |

**Exemplo — `POST /treatments`:**
```json
{
  "id": "3fa85f64-...",
  "disease": "ferrugem",
  "severity": "moderada",
  "started_at": "2026-06-14T10:00:00",
  "status": "em_andamento",
  "steps": [
    { "description": "Aplicar fungicida sistêmico (triazol ou estrobilurina)", "status": "em_andamento" },
    { "description": "Aguardar 7 dias e monitorar as manchas", "status": "pendente" },
    { "description": "Reaplicar fungicida se as manchas persistirem", "status": "pendente" },
    { "description": "Verificar o surgimento de novas folhas afetadas", "status": "pendente" },
    { "description": "Realizar nova análise para confirmar o controle", "status": "pendente" }
  ]
}
```



## Tecnologias e Bibliotecas

| Tecnologia | Versão | Uso |
|---|---|---|
| Python | 3.11 | Linguagem principal |
| FastAPI | — | Framework web / REST API |
| Uvicorn | — | Servidor ASGI |
| SQLAlchemy | — | ORM |
| Alembic | — | Migrations de banco de dados |
| PostgreSQL | — | Banco de dados relacional |
| psycopg2 | — | Driver PostgreSQL |
| Ultralytics | — | YOLOv8 — treino e inferência |
| Pillow | — | Processamento de imagens |
| Pydantic | v2 | Validação e serialização de dados |
| pydantic-settings | — | Configuração via `.env` |



## Pesos Treinados (best.pt)

O arquivo `best.pt` está disponível em `models/best.pt`.



## Como Executar

### Pré-requisitos

- Python 3.11+
- PostgreSQL rodando localmente

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

Copie o `.env.example` e preencha com suas credenciais:

```bash
cp .env.example .env
```

```env
DATABASE_URL=postgresql://postgres:SUA_SENHA@localhost:5432/cerrado
MODEL_PATH=models/best.pt
```

### 3. Criar o banco de dados

```sql
CREATE DATABASE cerrado;
```

### 4. Aplicar migrations

```bash
python -m alembic upgrade head
```

### 5. Iniciar o servidor

```bash
uvicorn app.main:app --reload
```

API disponível em `http://localhost:8000`  
Documentação interativa: `http://localhost:8000/docs`

Na primeira execução, um usuário padrão é criado automaticamente:

| Campo | Valor |
|---|---|
| Email | `cerrado@admin.com` |
| Senha | `cerrado123` |
