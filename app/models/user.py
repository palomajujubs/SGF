from sqlalchemy import Column, Integer, String, Boolean
from app.core.configs import settingssource .venv/bin/activate


# Tabela de users
class User(settings.DBBaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, unique=False, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
