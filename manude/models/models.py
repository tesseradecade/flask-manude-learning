import peewee
from .database import db
from flask_login import UserMixin


class User(peewee.Model, UserMixin):
    id = peewee.IntegerField(primary_key=True)
    token = peewee.CharField()
    ip = peewee.CharField(null=True)
    photos = peewee.IntegerField(default=0)
    username = peewee.CharField(null=True)

    class Meta:
        database = db


class Label(peewee.Model):
    id = peewee.IntegerField(primary_key=True)
    user_id = peewee.IntegerField()
    photo_id = peewee.IntegerField()
    label = peewee.CharField(50)

    class Meta:
        database = db


models = [User, Label]
