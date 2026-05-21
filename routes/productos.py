from flask import Blueprint, jsonify, request
from config import get_conn

productos_bp = Blueprint('productos', __name__)

@productos_bp.route("/", methods=["POST"])
def crear_producto():
    data = request.json
    conn = get_conn()
    cursor = conn.cursor()
    
    try:
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
        return jsonify({"id": new_id}), 201
        
    finally:
        cursor.close()
        conn.close()


@productos_bp.route("/", methods=["GET"])
def listar_productos():

    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, titulo, descripcion, precio, stock 
            FROM productos
        """)
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        productos = [dict(zip(columns, row)) for row in rows]
        
        return jsonify(productos), 200
        
    finally:
        cursor.close()
        conn.close()


@productos_bp.route("/<int:id>", methods=["DELETE"])
def eliminar_producto(id):

    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
        conn.commit()
        
        return jsonify({"mensaje": f"Producto con ID {id} eliminado exitosamente"}), 200
        
    finally:
        cursor.close()
        conn.close()


@productos_bp.route("/<int:id>/comprar", methods=["POST"])
def comprar_producto(id):

    data = request.json or {}
    cantidad_a_comprar = data.get("cantidad", 1)

    conn = get_conn()
    cursor = conn.cursor()
    
    try:
        conn.autocommit = False 

        cursor.execute("""
            SELECT titulo, stock, precio 
            FROM productos 
            WHERE id = %s 
            FOR UPDATE
        """, (id,))
        
        producto = cursor.fetchone()
        
        if not producto:
            conn.rollback()
            return jsonify({"error": "Producto no encontrado"}), 404
            
        titulo, stock_actual, precio = producto

        if stock_actual < cantidad_a_comprar:
            conn.rollback()
            return jsonify({
                "error": f"Stock insuficiente para '{titulo}'. Disponible: {stock_actual}"
            }), 400

        nuevo_stock = stock_actual - cantidad_a_comprar
        cursor.execute("""
            UPDATE productos 
            SET stock = %s 
            WHERE id = %s
        """, (nuevo_stock, id))

        conn.commit()
        
        return jsonify({
            "mensaje": "Compra realizada con éxito",
            "producto": titulo,
            "cantidad_comprada": cantidad_a_comprar,
            "stock_restante": nuevo_stock,
            "total_pagado": precio * cantidad_a_comprar
        }), 200
        
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Error interno al procesar la compra", "detalle": str(e)}), 500
        
    finally:
        cursor.close()
        conn.close()