"""Cliente para la API de Twilio - Llamadas telefónicas."""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "")


def esta_configurado() -> bool:
    """Verifica si Twilio está configurado."""
    return bool(TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and TWILIO_PHONE_NUMBER)


async def realizar_llamada(
    telefono_destino: str,
    audio_url: str,
    webhook_url: str,
) -> dict:
    """Realiza una llamada telefónica reproduciendo un audio MP3 vía Twilio."""

    if not esta_configurado():
        return {"error": "Twilio no está configurado", "configurado": False}

    url = (
        f"https://api.twilio.com/2010-04-01/"
        f"Accounts/{TWILIO_ACCOUNT_SID}/Calls.json"
    )

    twiml = (
        f'<Response><Play>{audio_url}</Play>'
        f'<Pause length="2"/>'
        f'<Say language="es-MX">Gracias por su atención. Adiós.</Say>'
        f'</Response>'
    )

    data = {
        "To": telefono_destino,
        "From": TWILIO_PHONE_NUMBER,
        "Twiml": twiml,
        "StatusCallback": webhook_url,
        "StatusCallbackEvent": "initiated ringing answered completed",
        "StatusCallbackMethod": "POST",
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            url,
            data=data,
            auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
        )
        response.raise_for_status()
        return response.json()
