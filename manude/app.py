from flask import Flask
from flask_login import LoginManager
from .models.models import User


app = Flask(__name__)
login = LoginManager(app)

@login.user_loader
def load_user(uid: int):
    return User.get_or_none(id=uid)
