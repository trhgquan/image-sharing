from flask import request
from flask_restful import Resource
from .Models.User import UserModel

class Register(Resource):
    def __init__(self):
        self.__UA = UserModel()

    def get_name(self):
        name = request.args.get('name')

        if name == None:
            raise Exception('Missing name')
        else:
            return name

    def get_public_key(self):
        public_key = request.args.get('public_key')

        if public_key == None:
            raise Exception('Missing public_key')
        else:
            return public_key

    def post(self):
        try:
            name = self.get_name()
            public_key = self.get_public_key()
            new_id = self.__UA.create_user(name, public_key)
        except Exception as e:
            print(e)
            return {
                'error' : True,
                'messages' : str(e)
            }, 400
        else: 
            return {
                'error' : False,
                'id' : new_id,
                'message' : 'account created successfully'
            }, 200
