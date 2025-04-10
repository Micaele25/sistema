from pydantic import BaseModel, EmailStr
from typing import Union

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    foto: Union[str, None] = None

class Usuario(BaseModel):
    id: int
    nome: str
    email: EmailStr
    foto: Union[str, None]

    class Config:
        from_attributes = True