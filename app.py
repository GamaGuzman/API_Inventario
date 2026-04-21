from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST"),
        database=os.environ.get("DB_NAME"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD")
    )

@app.route("/productos", methods=["POST"])
def crear_producto():
    data = request.json

    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO productos (titulo, descripcion, precio, stock, imagen_url)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
    """, (
        data["titulo"],
        data.get("descripcion"),
        data["precio"],
        data["stock"],
        data.get("imagen_url")
    ))

    new_id = cursor.fetchone()[0]

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"id": new_id}), 201

@app.route("/productos", methods=["GET"])
def listar_productos():
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, titulo, descripcion, precio, stock 
        FROM productos
    """)

    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    productos = [dict(zip(columns, row)) for row in rows]

    cursor.close()
    conn.close()

    return jsonify(productos)

@app.route("/productos/<int:id>", methods=["DELETE"])
def eliminar_producto(id):
    conn = get_conn()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"mensaje": "eliminado"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)