from manude.models.database import db
from manude.models.models import models, User
from os import urandom, makedirs, path, listdir, remove
import typing
import pkg_resources
import shutil

try:
    import numpy as np
    import cv2
except ImportError:
    pass

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

    image_path = config["image_dir"] + f"/{photo_id}.jpg"
    temp_path = "/".join(config["image_dir"].split("/")[:-1]) + "/temp"

    if path.exists(temp_path + f"/{photo_id}_{x1}_{x2}_{y1}_{y2}.jpg"):
        return temp_path + f"/{photo_id}_{x1}_{x2}_{y1}_{y2}.jpg"

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

def get_last_photo_id(folder_path: str):
    photo_ids = [int(photo_name.split(".")[0]) for photo_name in listdir(folder_path)]
    return max(photo_ids)


def rename_photos_for_static(
        path_to_photos: str,
        path_to_static: str,
        copy_files: bool = True,
) -> typing.List[str]:
    """
    Rename downloaded photos (with image-download-util)
    :param path_to_photos:
    :param path_to_static:
    :param copy_files:
    :return: list of renamed photo paths
    """
    file_names = []
    for file_name in listdir(path_to_photos):
        if "." not in file_name:
            # recursive
            file_names.extend(
                rename_photos_for_static(path.join(path_to_photos, file_name), path_to_static)
            )
        elif file_name.split(".")[-1] != "jpg":
            print(f"file type {file_name} is not supported")
        else:
            # change value copy_files to change mode
            mode = shutil.copyfile if copy_files else shutil.move
            photo_id = get_last_photo_id(path_to_static) + 1
            new_path = path.join(path_to_static, f"{photo_id}.jpg")

            mode(path.join(path_to_photos, file_name), new_path)
            file_names.append(new_path)
    return file_names

def resize_to_required_qualities(
        path_to_photos: str,
        delete_broken: bool = True,
):
    installed_pkg = get_installed_packages()

    if "opencv-python" not in installed_pkg or "numpy" not in installed_pkg:
        print("You need to install opencv-python and numpy packages to use method resize_to_required_qualities")
        return False

    import numpy as np
    import cv2

    def resize_to_square(im: np.array, desired_size: int = 1000):
        if im.shape == (desired_size, desired_size, 3):
            return im

        old_size = im.shape[:2]

        ratio = float(desired_size) / max(old_size)
        new_size = tuple([int(x * ratio) for x in old_size])
        im = cv2.resize(im, (new_size[1], new_size[0]))

        delta_w = desired_size - new_size[1]
        delta_h = desired_size - new_size[0]

        top, bottom = delta_h // 2, delta_h - (delta_h // 2)
        left, right = delta_w // 2, delta_w - (delta_w // 2)

        color = [0, 0, 0]
        im = cv2.copyMakeBorder(
            im, top, bottom, left, right, cv2.BORDER_CONSTANT, value=color
        )
        return im

    for file_name in listdir(path_to_photos):
        if file_name.endswith(".jpg"):
            print(file_name)
            image = cv2.imread(path.join(path_to_photos, file_name))
            if image is None and delete_broken:
                remove(path.join(path_to_photos, file_name))
                continue
            cv2.imwrite(
                path.join(path_to_photos, file_name),
                resize_to_square(image),
            )
        else:
            print(f"file type {file_name} is not supported")


