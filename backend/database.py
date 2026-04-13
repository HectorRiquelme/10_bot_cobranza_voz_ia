"""Configuración de base de datos SQLite con aiosqlite."""

import aiosqlite
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "cobranza.db")


async def get_db() -> aiosqlite.Connection:
    """Obtiene conexión a la base de datos."""
    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    await db.execute("PRAGMA foreign_keys=ON")
    return db


async def init_db():
    """Inicializa las tablas de la base de datos."""
    db = await get_db()
    try:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS deudores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                rut TEXT NOT NULL,
                telefono TEXT NOT NULL,
                monto_deuda REAL NOT NULL,
                dias_mora INTEGER NOT NULL,
                email TEXT,
                estado TEXT DEFAULT 'pendiente',
                script TEXT,
                audio_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS historial (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deudor_id INTEGER NOT NULL,
                accion TEXT NOT NULL,
                detalle TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deudor_id) REFERENCES deudores(id)
            );

            CREATE TABLE IF NOT EXISTS llamadas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                deudor_id INTEGER NOT NULL,
                twilio_sid TEXT,
                estado TEXT DEFAULT 'iniciada',
                duracion INTEGER DEFAULT 0,
                contestada INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (deudor_id) REFERENCES deudores(id)
            );
        """)
        await db.commit()
    finally:
        await db.close()
