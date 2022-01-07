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
            key_length = Utils.get_input('key_length')

            if self.__UA.check_public_key_exist(public_key, key_length):
                raise Exception('Public_key already used. Please try again')
            else:
                new_id = self.__UA.create_user(name, public_key, key_length)
                return {
                    'error' : False,
                    'user_id' : new_id,
                    'message' : 'account created successfully'
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
