from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.core.configs import settings


# Tabela de users
class User(settings.DBBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
    # relacionamento com a tabela de semestres
    user_id = Column(Integer, ForeignKey("semestres.id"))
    semestres = relationship("Semestres", back_populates="user")
