from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api import api_router
from app.core.admin import init_admin
from app.core.configs import settings

app = FastAPI(title=settings.TITLE)
app.include_router(api_router, prefix=settings.API_V1_STR)

# Inicializando o painel de administração
init_admin(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD,
    )
