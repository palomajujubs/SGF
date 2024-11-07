import re

from pydantic import BaseModel, Field, validator
from validate_docbr import CPF


class UserCPF(BaseModel):
    cpf: str = Field(..., min_length=11, max_length=11)

    @validator("cpf")
    def validate_cpf(cls, cpf: str) -> str:
        cpf_numeric = re.sub(r"\D", "", cpf)

        # Verify CPF length
        if len(cpf_numeric) != 11:
            raise ValueError("O CPF deve conter 11 dígitos numéricos")

        # Verify CPF validity
        cpf_validator = CPF()
        if not cpf_validator.validate(cpf_numeric):
            raise ValueError("Invalid CPF")

        return cpf_numeric
