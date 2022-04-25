from flask import Blueprint

from app.controllers.user_controller import create_user, delete_user, get_users, login_user, update_user

bp_user = Blueprint("bp_user", __name__, url_prefix="/api")

bp_user.post("/signup")(create_user)
bp_user.post("/signin")(login_user)
bp_user.get("")(get_users)
bp_user.put("")(update_user)
bp_user.delete("")(delete_user)