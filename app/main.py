from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routers import auth, curso, aluno, aula
from app.database.init_db import init_db
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(auth)
app.include_router(curso)
app.include_router(aluno)
app.include_router(aula)

@app.on_event("startup")
async def startup_event():
    try:
        init_db()
        logger.info("Aplicação iniciada com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao iniciar a aplicação: {str(e)}")
        raise e 