from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.database.db import Base

class Aula(Base):
    __tablename__ = "aulas"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    data = Column(Date)
    duracao = Column(Integer)  # Em minutos
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    
    # Relacionamento com o modelo Curso
    curso = relationship("Curso", back_populates="aulas")