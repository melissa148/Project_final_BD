from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app import db
from app.models import Usuario, Seguimiento, Influencer, Publicacion, Historico
from datetime import datetime

main_bp = Blueprint('main', __name__)

# Ruta de inicio
@main_bp.route('/')
def index():
    return render_template('index.html')

# Ruta para registrar a un usuario
@main_bp.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
    nombre = request.form['nombre']
    fecha_nacimiento = request.form['fechaNacimiento']
    correo = request.form.get('correo')
    celular = request.form.get('celular')

    nueva_persona = Usuario(
        nombre=nombre,
        fechaNacimiento=fecha_nacimiento,
        correo=correo,
        celular=celular
    )
    db.session.add(nueva_persona)
    db.session.commit()

    return redirect(url_for('main.index'))

# Verificar si una persona es influencer
@main_bp.route('/verificar_influencer/<int:persona_id>', methods=['GET'])
def verificar_influencer(persona_id):
    persona = Usuario.query.get(persona_id)
    seguidores = len(persona.seguidores)
    seguidos = len(persona.seguidos)

    if seguidores > 1000 and seguidos < (seguidores * 0.1):
        # Marcar como influencer
        influencer = Influencer(idPersona=persona.id, cantidadSeguidores=seguidores)
        db.session.add(influencer)
        db.session.commit()
        return jsonify({"message": f"{persona.nombre} ahora es un influencer!"})

    return jsonify({"message": f"{persona.nombre} no es un influencer."})

# Crear una nueva publicación
@main_bp.route('/crear_publicacion', methods=['POST'])
def crear_publicacion():
    persona_id = request.form['persona_id']
    url = request.form['url']
    tipo = request.form['tipo']  # 'video' o 'imagen'
    es_especial = request.form.get('especial') == 'on'

    nueva_publicacion = Publicacion(
        idPersona=persona_id,
        url=url,
        fechaPublicacion=datetime.now(),
        especial=es_especial
    )
    db.session.add(nueva_publicacion)
    db.session.commit()

    return redirect(url_for('main.index'))

# Guardar el historial de cuándo alguien fue influencer
def guardar_historial_influencer(persona_id):
    persona = Usuario.query.get(persona_id)
    if persona.es_influencer:
        historial = Historico(idPersona=persona.id, fechaHistorico=datetime.now(), tipoHistorico="Influencer")
        db.session.add(historial)
        db.session.commit()
