"""Rutas para el proceso de cobranza: scripts, audio y llamadas."""

import os
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import FileResponse
from database import get_db
from services.anthropic_client import generar_script_cobranza
from services.elevenlabs import generar_audio
from services.twilio_client import realizar_llamada, esta_configurado

router = APIRouter(prefix="/api/cobranza", tags=["Cobranza"])

AUDIOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audios")


async def _get_deudor(deudor_id: int):
    """Obtiene un deudor por ID o lanza 404."""
    db = await get_db()
    cursor = await db.execute("SELECT * FROM deudores WHERE id = ?", (deudor_id,))
    deudor = await cursor.fetchone()
    if not deudor:
        await db.close()
        raise HTTPException(status_code=404, detail="Deudor no encontrado")
    return db, dict(deudor)


@router.post("/generar-script/{deudor_id}")
async def generar_script(deudor_id: int):
    """Genera un script de cobranza personalizado con IA."""
    db, deudor = await _get_deudor(deudor_id)
    try:
        script = await generar_script_cobranza(
            nombre=deudor["nombre"],
            monto_deuda=deudor["monto_deuda"],
            dias_mora=deudor["dias_mora"],
            rut=deudor["rut"],
        )

        await db.execute(
            "UPDATE deudores SET script = ?, estado = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (script, "script_generado", deudor_id),
        )
        await db.execute(
            "INSERT INTO historial (deudor_id, accion, detalle) VALUES (?, ?, ?)",
            (deudor_id, "script_generado", "Script de cobranza generado con IA"),
        )
        await db.commit()

        return {"mensaje": "Script generado exitosamente", "script": script}
    finally:
        await db.close()


@router.post("/generar-audio/{deudor_id}")
async def generar_audio_endpoint(deudor_id: int):
    """Genera audio MP3 del script usando Eleven Labs."""
    db, deudor = await _get_deudor(deudor_id)
    try:
        if not deudor["script"]:
            raise HTTPException(
                status_code=400,
                detail="Primero debe generar el script de cobranza"
            )

        audio_path = await generar_audio(deudor["script"], deudor_id)

        await db.execute(
            "UPDATE deudores SET audio_path = ?, estado = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (audio_path, "audio_generado", deudor_id),
        )
        await db.execute(
            "INSERT INTO historial (deudor_id, accion, detalle) VALUES (?, ?, ?)",
            (deudor_id, "audio_generado", f"Audio generado: {os.path.basename(audio_path)}"),
        )
        await db.commit()

        return {
            "mensaje": "Audio generado exitosamente",
            "audio_url": f"/api/audio/{deudor_id}",
        }
    finally:
        await db.close()


@router.post("/llamar/{deudor_id}")
async def llamar_deudor(deudor_id: int, request: Request):
    """Realiza llamada telefónica al deudor."""
    db, deudor = await _get_deudor(deudor_id)
    try:
        if not deudor["audio_path"]:
            raise HTTPException(
                status_code=400,
                detail="Primero debe generar el audio"
            )

        if not esta_configurado():
            return {
                "mensaje": "Twilio no está configurado. Audio disponible para descarga.",
                "audio_url": f"/api/audio/{deudor_id}",
                "twilio_configurado": False,
            }

        base_url = str(request.base_url).rstrip("/")
        audio_url = f"{base_url}/api/audio/{deudor_id}"
        webhook_url = f"{base_url}/webhook/twilio"

        resultado = await realizar_llamada(
            telefono_destino=deudor["telefono"],
            audio_url=audio_url,
            webhook_url=webhook_url,
        )

        twilio_sid = resultado.get("sid", "")
        await db.execute(
            "INSERT INTO llamadas (deudor_id, twilio_sid, estado) VALUES (?, ?, ?)",
            (deudor_id, twilio_sid, "iniciada"),
        )
        await db.execute(
            "UPDATE deudores SET estado = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            ("llamado", deudor_id),
        )
        await db.execute(
            "INSERT INTO historial (deudor_id, accion, detalle) VALUES (?, ?, ?)",
            (deudor_id, "llamada_iniciada", f"Llamada iniciada - SID: {twilio_sid}"),
        )
        await db.commit()

        return {
            "mensaje": "Llamada iniciada exitosamente",
            "twilio_sid": twilio_sid,
            "twilio_configurado": True,
        }
    finally:
        await db.close()


@router.get("/audio/{deudor_id}")
async def stream_audio(deudor_id: int):
    """Sirve el archivo MP3 para reproducción."""
    audio_path = os.path.join(AUDIOS_DIR, f"cobranza_{deudor_id}.mp3")
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    return FileResponse(audio_path, media_type="audio/mpeg", filename=f"cobranza_{deudor_id}.mp3")
