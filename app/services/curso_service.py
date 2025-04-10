from sqlalchemy.orm import Session
from app.models.curso import Curso

class CursoService:
    @staticmethod
    def listar_cursos(db: Session):
        return db.query(Curso).all()

    @staticmethod
    def adicionar_curso(db: Session, nome: str, horas: float):
        novo_curso = Curso(nome=nome, horas=horas)
        db.add(novo_curso)
        db.commit()
        return novo_curso

    @staticmethod
    def editar_curso(db: Session, curso_id: int, nome: str, horas: float):
        curso = db.query(Curso).get(curso_id)
        if curso:
            curso.nome = nome
            curso.horas = horas
            db.commit()
        return curso

    @staticmethod
    def deletar_curso(db: Session, curso_id: int):
        curso = db.query(Curso).get(curso_id)
        if curso:
            db.delete(curso)
            db.commit()
        return curso 