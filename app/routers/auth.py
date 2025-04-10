from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.security import create_access_token, pwd_context, get_current_user
from app.database.db import get_db
from app.models.usuario import Usuario
from sqlalchemy.orm import Session
import logging

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("/", response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@router.get("/login", response_class=HTMLResponse)
async def exibir_login(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Dados recebidos - Email: {email}")
    user = db.query(Usuario).filter(Usuario.email == email).first()
    if not user or not pwd_context.verify(senha, user.senha):
        logger.error("Credenciais inválidas")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Email ou senha inválidos"})
    access_token = create_access_token(data={"sub": user.email})
    response = RedirectResponse(url="/index.html", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    logger.info("Login bem-sucedido")
    return response

@router.get("/index.html", response_class=HTMLResponse)
async def index(request: Request, user: dict = Depends(get_current_user)):
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/logout", response_class=HTMLResponse)
async def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("access_token")
    return response

@router.get("/cadastro", response_class=HTMLResponse)
async def exibir_cadastro(request: Request, error: str = None):
    return templates.TemplateResponse("cadastro.html", {"request": request, "error": error})

@router.post("/cadastro", response_class=HTMLResponse)
async def cadastrar(
    request: Request,
    email: str = Form(...),
    senha: str = Form(...),
    confirm_senha: str = Form(...),
    db: Session = Depends(get_db)
):
    logger.info(f"Tentativa de cadastro - Email: {email}")
    
    if senha != confirm_senha:
        logger.error("Senhas não conferem")
        return templates.TemplateResponse(
            "cadastro.html", 
            {"request": request, "error": "As senhas não conferem"}
        )
    
    if db.query(Usuario).filter(Usuario.email == email).first():
        logger.error("Email já cadastrado")
        return templates.TemplateResponse(
            "cadastro.html", 
            {"request": request, "error": "Este email já está cadastrado"}
        )
    
    try:
        hashed_password = pwd_context.hash(senha)
        novo_usuario = Usuario(
            email=email,
            senha=hashed_password,
            nome=email.split('@')[0]  
        )
        
        db.add(novo_usuario)
        db.commit()
        logger.info("Cadastro realizado com sucesso")
        return templates.TemplateResponse(
            "login.html", 
            {"request": request, "success": "Cadastro realizado com sucesso! Faça login para continuar."}
        )
    except Exception as e:
        logger.error(f"Erro ao cadastrar usuário: {str(e)}")
        db.rollback()
        return templates.TemplateResponse(
            "cadastro.html", 
            {"request": request, "error": "Erro ao realizar cadastro. Tente novamente."}
        )