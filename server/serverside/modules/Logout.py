from flask_restful import Resource

from .Models.User import UserModel
from .Utils import Utils

class Logout(Resource):
    def __init__(self):
        self.__UA = UserModel()

    def post(self):
        try:
            user_id = Utils.get_input('user_id')
            api_token = Utils.get_input('api_token')

            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')
            else:
                self.__UA.logout(user_id)
                return {
                    'error' : False,
                    'message' : 'logout success'
                }
        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }
