# /app/routers/__init__.py
from .auth import router as auth
from .aluno import router as aluno
from .aula import router as aula
from .curso import router as curso
from .usuario import router as usuario

__all__ = ['auth', 'aluno', 'aula', 'curso', 'usuario']