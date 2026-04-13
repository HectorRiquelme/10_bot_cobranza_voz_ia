"""Cliente para la API de Eleven Labs - Síntesis de voz."""

import httpx
import os
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "pNInz6obpgDQGcFmaJgB")

API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
AUDIOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "audios")


async def generar_audio(texto: str, deudor_id: int) -> str:
    """Envía texto a Eleven Labs y guarda el MP3 resultante."""

    os.makedirs(AUDIOS_DIR, exist_ok=True)

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }

    payload = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    voice_id = ELEVENLABS_VOICE_ID
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()

        audio_path = os.path.join(AUDIOS_DIR, f"cobranza_{deudor_id}.mp3")
        with open(audio_path, "wb") as f:
            f.write(response.content)

        return audio_path
