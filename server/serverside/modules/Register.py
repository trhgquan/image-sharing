from flask import request
from flask_restful import Resource
from .Models.User import UserModel

data_error = {
    'error' : True,
    'message' : 'invalid data, try again'
}, 500

public_key_error = {
    'error' : True,
    'message' : 'public key existed, try again'
}, 500

success = {
    'error' : False,
    'message' : 'success'
}, 200

class Register(Resource):
    def __init__(self):
        self.__UA = UserModel()

    def get_register_data(self):
        name = request.args.get('name')
        public_key = request.args.get('public_key')

        if name == None or public_key == None:
            raise Exception('Name or public_key is currently empty')
        
        else:
            return name, public_key

    def post(self):
        try:
            name, public_key = self.get_register_data()

        except Exception as e:
            print(e)
            return data_error

        try:
            self.__UA.create_user(name, public_key)
        except Exception as e:
            print(e)
            return public_key_error
        else: 
            return success
