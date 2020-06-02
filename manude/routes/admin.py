from flask import request, jsonify
from manude.models import User, Label
from flask import render_template, flash, redirect
from flask_login import login_required, current_user
from ..app import app
from ..util import make_preview, calculate_static


@app.route("/admin")
@login_required
def panel():
    if not current_user.is_admin:
        flash("You have no admin permission")
        return redirect("/")
    return render_template(
        "admin_key.html", users=User.select(), labels=Label.select(),
    )


@app.route("/remove_label/<int:label_id>")
@login_required
def rm_label(label_id: int):
    if not current_user.is_admin:
        flash("You have no admin permission")
        return redirect("/")
    label = Label.get_or_none(id=label_id)
    if label is None:
        return {"error": "not found"}
    label.delete_instance()
    return {"success": True}


@app.route("/remove_user/<int:user_id>")
@login_required
def rm_user(user_id: int):
    if not current_user.is_admin:
        flash("You have no admin permission")
        return redirect("/")
    user = User.get_or_none(id=user_id)
    if user is None:
        return {"error": "not found"}
    elif user.is_admin:
        return {"error": "user is admin"}
    user.delete_instance()
    return {"success": True}


@app.route("/make_admin/<int:user_id>")
@login_required
def mk_admin(user_id: int):
    if not current_user.is_admin:
        flash("You have no admin permission")
        return redirect("/")
    user = User.get_or_none(id=user_id)
    if user is None:
        return {"error": "not found"}
    user.is_admin = True
    user.save()
    return {"success": True}


@app.route("/label/<int:label_id>")
def preview_label(label_id: int):
    """
    if not current_user.is_admin:
        flash("You have no admin permission")
        return redirect("/")
    """
    label = Label.get_or_none(id=label_id)
    if not label:
        return "This label is undefined"
    abs_image_path = make_preview(label.photo_id, *map(int, label.label.split(",")))
    if abs_image_path is False:
        return "Requirements are not satisfied, see logs"
    static_image_path = calculate_static(abs_image_path)
    if request.args.get("only_path"):
        return jsonify({"path": static_image_path})
    return render_template("photo.html", path=static_image_path,)
