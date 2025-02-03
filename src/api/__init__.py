from quart import Blueprint
from .background import background as background
from .streaming import streaming as streaming

api = Blueprint("api", __name__, url_prefix="/api")

api.register_blueprint(background)
api.register_blueprint(streaming)
