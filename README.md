# Bot de Cobranza con Voz IA

Sistema de cobranza automatizada que genera scripts personalizados, sintetiza voz con Eleven Labs y realiza llamadas telefónicas vía Twilio.

**Autor:** Hector Riquelme

## Stack

- **Backend:** Python, FastAPI, SQLite, httpx, Pydantic
- **Frontend:** React, Vite, Tailwind CSS
- **APIs:** OpenAI GPT-4o (generación de scripts), Eleven Labs (voz), Twilio (llamadas)

## Instalación

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Editar .env con las API keys reales
python main.py
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Uso

1. Acceder a `http://localhost:5173`
2. Cargar CSV de deudores desde la pestaña "Cargar CSV"
3. En la tabla de deudores: Generar Script → Generar Audio → Llamar
4. El dashboard muestra métricas en tiempo real
5. Exportar reporte Excel desde el botón en el dashboard

## Variables de Entorno

| Variable | Descripción |
|---|---|
| `OPENAI_API_KEY` | API key de OpenAI |
| `ELEVENLABS_API_KEY` | API key de Eleven Labs |
| `ELEVENLABS_VOICE_ID` | ID de la voz en Eleven Labs |
| `TWILIO_ACCOUNT_SID` | Account SID de Twilio |
| `TWILIO_AUTH_TOKEN` | Auth Token de Twilio |
| `TWILIO_PHONE_NUMBER` | Número de teléfono Twilio |
| `PORT` | Puerto del backend (default: 8000) |
