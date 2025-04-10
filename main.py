from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from app.database.db import engine, Base

# Importações de routers (todos de app.routers)
from app.routers import auth, aluno, aula, curso, usuario
from app.services.websocket import websocket_endpoint

app = FastAPI()

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Diretório de uploads
UPLOAD_DIR = "app/static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# WebSocket
app.websocket("/ws")(websocket_endpoint)

# Inclusão das rotas
app.include_router(auth)
app.include_router(usuario)
app.include_router(aluno)
app.include_router(curso)
app.include_router(aula)

# Criação das tabelas no banco ao iniciar
@app.on_event("startup")
async def startup():
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")

@app.get("/")
async def root():
    return {"message": "Bem-vindo ao sistema Edutec!"}