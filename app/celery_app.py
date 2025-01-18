from backend import create_app
app = create_app()
app.app_context().push()

from backend.tasks import celery_bp
app.register_blueprint(celery_bp)
def get_app():
    return app

if __name__ == '__main__':
    from twisted.internet import reactor

    app.run(host='0.0.0.0', port=5000)

    if not reactor.running:
        reactor.run()
