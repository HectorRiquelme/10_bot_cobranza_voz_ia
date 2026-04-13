"""Webhook para recibir eventos de Twilio."""

from fastapi import APIRouter, Request
from database import get_db

router = APIRouter(tags=["Webhooks"])


@router.post("/webhook/twilio")
async def twilio_webhook(request: Request):
    """Recibe callbacks de estado de llamadas de Twilio."""
    form = await request.form()
    call_sid = form.get("CallSid", "")
    call_status = form.get("CallStatus", "")
    call_duration = form.get("CallDuration", "0")

    db = await get_db()
    try:
        contestada = call_status in ("completed", "answered", "in-progress")

        await db.execute(
            """UPDATE llamadas SET estado = ?, duracion = ?, contestada = ?
               WHERE twilio_sid = ?""",
            (call_status, int(call_duration or 0), int(contestada), call_sid),
        )

        cursor = await db.execute(
            "SELECT deudor_id FROM llamadas WHERE twilio_sid = ?", (call_sid,)
        )
        row = await cursor.fetchone()

        if row:
            deudor_id = row["deudor_id"]
            nuevo_estado = "contesto" if contestada else "no_contesto"

            if call_status in ("completed", "no-answer", "busy", "failed", "canceled"):
                await db.execute(
                    "UPDATE deudores SET estado = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                    (nuevo_estado, deudor_id),
                )

            await db.execute(
                "INSERT INTO historial (deudor_id, accion, detalle) VALUES (?, ?, ?)",
                (
                    deudor_id,
                    f"twilio_{call_status}",
                    f"Estado: {call_status}, Duración: {call_duration}s",
                ),
            )

        await db.commit()
    finally:
        await db.close()

    return {"status": "ok"}
