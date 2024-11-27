from app.routes.home import home_bp
from app.routes.users import user_bp
from app.routes.influencers import influencer_bp
from app.routes.posts import post_bp


def init_routes(app):
    app.register_blueprint(home_bp)  # Ruta de inicio
    app.register_blueprint(user_bp, url_prefix='/users')  # Rutas de usuarios
    app.register_blueprint(influencer_bp, url_prefix='/influencers')  # Rutas de influencers
    app.register_blueprint(post_bp, url_prefix='/posts')  # Rutas de publicaciones
