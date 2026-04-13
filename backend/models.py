"""Modelos Pydantic para validación de datos."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DeudorBase(BaseModel):
    nombre: str
    rut: str
    telefono: str
    monto_deuda: float
    dias_mora: int
    email: Optional[str] = None


class DeudorResponse(DeudorBase):
    id: int
    estado: str
    script: Optional[str] = None
    audio_path: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class HistorialResponse(BaseModel):
    id: int
    deudor_id: int
    accion: str
    detalle: Optional[str] = None
    created_at: Optional[str] = None


class LlamadaResponse(BaseModel):
    id: int
    deudor_id: int
    twilio_sid: Optional[str] = None
    estado: str
    duracion: int
    contestada: bool
    created_at: Optional[str] = None


class DeudorDetalle(DeudorResponse):
    historial: list[HistorialResponse] = []
    llamadas: list[LlamadaResponse] = []


class MetricasResponse(BaseModel):
    total_deudores: int
    total_llamados: int
    tasa_contestacion: float
    monto_total_mora: float


class MensajeResponse(BaseModel):
    mensaje: str
    data: Optional[dict] = None
