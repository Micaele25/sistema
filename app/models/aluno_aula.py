from sqlalchemy import Table, Column, Integer, ForeignKey
from app.database.db import Base

aluno_aula = Table(
    "aluno_aula",
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id"), primary_key=True),
    Column("aula_id", Integer, ForeignKey("aulas.id"), primary_key=True)
)