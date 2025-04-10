from sqlalchemy import Column, Integer, String
from app.database.db import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    foto = Column(String, nullable=True)