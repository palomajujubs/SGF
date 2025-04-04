from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.configs import settings


# Tabela de semestres
class Semestre(settings.DBBaseModel):
    __tablename__ = "semestres"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    ano = Column(Integer, index=True)
    data_inicio = Column(DateTime, index=True)
    data_fim = Column(DateTime, index=True)

    # Relacionamento com a tabela de disciplinas
    disciplinas = relationship("Disciplina", back_populates="semestre")

    # Relacionamento com a tabela de user
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="semestres")
