import sqlite3
import os


# Ruta absoluta a la base de datos SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "real_estate.db")
DB_PATH = os.path.normpath(DB_PATH)


def get_connection() -> sqlite3.Connection:
    """
    Crea y devuelve una conexión SQLite configurada con:
    - row_factory para devolver dicts
    - WAL mode para mejor concurrencia
    - Foreign keys activadas
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db() -> None:
    """
    Inicializa el esquema de la base de datos.
    Crea las tablas si no existen.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.executescript("""
-- Tabla users (sin cambios)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
);

-- Tabla properties (actualizada)
CREATE TABLE IF NOT EXISTS properties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    latitud REAL NOT NULL CHECK(latitud BETWEEN -90 AND 90),
    longitud REAL NOT NULL CHECK(longitud BETWEEN -180 AND 180),
    area_m2 REAL NOT NULL CHECK(area_m2 > 0),
    habitaciones INTEGER NOT NULL CHECK(habitaciones > 0),
    banos INTEGER NOT NULL CHECK(banos > 0),
    distancia_centro_km REAL NOT NULL CHECK(distancia_centro_km >= 0),
    antiguedad_anos REAL NOT NULL CHECK(antiguedad_anos >= 0),
    tiene_piscina INTEGER NOT NULL DEFAULT 0 CHECK(tiene_piscina IN (0,1)),
    precio_lista REAL NOT NULL CHECK(precio_lista >= 0),
    precio_predicho REAL,        -- columna derivada (se mantiene)
    diferencia REAL,            -- columna derivada (se mantiene)
    es_oportunidad INTEGER,     -- 0/1, se mantiene
    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
    updated_at TEXT
);

-- Tabla predictions (actualizada)
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    property_id INTEGER REFERENCES properties(id),
    area_m2 REAL,
    habitaciones INTEGER,
    banos INTEGER,
    distancia_centro_km REAL,
    antiguedad_anos REAL,
    tiene_piscina INTEGER,
    predicted_price REAL NOT NULL CHECK(predicted_price >= 0),
    margin_of_error REAL CHECK(margin_of_error >= 0),
    model_version TEXT NOT NULL DEFAULT 'v1',
    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_properties_user_id ON properties(user_id);
CREATE INDEX IF NOT EXISTS idx_properties_precio ON properties(precio_lista);
CREATE INDEX IF NOT EXISTS idx_properties_area ON properties(area_m2);
CREATE INDEX IF NOT EXISTS idx_properties_hab ON properties(habitaciones);
CREATE INDEX IF NOT EXISTS idx_properties_ubicacion ON properties(latitud, longitud);
CREATE INDEX IF NOT EXISTS idx_predictions_user_id ON predictions(user_id);
CREATE INDEX IF NOT EXISTS idx_predictions_property_id ON predictions(property_id);
CREATE INDEX IF NOT EXISTS idx_predictions_fecha ON predictions(created_at);
""")
    # Insertar usuario por defecto (Test) si la tabla está vacía para evitar fallos de Foreign Key
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO users (id, nombre, email) VALUES (1, 'Test', 'test@test.com')")
    conn.commit()
    conn.close()
