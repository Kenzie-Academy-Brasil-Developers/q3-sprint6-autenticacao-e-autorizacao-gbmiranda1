from flask import Flask 
from app.routes.user_route import bp_user

def init_app(app):
	app.register_blueprint(bp_user)