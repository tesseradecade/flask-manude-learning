from manude.models.database import db
from manude.models.models import models, User
from os import urandom

def run_app(
        host: str = None,
        port: int = None,
        secret_key: str = None
):
    """
    Run flask app directly
    :param host:
    :param port:
    :param secret_key:
    :return:
    """
    from .app import app
    from manude.routes import api, main
    db.connect()
    db.create_tables(models)
    app.secret_key = secret_key or urandom(24)
    app.run(host, port)


def new_user_manually(token: str, name: str = None):
    query = {k: v for k, v in locals().items() if v is not None}
    return User.create()
