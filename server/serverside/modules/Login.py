from flask import request
from flask_restful import Resource
# from .db import get_db
from .Authentication import UserAuthentication

data_error = {
    'error' : True,
    'message' : 'invalid credentials, try again'
}, 500

class Login(Resource):
    def __init__(self):
        self.__UA = UserAuthentication()

    def get_login_id(self):
        user_id = request.args.get('id')
        if user_id == None:
            raise Exception('Missing user_id')
        else:
            return user_id

    def get_verify_token(self):
        verify_token = request.args.get('verify_token')
        if verify_token == None:
            raise Exception('Missing verify_token')
        else:
            return verify_token

    def get(self):
        try:
            user_id = self.get_login_id()

            if not self.__UA.loginable(user_id):
                raise Exception('Invalid user_id')

        except Exception as e:
            print(e)
            return data_error
        
        verify_token = self.__UA.generate_token()

        self.__UA.login_pending(user_id, verify_token)

        return {
            'error' : False,
            'verify_token' : verify_token,
        }, 200

    def post(self):
        try:
            user_id = self.get_login_id()
            verify_token = self.get_verify_token()

            if not self.__UA.check_verify_token(user_id, verify_token):
                raise Exception('Invalid verify_token')

        except Exception as e:
            print(e)
            return data_error

        api_token = self.__UA.login_accepted(user_id)

        return {
            'error' : False,
            'api_token' : api_token,
            'message' : 'login success'
        }, 200
