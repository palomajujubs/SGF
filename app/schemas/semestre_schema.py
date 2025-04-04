from typing import Optional

from pydantic import BaseModel, Field, conint


class SemestreBase(BaseModel):
    ano: conint = Field(..., ge=1900, le=2030, description="ano do semestre")
    data_inicio: str
    data_fim: str


class SemestreCreate(SemestreBase):
    ano: conint = Field(..., ge=1900, le=2030, description="ano do semestre")
    data_inicio: str
    data_fim: str
    user_id: Optional[conint] = Field(
        None, description="id do usuario que criou o semestre"
    )


class Semestre(SemestreBase):
    id: conint = Field(..., description="id do semestre")
    user_id: Optional[conint] = Field(
        None, description="id do usuario que criou o semestre"
    )

    class Config:
        from_attributes = True
