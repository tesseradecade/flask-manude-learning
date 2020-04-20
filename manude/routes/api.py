from flask import request
from manude.models import User
from ..app import app


@app.route("/u/<int:uid>/<token>")
def check_user(uid: int, token: str) -> dict:
    """
    Method returns True if the note with id=uid and token=token exists
    :param uid:
    :param token:
    :return:
    """
    u = User.get_or_none(id=uid, token=token)
    if User.get_or_none(id=uid, token=token):
        if request.args.get("name"):
            u.username = request.args.get("name")
        u.save()
        return {"success": True}
    return {"success": False, "error": "ID or Token is invalid!"}


@app.route("/u/<int:uid>")
def get_user(uid: int) -> dict:
    """
    Method receives open information about the user
    :param uid:
    :return:
    """
    user = User.get_or_none(id=uid)
    if not user:
        return {"success": False, "error": "User Undefined!"}
    s = 0
    for p in User.select():
        s += p.photos
    mean = 100 / s
    return {
        "success": True,
        "photos": {"count": user.photos, "percent": round(mean * user.photos, 2)},
        "name": user.username,
    }
