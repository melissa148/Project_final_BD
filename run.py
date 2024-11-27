from app import create_app

# Crea la aplicación Flask
app = create_app()

# Inicia la aplicación Flask
if __name__ == '__main__':
    app.run(debug=True,  port=5001)  # Esto puede cambiar a app.run(host='0.0.0.0') en producción
