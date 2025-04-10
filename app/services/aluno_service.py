from sqlalchemy.orm import Session
from app.models.aluno import Aluno as AlunoModel
from app.models.aula import Aula as AulaModel
from app.models.curso import Curso as CursoModel
from app.models.aluno_aula import aluno_aula
from sqlalchemy.sql import func

def listar_alunos_com_horas(db: Session):
    # Buscar todos os alunos
    alunos = db.query(AlunoModel).all()
    
    # Para cada aluno, calcular o total de horas
    relatorio = []
    for aluno in alunos:
        # Buscar o curso do aluno
        curso_nome = "Sem curso"
        if aluno.curso_id is not None:
            curso = db.query(CursoModel).get(aluno.curso_id)
            if curso:
                curso_nome = curso.nome
        
        # Calcular o total de horas do aluno
        resultado = db.query(func.sum(AulaModel.duracao).label("total_horas"))\
            .join(aluno_aula, AulaModel.id == aluno_aula.c.aula_id)\
            .filter(aluno_aula.c.aluno_id == aluno.id)\
            .first()
        
        total_horas = resultado.total_horas if resultado and resultado.total_horas else 0
        
        relatorio.append({
            "aluno_id": aluno.id,
            "aluno_nome": aluno.nome,
            "aluno_email": aluno.email,
            "curso_nome": curso_nome,
            "total_horas": total_horas
        })
    
    return relatorio