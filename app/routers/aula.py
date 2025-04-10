from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.aula import Aula as AulaModel
from app.models.curso import Curso as CursoModel
from app.models.aluno import Aluno as AlunoModel
from app.models.aluno_aula import aluno_aula
from app.schemas.aula import AulaCreate
from app.services.security import get_current_user
from app.services.websocket import notify_users
from datetime import datetime

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/aulas", response_class=HTMLResponse)
def listar_aulas(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    aulas = db.query(AulaModel).all()
    cursos = db.query(CursoModel).all()
    alunos = db.query(AlunoModel).all()
    
    for aula in aulas:
        aula.alunos = []
        for aluno in alunos:
            resultado = db.execute(
                aluno_aula.select().where(
                    aluno_aula.c.aula_id == aula.id,
                    aluno_aula.c.aluno_id == aluno.id
                )
            ).first()
            if resultado:
                aula.alunos.append(aluno)
    
    return templates.TemplateResponse("aula.html", {
        "request": request, 
        "aulas": aulas, 
        "cursos": cursos,
        "alunos": alunos
    })

@router.post("/aulas/adicionar", response_class=HTMLResponse)
async def adicionar_aula(
    titulo: str = Form(...),
    data: str = Form(...),
    duracao: int = Form(...),
    curso_id: int = Form(...),
    aluno_ids: list = Form([]),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y")
        data_formatada = data_obj.strftime("%Y-%m-%d")
    except ValueError:
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        data_formatada = data

    aula_data = AulaCreate(
        titulo=titulo,
        data=datetime.strptime(data_formatada, "%Y-%m-%d").date(),
        duracao=duracao,
        curso_id=curso_id
    )
    nova_aula = AulaModel(**aula_data.dict())
    db.add(nova_aula)
    db.commit()
    
    if aluno_ids:
        for aluno_id in aluno_ids:
            db.execute(
                aluno_aula.insert().values(
                    aluno_id=int(aluno_id),
                    aula_id=nova_aula.id
                )
            )
        db.commit()
    
    await notify_users(db)
    return RedirectResponse("/aulas", status_code=303)

@router.post("/aulas/editar/{aula_id}", response_class=HTMLResponse)
async def editar_aula(
    aula_id: int,
    titulo: str = Form(...),
    data: str = Form(...),
    duracao: int = Form(...),
    curso_id: int = Form(...),
    aluno_ids: list = Form([]),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    try:
        data_obj = datetime.strptime(data, "%d/%m/%Y")
        data_formatada = data_obj.strftime("%Y-%m-%d")
    except ValueError:
        data_obj = datetime.strptime(data, "%Y-%m-%d")
        data_formatada = data

    aula_data = AulaCreate(
        titulo=titulo,
        data=datetime.strptime(data_formatada, "%Y-%m-%d").date(),
        duracao=duracao,
        curso_id=curso_id
    )
    aula = db.query(AulaModel).get(aula_id)
    if aula:
        aula.titulo = aula_data.titulo
        aula.data = aula_data.data
        aula.duracao = aula_data.duracao
        aula.curso_id = aula_data.curso_id
        
        db.execute(
            aluno_aula.delete().where(aluno_aula.c.aula_id == aula_id)
        )
        
        if aluno_ids:
            for aluno_id in aluno_ids:
                db.execute(
                    aluno_aula.insert().values(
                        aluno_id=int(aluno_id),
                        aula_id=aula_id
                    )
                )
        
        db.commit()
        await notify_users(db)
    return RedirectResponse("/aulas", status_code=303)

@router.get("/aulas/deletar/{aula_id}")
async def deletar_aula(aula_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    aula = db.query(AulaModel).get(aula_id)
    if aula:
        db.execute(
            aluno_aula.delete().where(aluno_aula.c.aula_id == aula_id)
        )
        db.delete(aula)
        db.commit()
        await notify_users(db)
    return RedirectResponse("/aulas", status_code=303)