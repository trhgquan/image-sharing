from flask import request
from flask_restful import Resource

from .Models.User import UserModel
from .Models.Image import ImageModel

class Sharing(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = ImageModel()

    def get_author_id(self):
        author_id = request.args.get('author_id')
        if author_id == None:
            raise Exception('Missing author_id')
        else:
            return author_id

    def get_guess_id(self):
        guess_id = request.args.get('guess_id')
        if guess_id == None:
            raise Exception('Missing author_id')
        else:
            return guess_id

    def get_api_token(self):
        api_token = request.args.get('api_token')
        if api_token == None:
            raise Exception('Missing api_token')
        else:
            return api_token

    def get_image_id(self):
        image_id = request.args.get('image_id')
        if image_id == None:
            raise Exception('Missing image_id')
        else:
            return image_id

    def get_passphrase(self):
        passphrase = request.args.get('passphrase')
        if passphrase == None:
            raise Exception('Missing passphrase')
        else:
            return passphrase

    def post(self):
        if request.endpoint == 'publickey':
            return self.get_user_public_key()
        if request.endpoint == 'shareimage':
            return self.share_image_to_user()
        return None, 204

    def get_user_public_key(self):
        try:
            author_id = self.get_author_id()
            guess_id = self.get_guess_id()
            api_token = self.get_api_token()

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
                'messages' : str(e)
            }, 400

    def share_image_to_user(self):
        try:
            api_token = self.get_api_token()
            author_id = self.get_author_id()
            guess_id = self.get_guess_id()
            image_id = self.get_image_id()
            passphrase = self.get_passphrase()

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
                self.__im.share_to_user(guess_id, passphrase)

                return {
                    'error' : False,
                    'message' : 'shared successfully'
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'messages' : str(e)
            }, 400
