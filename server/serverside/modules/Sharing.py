from flask import request
from flask_restful import Resource

from .Models.User import UserModel
from .Models.Image import ImageModel

from .Utils import Utils

class Sharing(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = ImageModel()

    def post(self):
        if request.endpoint == 'publickey':
            return self.get_user_public_key()
        if request.endpoint == 'share':
            return self.share_image_to_user()
        return None, 204

    def get_user_public_key(self):
        try:
            author_id = Utils.get_input('author_id')
            guess_id = Utils.get_input('guess_id')
            api_token = Utils.get_input('api_token')

            if not self.__UA.check_api_token(author_id, api_token):
                raise Exception('Permission denied: either author_id or api_token is wrong')
    
            elif not self.__UA.check_user_exist(guess_id):
                raise Exception('Guess not found')
            
            else:
                public_key = self.__UA.get_user_public_key(guess_id)
                return {
                    'error' : False,
                    'public_key' : public_key
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400

    def share_image_to_user(self):
        try:
            author_id = Utils.get_input('author_id')
            guess_id = Utils.get_input('guess_id')
            api_token = Utils.get_input('api_token')
            image_id = Utils.get_input('img_id')
            passphrase = Utils.get_input('passphrase')

            if not self.__UA.check_api_token(author_id, api_token):
                raise Exception('Permission denied: either author_id or api_token is wrong')
            
            elif not self.__im.is_author(author_id, image_id):
                raise Exception('Permission denied: this user is not the author')
            
            elif not self.__im.check_img_exist(author_id, image_id):
                raise Exception('Image not found')
            
            elif self.__im.check_img_exist(guess_id, image_id):
                raise Exception('Already shared')
            
            elif not self.__UA.check_user_exist(guess_id):
                raise Exception('Guess not found')
            
            else:
                self.__im.share_img_to_user(image_id, guess_id, passphrase)

                return {
                    'error' : False,
                    'message' : 'shared successfully'
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 400
