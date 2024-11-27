from flask import Blueprint, render_template, redirect, url_for, request
from app.models import Publicacion, Usuario, db

post_bp = Blueprint('post_bp', __name__)

@post_bp.route('/publicacion/<int:post_id>')
def ver_publicacion(post_id):
    if post_id is None:
        # Manejar el caso en el que usuario_id es None
        return redirect(url_for('home'))
    publicacion = Publicacion.query.get_or_404(post_id)
    return render_template('post/ver_publicacion.html', publicacion=publicacion)

@post_bp.route('/usuario/<int:usuario_id>/publicar', methods=['GET', 'POST'])
def publicar(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    if request.method == 'POST':
        url = request.form['url']
        publicacion = Publicacion(idPersona=usuario.id, url=url)
        db.session.add(publicacion)
        db.session.commit()
        return redirect(url_for('user_bp.ver_usuario', usuario_id=usuario.id))
    return render_template('post/publicar.html', usuario=usuario)
