from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.models.aluno import Aluno as AlunoModel
from app.models.curso import Curso as CursoModel
from app.schemas.aluno import AlunoCreate
from app.services.security import get_current_user
from app.services.aluno_service import listar_alunos_com_horas
from app.database.init_db import reset_sequence

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/alunos", response_class=HTMLResponse)
def listar_alunos(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    # Buscar todos os alunos e cursos
    alunos = db.query(AlunoModel).all()
    cursos = db.query(CursoModel).all()
    
    # Buscar o relatório de alunos com horas
    relatorio = listar_alunos_com_horas(db)
    
    return templates.TemplateResponse("aluno.html", {
        "request": request, 
        "alunos": alunos, 
        "cursos": cursos, 
        "relatorio": relatorio
    })

@router.post("/alunos/adicionar", response_class=HTMLResponse)
def adicionar_aluno(
    nome: str = Form(...),
    email: str = Form(...),
    curso_id: int = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    novo_aluno = AlunoModel(nome=nome, email=email, curso_id=curso_id)
    db.add(novo_aluno)
    db.commit()
    return RedirectResponse("/alunos", status_code=303)

@router.post("/alunos/editar/{aluno_id}", response_class=HTMLResponse)
def editar_aluno(
    aluno_id: int,
    nome: str = Form(...),
    email: str = Form(...),
    curso_id: int = Form(...),
    db: Session = Depends(get_db),
    user: dict = Depends(get_current_user)
):
    aluno_data = AlunoCreate(nome=nome, email=email, curso_id=curso_id)
    aluno = db.query(AlunoModel).get(aluno_id)
    if aluno:
        aluno.nome = aluno_data.nome
        aluno.email = aluno_data.email
        aluno.curso_id = aluno_data.curso_id
        db.commit()
    return RedirectResponse("/alunos", status_code=303)

@router.get("/alunos/deletar/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    aluno = db.query(AlunoModel).get(aluno_id)
    if aluno:
        db.delete(aluno)
        db.commit()
    return RedirectResponse("/alunos", status_code=303)

@router.get("/alunos/relatorio", response_class=HTMLResponse)
def relatorio_alunos(request: Request, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    relatorio = listar_alunos_com_horas(db)
    return templates.TemplateResponse("lista_alunos.html", {"request": request, "relatorio": relatorio})

@router.get("/alunos/reset_id/{start_value}")
def reset_aluno_id(start_value: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    reset_sequence(db, "alunos", start_value)
    return RedirectResponse("/alunos", status_code=303)