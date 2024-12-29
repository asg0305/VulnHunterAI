from flask import Flask

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_object('config.Config')

    # Registrar blueprints
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
