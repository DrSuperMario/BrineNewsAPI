from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token
from modules.admin import AdminModel


_parser = reqparse.RequestParser()
_parser.add_argument('username',
                     type=str,
                     required=True,
                     help="Username field canntot be left blank")

_parser.add_argument('password', 
                     type=str,
                     required=True,
                     help="Password must be added")

_parser.add_argument('email', 
                     type=str,
                     required=True,
                     help="Email must be added")

class AdminRegister(Resource):

    def post(self):
        data = _parser.parse_args()

        if AdminModel.find_by_username(data['username']):
            return {"message": f"{data['username']} is allready taken"}, 400
        elif data['email'] is None:
            return {"message":"you must include email"}, 400
   
        user = AdminModel(**data) 
        user.save_to_db()
        #except:
        #    return {"message":"Something went wrong"}, 500

        
        return {"message":"User created successfully"} ,201

class AdminLogin(Resource):
    @classmethod
    def post(cls):
        data = _parser.parse_args()

        admin = AdminModel.find_by_username(data['username'])

        if admin and safe_str_cmp(admin.password, data['password']):
            access_token = create_access_token(identity=admin.id, fresh=True)
            refresh_token = create_refresh_token(admin.id)

            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            }, 200
            
        return {"message":"Invalid credientals"},401

