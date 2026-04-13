"""Servidor principal FastAPI - Sistema de Cobranza con Voz IA."""

import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import init_db
from routes.deudores import router as deudores_router
from routes.cobranza import router as cobranza_router
from routes.webhooks import router as webhooks_router
from routes.reportes import router as reportes_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Bot de Cobranza con Voz IA",
    description="Sistema de cobranza automatizada con generación de voz IA",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deudores_router)
app.include_router(cobranza_router)
app.include_router(webhooks_router)
app.include_router(reportes_router)


@app.get("/")
async def root():
    return {"mensaje": "Bot de Cobranza con Voz IA - API activa", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
