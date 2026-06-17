import sqlite3
import os

# Import the get_connection helper from the existing database module
from .database import get_connection, DB_PATH

def migrate():
    """Ejecuta la migración de la base de datos a la nueva estructura.
    - Crea tabla temporal `properties_new` con la nueva definición (incluye user_id).
    - Copia los datos de `properties` a la tabla nueva, asignando user_id=1 por defecto.
    - Reemplaza la tabla original.
    - Crea tabla temporal `predictions_new` con FK a `properties`.
    - Si existen datos en `predictions`, los migra dejando property_id NULL (se podrá actualizar manualmente).
    - Finalmente, crea índices (ya están en init_db) y cierra la conexión.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # 1. Asegurar que existe al menos un usuario de prueba en la tabla users
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        if user_count == 0:
            cursor.execute(
                "INSERT INTO users (id, nombre, email) VALUES (1, 'Usuario de Prueba', 'prueba@example.com')"
            )

        # 2. Crear tabla temporal con el nuevo esquema
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS properties_new (
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
            precio_predicho REAL,
            diferencia REAL,
            es_oportunidad INTEGER,
            created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
            updated_at TEXT
        );
        """)
        # 3. Copiar datos existentes, rellenando user_id con 1 (usuario de prueba).
        # Omitimos created_at para usar el default de properties_new.
        cursor.execute("""
            INSERT INTO properties_new (
                id, user_id, latitud, longitud, area_m2, habitaciones, banos,
                distancia_centro_km, antiguedad_anos, tiene_piscina, precio_lista,
                precio_predicho, diferencia, es_oportunidad, updated_at
            )
            SELECT
                id,
                1 AS user_id,
                COALESCE(latitud, 0.0),
                COALESCE(longitud, 0.0),
                COALESCE(area_m2, 0.0),
                COALESCE(habitaciones, 0),
                COALESCE(banos, 0),
                COALESCE(distancia_centro_km, 0.0),
                COALESCE(antiguedad_anos, 0.0),
                COALESCE(tiene_piscina, 0),
                COALESCE(precio_lista, 0.0),
                precio_predicho,
                diferencia,
                es_oportunidad,
                NULL
            FROM properties;
        """)
        # 4. Eliminar tabla antigua y renombrar la nueva
        cursor.executescript("""
            DROP TABLE IF EXISTS properties;
            ALTER TABLE properties_new RENAME TO properties;
        """)
        # 5. Crear tabla temporal predictions_new con FK a properties (property_id es nullable)
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS predictions_new (
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
        """)
        # 6. Migrar datos de predictions si existen (se asume que la tabla antigua no tiene property_id)
        # En este caso, los registros se insertan con property_id como NULL.
        cursor.execute("""
            INSERT INTO predictions_new (
                user_id, property_id, area_m2, habitaciones, banos,
                distancia_centro_km, antiguedad_anos, tiene_piscina,
                predicted_price, margin_of_error, model_version, created_at
            )
            SELECT
                user_id, NULL, area_m2, habitaciones, banos,
                distancia_centro_km, antiguedad_anos, tiene_piscina,
                predicted_price, margin_of_error, 'v1', created_at
            FROM predictions;
        """)
        # 7. Reemplazar tabla predictions
        cursor.executescript("""
            DROP TABLE IF EXISTS predictions;
            ALTER TABLE predictions_new RENAME TO predictions;
        """)
        conn.commit()
        print("Migración completada con éxito.")
    except Exception as e:
        conn.rollback()
        raise RuntimeError(f"Error durante la migración: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
