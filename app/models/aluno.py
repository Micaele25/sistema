from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.db import Base

class Aluno(Base):
    __tablename__ = "alunos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    curso_id = Column(Integer, ForeignKey("cursos.id"))