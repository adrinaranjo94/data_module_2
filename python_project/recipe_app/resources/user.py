from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models import User  # Definiremos este modelo en models.py para almacenar usuarios

# Parseador de solicitudes para el registro
user_parser = reqparse.RequestParser()
user_parser.add_argument('username', required=True, help="El nombre de usuario es obligatorio")
user_parser.add_argument('password', required=True, help="La contraseña es obligatoria")
user_parser.add_argument('role', choices=('admin', 'user', 'everyone'), help="Rol debe ser admin, user, o everyone")

class Register(Resource):
    def post(self):
        data = user_parser.parse_args()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        
        new_user = User(username=data['username'], password=hashed_password, role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({"message": "Usuario registrado exitosamente"})

class Login(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"message": "Credenciales incorrectas"}), 401
        
        access_token = create_access_token(identity={"username": user.username, "role": user.role})
        return jsonify(access_token=access_token)

class UserProfile(Resource):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user)
