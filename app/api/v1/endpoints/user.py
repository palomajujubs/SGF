import os
from typing import List

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi_mail import FastMail, MessageSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.auth.auth import create_token_form_access
from app.core.configs import config
from app.core.auth.deps import get_session
from app.core.auth.security import generate_password_hash, verify_password
from app.models.user import User as UserModel
from app.schemas.user_schema import (
    EmailSchema,
    User,
    UserCreate,
    UserLoginSchema,
)

load_dotenv()
link_acesso_base = os.getenv("LINK_ACESSO")

router = APIRouter()


@router.get("/teste", response_model=str)
async def teste(session: AsyncSession = Depends(get_session)) -> str:
    return "True"


@router.post("/enviar-link-acesso", status_code=status.HTTP_202_ACCEPTED)
async def enviar_link_acesso(email_schema: EmailSchema):
    email = email_schema.email

    if not email.endswith("@fesfsus.ba.gov.br"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Apenas emails com o domínio @fesfsus.ba.gov.br são autorizados a receber o link de acesso."
            ),
        )

    # Simulando a criação do token sem armazenar o email no banco
    token = create_token_form_access(sub=email)

    # Construir o link de acesso com o token JWT
    link_acesso = f"http://{link_acesso_base}?token={token}"

    # Preparar o corpo do email
    body = (
        "Olá,<br><br>"
        "Você solicitou um link de acesso ao Sistema de Registro de Documentos. "
        "Clique no link abaixo para acessar:<br>"
        f"<a href='{link_acesso}'>Clique aqui para acessar o sistema</a>"
    )

    message = MessageSchema(
        subject="Link de Acesso ao Sistema de Registro de Documentos",
        recipients=[email],
        body=body,
        subtype="html",
    )

    # Enviar o email
    fm = FastMail(config)
    await fm.send_message(message)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Email enviado com sucesso."},
    )


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_session)
):
    # Verificar se o e-mail já existe na base de dados
    async with session.begin():
        result = await session.execute(
            select(UserModel).filter_by(email=user.email)
        )
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

    hashed_password = generate_password_hash(
        user.password
    )  # Gerar hash da senha
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int, session: AsyncSession = Depends(get_session)):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user


@router.get("/", response_model=List[User])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    session: AsyncSession = Depends(get_session),
):
    query = select(UserModel).offset(skip).limit(limit)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: int,
    user_update: UserCreate,
    session: AsyncSession = Depends(get_session),
):
    query = select(UserModel).where(UserModel.id == user_id)
    result = await session.execute(query)
    db_user = result.scalars().first()

    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db_user.username = user_update.username
    db_user.email = user_update.email

    if user_update.password:  # Verifica se a senha foi fornecida
        db_user.hashed_password = generate_password_hash(
            user_update.password
        )  # Atualizar senha com hash

    await session.commit()
    await session.refresh(db_user)
    return db_user


# Endpoint para login
@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    user_login: UserLoginSchema, session: AsyncSession = Depends(get_session)
):
    # Verificar se o usuário existe
    async with session.begin():
        result = await session.execute(
            select(UserModel).filter_by(username=user_login.username)
        )
        user = result.scalars().first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Verificar se a senha está correta
    if not verify_password(
        user_login.password, user.hashed_password
    ):  # Função para verificar senha
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Criar token JWT
    token = create_token_form_access(sub=user.username)

    return {"access_token": token, "token_type": "bearer"}
