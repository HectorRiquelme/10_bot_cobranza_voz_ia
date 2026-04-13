"""Rutas para gestión de deudores."""

import csv
import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from database import get_db
from models import DeudorResponse, DeudorDetalle, HistorialResponse, LlamadaResponse

router = APIRouter(prefix="/api/deudores", tags=["Deudores"])


@router.post("/upload")
async def upload_csv(archivo: UploadFile = File(...)):
    """Carga un CSV de deudores y los guarda en la base de datos."""
    if not archivo.filename or not archivo.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser CSV")

    contenido = await archivo.read()
    texto = contenido.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(texto))

    campos_requeridos = {"nombre", "rut", "telefono", "monto_deuda", "dias_mora"}
    if not campos_requeridos.issubset(set(reader.fieldnames or [])):
        raise HTTPException(
            status_code=400,
            detail=f"El CSV debe contener las columnas: {', '.join(campos_requeridos)}"
        )

    db = await get_db()
    insertados = 0
    try:
        for row in reader:
            await db.execute(
                """INSERT INTO deudores (nombre, rut, telefono, monto_deuda, dias_mora, email)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (
                    row["nombre"].strip(),
                    row["rut"].strip(),
                    row["telefono"].strip(),
                    float(row["monto_deuda"]),
                    int(row["dias_mora"]),
                    row.get("email", "").strip() or None,
                ),
            )
            insertados += 1
        await db.commit()
    finally:
        await db.close()

    return {"mensaje": f"Se cargaron {insertados} deudores exitosamente", "total": insertados}


@router.get("", response_model=list[DeudorResponse])
async def listar_deudores():
    """Lista todos los deudores con su estado de cobranza."""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM deudores ORDER BY dias_mora DESC"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()


@router.get("/{deudor_id}", response_model=DeudorDetalle)
async def detalle_deudor(deudor_id: int):
    """Detalle de un deudor con historial completo."""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM deudores WHERE id = ?", (deudor_id,))
        deudor = await cursor.fetchone()
        if not deudor:
            raise HTTPException(status_code=404, detail="Deudor no encontrado")

        cursor_h = await db.execute(
            "SELECT * FROM historial WHERE deudor_id = ? ORDER BY created_at DESC",
            (deudor_id,),
        )
        historial = [dict(r) for r in await cursor_h.fetchall()]

        cursor_l = await db.execute(
            "SELECT * FROM llamadas WHERE deudor_id = ? ORDER BY created_at DESC",
            (deudor_id,),
        )
        llamadas_raw = await cursor_l.fetchall()
        llamadas = []
        for r in llamadas_raw:
            d = dict(r)
            d["contestada"] = bool(d["contestada"])
            llamadas.append(d)

        data = dict(deudor)
        data["historial"] = historial
        data["llamadas"] = llamadas
        return data
    finally:
        await db.close()
