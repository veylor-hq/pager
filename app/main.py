from contextlib import asynccontextmanager

from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import config
from app.core.database import db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_beanie(
        database=db,
        document_models=[
        ],
    )

    yield


def get_application():
    _app = FastAPI(title=config.PROJECT_NAME, lifespan=lifespan)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=config.BACKEND_CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return _app


app = get_application()


@app.get("/health")
async def health():
    return {"status": "ok"}