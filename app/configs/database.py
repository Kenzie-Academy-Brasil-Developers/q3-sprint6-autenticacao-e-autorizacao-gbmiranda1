from operator import imod
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from os import getenv

db = SQLAlchemy()

def init_app(app):
    
    app.config["SQLALCHEMY_DATABASE_URI"] = getenv("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.db = db

    from app.models.user_model import UserModel
