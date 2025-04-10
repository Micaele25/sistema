from pydantic import BaseModel
from datetime import date

class AulaCreate(BaseModel):
    titulo: str
    data: date
    duracao: int
    curso_id: int

class Aula(BaseModel):
    id: int
    titulo: str
    data: date
    duracao: int
    curso_id: int

    class Config:
        from_attributes = True