from sqlalchemy import create_engine
from database.base import Base  # Ou o caminho correto
from app.models import aluno, aula, curso  # Importa os modelos para registrar as tabelas

# Substitua pelos seus dados de acesso reais
DATABASE_URL = "postgresql://postgres:micaele12@db:5432/educacao"

engine = create_engine(DATABASE_URL)

# Cria as tabelas no banco
Base.metadata.create_all(bind=engine)

print("Tabelas criadas com sucesso!")

from database.base import Base
