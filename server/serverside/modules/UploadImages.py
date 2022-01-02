from flask import request
from flask_restful import Resource, reqparse

from .Models.Authentication import UserAuthentication
from .Models.Image import ImageModel

class UploadImages(Resource):
    def __init__(self):
        self.__UA = UserAuthentication()
        self.__im = ImageModel()

    def get_api_token(self):
        api_token = request.args.get('api_token')

        if api_token == None:
            raise Exception('Missing api_token')
        else:
            return api_token

    def get_user_id(self):
        user_id = request.args.get('id')

        if user_id == None:
            raise Exception('Missing user_id')
        else:
            return user_id
    
    def get_passphrase(self):
        passphrase = request.args.get('passphrase')

        if passphrase == None:
            raise Exception('Missing passphrase')
        else:
            return passphrase

    def get_image(self):
        try:
            image_file = request.files['image']

        except Exception:
            raise Exception('No image selected')
        else:
            return image_file

    def post(self):
        try:
            user_id = self.get_user_id()
            api_token = self.get_api_token()
            passphrase = self.get_passphrase()
            
            image = self.get_image()
           
            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')
            
            else:
                new_path, new_img_id = self.__im.save_img_dir(image)
                self.__im.save_img_record(
                    user_id, new_img_id,
                    passphrase, new_path)

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : 'missing credentials'
            }, 500
        else:
            return {
                'error' : False,
                'image_path' : new_path,
                'image_id' : new_img_id,
                'message' : 'upload successful'
            }, 200
