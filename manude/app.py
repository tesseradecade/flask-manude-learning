from flask import Flask
from flask_login import LoginManager
from .models.models import User
import os


app = Flask(__name__)
login = LoginManager(app)
images = [
    int(image.replace(".jpg", ""))
    for image in os.listdir("static/imgs/")
    if not image.startswith(".")
]

@login.user_loader
def load_user(uid: int):
    return User.get_or_none(id=uid)
