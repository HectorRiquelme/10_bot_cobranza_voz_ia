# Prompt 1 - Bot de cobranza con voz IA (Eleven Labs + CRM)

**Stack:** Python, FastAPI, React, Eleven Labs API, SQLite

---

Crea un sistema de cobranza automatizada con voz IA real usando Eleven Labs. Python + FastAPI backend, React frontend. Usa Eleven Labs API (https://api.elevenlabs.io). Implementa: 1) admin carga CSV de deudores, 2) genera script de cobranza personalizado usando la API de Anthropic (Claude) con el contexto del deudor, 3) envia el script a Eleven Labs API (POST /v1/text-to-speech/:voice_id) para generar audio, 4) almacena el MP3 generado en disco, 5) integra con Twilio API para realizar llamada telefonica reproduciendo el audio (o con enlace descargable si no hay Twilio), 6) webhook de Twilio para registrar si contesto o no. Panel admin con player, metricas y exportacion a Excel. README: crear cuenta Eleven Labs (tier gratis), obtener API key y voice_id.

---

**IMPORTANTE:** No incluyas referencias a Claude, Claude Code, Anthropic ni ningun asistente IA en commits, README, package.json, comentarios de codigo ni en ningun archivo del proyecto. El unico autor debe ser "Hector Riquelme" con el email y usuario de GitHub "HectorRiquelme".
