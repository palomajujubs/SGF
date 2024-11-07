import random
import secrets
import string

from passlib.context import CryptContext

CRIPTO = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_password: str) -> bool:
    return CRIPTO.verify(password, hashed_password)


def generate_password_hash(password: str) -> str:
    return CRIPTO.hash(password)


# GERADOR DE SENHA AUTO
def generate_password():
    letras_maiusculas = string.ascii_uppercase
    letras_minusculas = string.ascii_lowercase
    numero = string.digits

    senha = [
        secrets.choice(letras_maiusculas),
        secrets.choice(letras_minusculas),
    ]

    for _ in range(6):
        senha.append(
            secrets.choice(letras_maiusculas + letras_minusculas + numero)
        )

    random.shuffle(senha)
    senha = "".join(senha)

    return senha
