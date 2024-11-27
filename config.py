import os
from ctypes import c_ssize_t

from dotenv import load_dotenv
from flask.cli import routes_command

load_dotenv()  # Cargar las variables de entorno desde el archivo .env

class Config:
    # Configuración de la base de datos MySQL
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('root')}:{os.getenv('xTuMaNptdsOzYlHUbeDPiCfnbfpiMAVy')}@"
        f"{os.getenv('junction.proxy')}:{os.getenv('12553')}/{os.getenv('tablas_OK')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

