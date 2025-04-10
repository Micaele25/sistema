from pydantic import BaseModel, EmailStr
from typing import Union

class AlunoCreate(BaseModel):
    nome: str
    email: EmailStr
    curso_id: Union[int, None] = None

class Aluno(BaseModel):
    id: int
    nome: str
    email: EmailStr
    curso_id: Union[int, None]

    class Config:
        from_attributes = True