"""Cliente para la API de OpenAI - Generación de scripts de cobranza."""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
API_URL = "https://api.openai.com/v1/chat/completions"


async def generar_script_cobranza(
    nombre: str,
    monto_deuda: float,
    dias_mora: int,
    rut: str
) -> str:
    """Genera un script de cobranza personalizado usando la API de OpenAI."""

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
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "gpt-4o",
        "max_tokens": 1024,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]
