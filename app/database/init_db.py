from app.database.db import engine, Base
from app.models.curso import Curso
from app.models.aluno import Aluno
from app.models.aula import Aula
from app.models.usuario import Usuario
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reset_sequence(db, table_name, start_value=1):
    """Reset a sequence to start from a specific value."""
    try:
        sequence_name = f"{table_name}_id_seq"
        
        sql = text(f"ALTER SEQUENCE {sequence_name} RESTART WITH {start_value}")
        db.execute(sql)
        db.commit()
        logger.info(f"Sequência {sequence_name} resetada para começar de {start_value}")
    except Exception as e:
        logger.error(f"Erro ao resetar sequência: {str(e)}")
        db.rollback()

def init_db():
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Banco de dados inicializado com sucesso!")
    except Exception as e:
        logger.error(f"Erro ao inicializar o banco de dados: {str(e)}")
        raise e

if __name__ == "__main__":
    init_db() 