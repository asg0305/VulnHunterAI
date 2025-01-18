from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.Config')

    # Registrar blueprints
    from .routes import main as main_blueprint
    #from .tasks import celery_bp as celery_blueprint
    app.register_blueprint(main_blueprint)
    #app.register_blueprint(celery_blueprint)

    return app


