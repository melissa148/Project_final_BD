from datetime import datetime
from app import db

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(45), nullable=False)
    fechaNacimiento = db.Column(db.Date)
    correo = db.Column(db.String(45))
    celular = db.Column(db.String(45))
    seguidores = db.relationship('Seguimiento', backref='persona', foreign_keys='Seguimiento.idPersona')
    seguidos = db.relationship('Seguimiento', backref='seguido', foreign_keys='Seguimiento.idPersonaSeguida')
    publicaciones = db.relationship('Publicacion', backref='usuario', lazy='dynamic')

class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idPersona = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    cantidadSeguidores = db.Column(db.Integer, nullable=False)
    persona = db.relationship('Usuario', backref=db.backref('influencer', uselist=False))

class Publicacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idPersona = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    fechaPublicacion = db.Column(db.DateTime, default=datetime.now)
    especial = db.Column(db.Boolean, default=False)

class Seguimiento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idPersona = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    idPersonaSeguida = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    activo = db.Column(db.Boolean, nullable=False)

class Historico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idPersona = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    fechaHistorico = db.Column(db.Date, nullable=False)
    tipoHistorico = db.Column(db.String(45), nullable=False)
