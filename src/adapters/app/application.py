from flask import Flask, jsonify, make_response
from flask_cors import CORS

from src.main.config import init_app
from src.main.containers import Container

from .routes import todo_api, swagger_api


def create_app() -> Flask:
    container = Container()
    app = Flask(__name__)
    app.container = container
    with app.app_context():
        init_app(app)
        CORS().init_app(app)
    
    app.register_blueprint(todo_api.get_blueprint())
    app.register_blueprint(swagger_api.get_blueprint())

    @app.errorhandler(400)
    def handle_400_error(_error):
        """Return a http 400 error to client"""
        return make_response(jsonify({"error": "Misunderstood"}), 400)

    @app.errorhandler(401)
    def handle_401_error(_error):
        """Return a http 401 error to client"""
        return make_response(jsonify({"error": "Unauthorised"}), 401)

    @app.errorhandler(404)
    def handle_404_error(_error):
        """Return a http 404 error to client"""
        return make_response(jsonify({"error": "Not found"}), 404)

    @app.errorhandler(500)
    def handle_500_error(_error):
        """Return a http 500 error to client"""
        return make_response(jsonify({"error": "Server error"}), 500)
    return app
