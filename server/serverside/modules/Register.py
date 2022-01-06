from flask_restful import Resource

from .Models.User import UserModel
from .Utils import Utils

class Register(Resource):
    def __init__(self):
        self.__UA = UserModel()

    def post(self):
        try:
            name = Utils.get_input('name')
            public_key = Utils.get_input('public_key')
            new_id = self.__UA.create_user(name, public_key)
        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
        else: 
            return {
                'error' : False,
                'user_id' : new_id,
                'message' : 'account created successfully'
            }, 200
