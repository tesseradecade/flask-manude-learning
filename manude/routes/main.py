from flask import render_template, request, redirect, flash, Response
from databases import User, Label
from urllib import parse
from flask_login import current_user, login_user, logout_user, login_required
from ..app import app, images


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

        # Standard match menu
        return render_template("index.html", img=images[current_user.photos], allim=max(images))

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
    :return: 200 or error
    """
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0]
    current_user.ip = ip
    data = parse.parse_qs(request.get_data(as_text=True))

    if "m" in data and "p" in data:
        arg = request.args["m"][0].split("-")
        photo = request.args["p"][0]

        if not photo.isdigit() or not "".join(arg).isdigit():
            return {"error": "m should be specified as a specific schema, p should be integer"}

        arg = list(map(int, arg))

        # noqa
        xmax, xmin = arg[0] + (arg[2] // 2), arg[1] + (arg[3] // 2)
        ymax, ymin = arg[0] - (arg[2] // 2), arg[1] - (arg[3] // 2)

        Label.create(
            photo_id=int(photo),
            user_id=current_user.id,
            label="{},{},{},{}".format(xmin, xmax, ymin, ymax)
        )
        current_user.photos += 1
        current_user.save()
    else:
        return {"error": "Parameters m and p are required"}
    return Response(status=200)


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
