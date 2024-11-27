from flask import Blueprint, jsonify, request
from app.models import Usuario, db
from app.neo4j_connection import Neo4jConnection

# Inicializar la conexión con Neo4j
neo4j_connection = Neo4jConnection(uri="bolt://44.214.2.87", user="neo4j", password="maples-altimeter-dip")

influencer_bp = Blueprint('influencer_bp', __name__)

# Obtener influencers
@influencer_bp.route('/influencers', methods=['GET'])
def obtener_influencers():
    try:
        # Obtener influencers desde MySQL
        influencers = Usuario.query.filter(Usuario.seguidores > 1000).all()
        influencers_mysql = [{"id": i.id, "nombre": i.nombre, "seguidores": i.seguidores} for i in influencers]

        # Obtener influencers desde Neo4j
        query = "MATCH (i:Usuario)-[:ES_INFLUENCER]->(:Influencer) RETURN i.nombre AS nombre, i.seguidores AS seguidores"
        influencers_neo4j = neo4j_connection.execute_query(query)

        return jsonify({
            "influencers_mysql": influencers_mysql,
            "influencers_neo4j": influencers_neo4j
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Agregar influencer
@influencer_bp.route('/agregar_influencer', methods=['POST'])
def agregar_influencer():
    try:
        nombre = request.json.get('nombre')
        seguidores = request.json.get('seguidores')

        if not nombre or seguidores is None:
            return jsonify({"error": "El nombre y los seguidores son requeridos"}), 400

        # Crear en MySQL
        nuevo_influencer = Usuario(nombre=nombre, seguidores=seguidores)
        db.session.add(nuevo_influencer)
        db.session.commit()

        # Crear en Neo4j
        query = "CREATE (i:Usuario {id: $id, nombre: $nombre, seguidores: $seguidores})-[:ES_INFLUENCER]->(:Influencer)"
        neo4j_connection.execute_query(query, parameters={"id": nuevo_influencer.id, "nombre": nombre, "seguidores": seguidores})

        return jsonify({"message": f"Influencer {nombre} agregado a MySQL y Neo4j"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Actualizar influencer
@influencer_bp.route('/actualizar_influencer/<int:influencer_id>', methods=['PUT'])
def actualizar_influencer(influencer_id):
    try:
        data = request.json
        nombre = data.get('nombre')
        seguidores = data.get('seguidores')

        if not nombre or seguidores is None:
            return jsonify({"error": "Nombre y seguidores son obligatorios"}), 400

        influencer = Usuario.query.get(influencer_id)
        if not influencer:
            return jsonify({"error": "Influencer no encontrado"}), 404

        influencer.nombre = nombre
        influencer.seguidores = seguidores
        db.session.commit()

        query = """
            MATCH (i:Usuario {id: $id})-[:ES_INFLUENCER]->(:Influencer)
            SET i.nombre = $nombre, i.seguidores = $seguidores
        """
        neo4j_connection.execute_query(query, parameters={"id": influencer_id, "nombre": nombre, "seguidores": seguidores})

        return jsonify({"message": "Influencer actualizado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# Eliminar influencer
@influencer_bp.route('/eliminar_influencer/<int:influencer_id>', methods=['DELETE'])
def eliminar_influencer(influencer_id):
    try:
        influencer = Usuario.query.get(influencer_id)
        if not influencer:
            return jsonify({"error": "Influencer no encontrado"}), 404

        db.session.delete(influencer)
        db.session.commit()

        query = """
            MATCH (i:Usuario {id: $id})-[:ES_INFLUENCER]->(:Influencer)
            DETACH DELETE i
        """
        neo4j_connection.execute_query(query, parameters={"id": influencer_id})

        return jsonify({"message": "Influencer eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
