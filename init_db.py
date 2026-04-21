import psycopg2
import os

conn = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD")
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT,
    precio NUMERIC(10,2) NOT NULL,
    moneda VARCHAR(10) DEFAULT 'MXN',
    stock INT NOT NULL DEFAULT 0,
    rating_promedio NUMERIC(2,1) DEFAULT 0,
    total_reviews INT DEFAULT 0,
    imagen_url TEXT,
    creado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

conn.commit()
cursor.close()
conn.close()

print("Base de datos inicializada")