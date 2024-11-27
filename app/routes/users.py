from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app.models import Usuario, Seguimiento, db

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/usuario/<int:usuario_id>')
def ver_usuario(usuario_id):
    if usuario_id is None:
        # Manejar el caso en el que usuario_id es None
        return redirect(url_for('home'))
    usuario = Usuario.query.get_or_404(usuario_id)
    return render_template('user/ver_usuario.html', usuario=usuario)

@user_bp.route('/usuario/<int:usuario_id>/seguir', methods=['POST'])
def seguir_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    seguimiento = Seguimiento(idPersona=current_user.id, idPersonaSeguida=usuario.id, activo=True)
    db.session.add(seguimiento)
    db.session.commit()
    return redirect(url_for('user_bp.ver_usuario', usuario_id=usuario.id))

@user_bp.route('/usuario/<int:usuario_id>/dejar-de-seguir', methods=['POST'])
def dejar_de_seguir(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    seguimiento = Seguimiento.query.filter_by(idPersona=current_user.id, idPersonaSeguida=usuario.id).first()
    if seguimiento:
        seguimiento.activo = False
        db.session.commit()
    return redirect(url_for('user_bp.ver_usuario', usuario_id=usuario.id))
