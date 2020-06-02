from flask import render_template, request, redirect, flash, Response, Request, jsonify
from manude.models import User, Label
from urllib import parse
from flask_login import current_user, login_user, logout_user, login_required
from ..app import app, login
import os, json


request: Request
images = [
    int(image.replace(".jpg", ""))
    for image in os.listdir(app.config.get("image_dir", "."))
    if not image.startswith(".")
]


@app.route("/")
def index():
    """
    Manage manude matches and login users
    :return:
    """
    if current_user.is_authenticated:
        ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0]
        current_user.ip = ip

        if len(images) <= current_user.photos:
            flash("Photos are all completed. See you later")
            logout_user()
            return render_template("token.html")
        elif request.query_string == b"bf":
            flash(f"You marked {current_user.photos} as a bad photo (skipped)")
            current_user.photos += 1

        current_user.save()
        # Standard match menu
        return render_template(
            "index.html", img=images[current_user.photos], allim=max(images)
        )

    elif request.args.get("token"):
        user = User.get_or_none(token=request.args["token"])
        if user:
            login_user(user, remember=True)
            return redirect("/")
        flash("[ACCESS FAILED] Invalid token")

    # Login menu
    return render_template("token.html")


@app.route("/take", methods=["POST"])
@login_required
def take():
    """
    Method takes all the incoming data from the fetching request after the user's match
    :return: json
    """
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0]
    current_user.ip = ip
    data = json.loads(request.data)

    if "m" in data and "p" in data:
        arg = data["m"].split("-")
        photo = data["p"]

        if not isinstance(photo, int) or not "".join(arg).isdigit():
            print("error")
            return jsonify(
                {
                    "error": "m should be specified as a specific schema, p should be integer"
                }
            )

        arg = list(map(int, arg))

        # noqa
        xmin, ymin, xmax, ymax = arg

        Label.create(
            photo_id=photo,
            user_id=current_user.id,
            label="{},{},{},{}".format(xmin, xmax, ymin, ymax),
        )
        current_user.photos += 1
        current_user.save()
        return jsonify({"success": True})
    else:
        return jsonify({"error": "Parameters m and p are required"})


@app.route("/logout")
@login_required
def logout():
    """
    Logout users [force]
    :return:
    """
    logout_user()
    flash("You was logged out")
    return redirect("/")


@login.unauthorized_handler
def go_login():
    flash("You should login to access this page")
    return redirect("/")
