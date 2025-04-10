from pydantic import BaseModel
from typing import Union

class CursoCreate(BaseModel):
    nome: str
    descricao: Union[str, None] = None

class Curso(BaseModel):
    id: int
    nome: str
    descricao: Union[str, None]

    class Config:
        from_attributes = True