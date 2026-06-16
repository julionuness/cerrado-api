# Dependências da API — O que cada pacote faz

| Pacote | Função no sistema |
|---|---|
| `fastapi` | Framework web — cria os endpoints `/predict` e `/history` |
| `uvicorn[standard]` | Servidor que executa a aplicação FastAPI |
| `ultralytics` | Biblioteca do YOLOv8 — carrega o `best.pt` e detecta doenças nas imagens |
| `pillow` | Lê e converte as imagens recebidas antes de passar para o modelo |
| `sqlalchemy` | ORM — mapeia as tabelas do banco para classes Python sem escrever SQL |
| `psycopg2-binary` | Driver de conexão entre SQLAlchemy e PostgreSQL |
| `alembic` | Gerencia migrações do banco — cria e atualiza tabelas sem perder dados |
| `python-multipart` | Habilita o FastAPI a receber arquivos via upload (imagens do frontend) |
| `pydantic-settings` | Lê as variáveis do `.env` de forma tipada e segura |

## Como instalar
```bash
pip install -r requirements.txt
```

## Como rodar
```bash
# 1. Criar as tabelas no banco
alembic upgrade head

# 2. Iniciar o servidor
uvicorn app.main:app --reload

# 3. Acessar a documentação automática
# http://localhost:8000/docs
```
