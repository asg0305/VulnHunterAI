from app import create_app
from twisted.internet import reactor
from flask import jsonify

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    if not reactor.running:
        reactor.run()
