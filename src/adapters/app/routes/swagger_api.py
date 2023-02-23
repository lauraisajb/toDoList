from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/swagger"
API_URL = "/static/swagger.json"
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "Todo-Python-Flask-REST"}
)


def get_blueprint():
    """Return the blueprint for the swagger module"""
    return SWAGGERUI_BLUEPRINT
