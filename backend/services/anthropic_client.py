"""Cliente para la API de Anthropic - Generación de scripts de cobranza."""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
API_URL = "https://api.anthropic.com/v1/messages"


async def generar_script_cobranza(
    nombre: str,
    monto_deuda: float,
    dias_mora: int,
    rut: str
) -> str:
    """Genera un script de cobranza personalizado usando la API de Anthropic."""

    monto_formateado = f"${monto_deuda:,.0f}"

    system_prompt = (
        "Eres un agente de cobranza profesional y respetuoso. "
        "Genera un script de llamada telefónica para cobrar una deuda. "
        "El tono debe ser firme pero cordial. Incluye saludo, identificación, "
        "motivo de la llamada, opciones de pago y despedida. "
        "El script debe ser natural para ser leído en voz alta. "
        "Responde SOLO con el script, sin encabezados ni notas adicionales."
    )

    user_message = (
        f"Genera un script de cobranza telefónica para el siguiente deudor:\n"
        f"- Nombre: {nombre}\n"
        f"- RUT: {rut}\n"
        f"- Monto adeudado: {monto_formateado} pesos\n"
        f"- Días de mora: {dias_mora} días\n\n"
        f"El script debe durar aproximadamente 40 segundos al ser leído."
    )

    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }

    payload = {
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 1024,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": user_message}
        ],
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["content"][0]["text"]
