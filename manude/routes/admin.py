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
        "admin_key.html",
        users=User.select(),
        labels=Label.select(),
    )


@app.route("/remove_label/<int:label_id>")
@login_required
def panel(label_id: int):
    if not current_user.is_admin:
        flash("You have no admin permission")
        return redirect("/")
    label = Label.get_or_none(id=label_id)
    if label is None:
        return {"error": "not found"}
    await label.delete()
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
    return render_template(
        "photo.html",
        path=static_image_path,
    )
