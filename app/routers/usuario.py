from fastapi import APIRouter, Request, Form, Depends, HTTPException, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.database.db import get_db
from app.services.security import pwd_context
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate
from sqlalchemy.orm import Session
import uuid
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/cadastro", response_class=HTMLResponse)
async def exibir_cadastro(request: Request):
    return templates.TemplateResponse("cadastro.html", {"request": request})

@router.post("/cadastro", response_class=HTMLResponse)
async def cadastrar_usuario(
    nome: str = Form(...),
    email: str = Form(...),
    senha: str = Form(...),
    foto: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    usuario_data = UsuarioCreate(nome=nome, email=email, senha=senha, foto=None)
    usuario_existente = db.query(Usuario).filter(Usuario.email == usuario_data.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    senha_hash = pwd_context.hash(usuario_data.senha)
    foto_path = None
    if foto:
        extensao = os.path.splitext(foto.filename)[1]
        nome_unico = f"{uuid.uuid4()}{extensao}"
        foto_path = f"app/static/uploads/{nome_unico}"
        with open(foto_path, "wb") as f:
            f.write(await foto.read())
    novo_usuario = Usuario(nome=nome, email=email, senha=senha_hash, foto=foto_path)
    db.add(novo_usuario)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)