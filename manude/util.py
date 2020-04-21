from manude.models.database import db
from manude.models.models import models, User
from os import urandom

def stable_database_connection() -> db:
    if not db.is_connection_usable():
        db.connect(reuse_if_open=True)
        db.create_tables(models)


def run_app(
        host: str = None,
        port: int = None,
        secret_key: str = None,
        image_dir: str = "manude/static/imgs",
):
    """
    Run flask app directly
    :param host:
    :param port:
    :param secret_key:
    :param image_dir: directory with images
    :return:
    """
    from .app import app
    app.config["image_dir"] = image_dir or "imgs"
    from manude.routes import api, main
    stable_database_connection()
    app.secret_key = secret_key or urandom(24)
    app.run(host, port)


def new_user_manually(token: str, username: str = None):
    stable_database_connection()
    query = {k: v for k, v in locals().items() if v is not None}
    return User.get_or_create(**query)


def delete_user_manually(uid: int = None, token: str = None, username: str = None):
    stable_database_connection()
    query = {k: v for k, v in locals().items() if v is not None}
    return User.get(**query).delete()
