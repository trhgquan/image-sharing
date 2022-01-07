from flask_restful import Resource

from .Models.User import UserModel
from .Utils import Utils

class Login(Resource):
    def __init__(self):
        self.__UA = UserModel()

    def get(self):
        try:
            user_id = Utils.get_input('user_id')

            if not self.__UA.loginable(user_id):
                raise Exception('Invalid user_id')

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }
        
        verify_token = self.__UA.generate_token()

        self.__UA.login_pending(user_id, verify_token)

        return {
            'error' : False,
            'verify_token' : verify_token,
        }, 200

    def post(self):
        try:
            user_id = Utils.get_input('user_id')
            verify_token = Utils.get_input('verify_token')

            if not self.__UA.check_verify_token(user_id, verify_token):
                raise Exception('Invalid verify_token')

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400

        api_token = self.__UA.login_accepted(user_id)
        user_name = self.__UA.get_user_name(user_id)

        return {
            'error' : False,
            'api_token' : api_token,
            'name' : user_name,
            'message' : 'login success'
        }, 200
