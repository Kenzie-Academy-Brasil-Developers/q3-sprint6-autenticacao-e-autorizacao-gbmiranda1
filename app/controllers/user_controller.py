from datetime import timedelta
import email
from multiprocessing import AuthenticationError
from xml.dom import NotFoundErr
from flask import request, jsonify
from http import HTTPStatus
from app.models.user_model import UserModel
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required


def create_user():
    data = request.get_json()
    keys = ["name", "last_name", "email", "password"]
    wrongKeys = list(data.keys() - keys)

    try: 
        if len(wrongKeys) > 0:
            raise KeyError
        password_hash = data.pop("password")
        data["name"] = data["name"].title()
        data["last_name"] = data["last_name"].title()
        newUser = UserModel(**data)
        newUser.password = password_hash
        db.session.add(newUser)
        db.session.commit()

        return jsonify({
            "name": newUser.name,
            "last_name": newUser.last_name,
            "email": newUser.email
        }), HTTPStatus.CREATED
    except KeyError:
        return jsonify({"error": {"expected_keys": keys, "incoming_keys": wrongKeys}}), HTTPStatus.BAD_REQUEST
    except IntegrityError:
        return {"errror": "email already exists"}, HTTPStatus.CONFLICT


def login_user():
    data = request.get_json()
    try:
        user = UserModel.query.filter_by(email=data["email"]).first()
        if not user:
            raise NotFoundErr 
        if not user.verify_password(data["password"]):
            raise AuthenticationError
        
        user = user.__dict__
        user.pop("_sa_instance_state")

        token = create_access_token(user, expires_delta=timedelta(hours=1))

        return jsonify({"access_token": token}), HTTPStatus.OK
            
    except NotFoundErr:
        return jsonify({"error": "user not found"}), HTTPStatus.NOT_FOUND
    except AuthenticationError: 
        return jsonify({"error": "wrong password"}), HTTPStatus.UNAUTHORIZED 
    
@jwt_required()
def get_users():
    user = get_jwt_identity()
    return jsonify({
        "name": user["name"],
        "last_name": user["last_name"],
        "email": user["email"]
    }), HTTPStatus.OK

@jwt_required()
def delete_user():
    user = get_jwt_identity()
    
    user_delete = UserModel.query.filter_by(email=user["email"]).first()
    db.session.delete(user_delete)
    db.session.commit()
    
    return {'message': f"User {user_delete.name} has been deleted"}, HTTPStatus.OK

@jwt_required()
def update_user():
    data = request.get_json()
    user = UserModel.query.filter_by(email=data["email"]).first()
    password = data.pop("password")

    for key, value in data.items():
        setattr(user, key, value)
    
    user.password = password

    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "name": user.name,
        "last_name": user.last_name,
        "email": user.email
    }), HTTPStatus.OK