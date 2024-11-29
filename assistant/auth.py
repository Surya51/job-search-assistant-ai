import functools
from flask import Blueprint, jsonify, request, session
from flask_cors import CORS
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from assistant.db import add_user, get_user_by_username
from assistant.jwt import create_jwt, decode_jwt

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

CORS(auth_bp)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")

    error = None

    if not username:
        error = "Username is required."
    elif not password:
        error = "Password is required."

    if error is None:
        try:
            add_user(name, username.lower(), generate_password_hash(password))
        except Exception as e:
            error = f"User {username} is already registered."
            return jsonify({
                'success': False,
                'error': error
            }), 400
        else:
            return jsonify({
                'success': True,
                'error': None
            }), 200
        
    else:
        return jsonify({
            'success': False,
            'error': error
        }), 400


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    error = None

    if username is not None and password is not None:
        user = get_user_by_username(username.lower())

    if user is None:
        error = "Incorrect Username / Username doesn't exist."
    
    elif not check_password_hash(user["password"], password):
        error = 'Incorrect Password.'

    if error is None:
        session.clear()
        session["user_guid"] = user["guid"]
        jwt = create_jwt(user)
        return jsonify({
            'token': jwt,
            'success': True,
            'error': None
        }), 200
    else:
        return jsonify({
            'token': None,
            'success': False,
            'error': error
        }), 401

@auth_bp.route("/logout")
def logout():
    session.clear()
    return jsonify({
        'loggedOut': True
    }), 200

@auth_bp.route('/validate', methods=["GET"])
def isAuthorized():
    token = request.headers.get('Authorization')
    return decode_jwt(token)