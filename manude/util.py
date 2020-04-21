from manude.models.database import db
from manude.models.models import models, User
from os import urandom, makedirs, path
import typing
import pkg_resources


def get_installed_packages() -> typing.List[str]:
    return [
        pkg.key for pkg in pkg_resources.working_set
    ]


def stable_database_connection() -> db:
    if not db.is_connection_usable():
        db.connect(reuse_if_open=True)
        db.create_tables(models)
    return db


def calculate_static(abs_path: str) -> str:
    abs_path = abs_path.split("/")
    if "static" not in abs_path:
        raise Exception("Folder has no estimation to static")
    new_path = abs_path[abs_path.index("static"):]
    return "/" + "/".join(new_path)


def make_preview(
        photo_id: int,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        as_window: bool = False,
        config: dict = None,
        color: tuple = (73, 98, 240),
) -> typing.Union[str, bool]:
    from .app import app
    installed_pkg = get_installed_packages()

    if "opencv-python" not in installed_pkg or "numpy" not in installed_pkg:
        print("You need to install opencv-python and numpy packages to use preview")
        return False

    config = config or app.config

    import numpy as np
    import cv2

    image_path = config["image_dir"] + f"/{photo_id}.jpg"
    temp_path = "/".join(config["image_dir"].split("/")[:-1]) + "/temp"
    color = np.array(color, dtype="int16")

    image = cv2.imread(image_path)
    mask = np.zeros(image[y1:y2, x1:x2].shape)
    for iy, y in enumerate(mask):
        for ix, x in enumerate(y):
            mask[iy][ix] = color

    image[y1:y2, x1:x2] = mask

    if as_window:
        cv2.imshow("preview", image)
        cv2.waitKey()
        cv2.destroyAllWindows()
        return True

    if not path.exists(temp_path):
        makedirs(temp_path)
    file_path = temp_path + f"/{photo_id}_{x1}_{x2}_{y1}_{y2}.jpg"
    cv2.imwrite(file_path, image)
    return file_path


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
    from manude.routes import api, main, admin
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
