from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.curso import Curso as CursoModel
from app.models.aluno import Aluno as AlunoModel
from app.schemas.curso import CursoCreate
from app.services.security import get_current_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/cursos", response_class=HTMLResponse)
def listar_cursos(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    cursos = db.query(CursoModel).all()
    return templates.TemplateResponse("curso.html", {"request": request, "cursos": cursos})

@router.post("/cursos/adicionar", response_class=HTMLResponse)
def adicionar_curso(
    nome: str = Form(...),
    descricao: str = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    novo_curso = CursoModel(nome=nome, descricao=descricao)
    db.add(novo_curso)
    db.commit()
    return RedirectResponse("/cursos", status_code=303)

@router.post("/cursos/editar/{curso_id}", response_class=HTMLResponse)
def editar_curso(
    curso_id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    curso_data = CursoCreate(nome=nome, descricao=descricao)
    curso = db.query(CursoModel).get(curso_id)
    if curso:
        curso.nome = curso_data.nome
        curso.descricao = curso_data.descricao
        db.commit()
    return RedirectResponse("/cursos", status_code=303)

@router.get("/cursos/deletar/{curso_id}")
def deletar_curso(curso_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    curso = db.query(CursoModel).get(curso_id)
    if curso:
        alunos = db.query(AlunoModel).filter(AlunoModel.curso_id == curso_id).all()
        for aluno in alunos:
            aluno.curso_id = None
        
        db.delete(curso)
        db.commit()
    return RedirectResponse("/cursos", status_code=303)