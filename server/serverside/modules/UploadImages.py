from flask import request
from flask_restful import Resource, reqparse

from .Models.User import UserModel
from .Models.Image import ImageModel

from .Utils import Utils
import os

class UploadImages(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = ImageModel()
        self.ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    def get_image(self):
        try:
            image_file = request.files['image']

        except Exception:
            raise Exception('No image selected')
        else:
            _, extension = os.path.splitext(image_file.filename.lower())

            if extension not in self.ALLOWED_EXTENSIONS:
                raise Exception('Extension not allowed')

            else:
                return image_file

    def post(self):
        try:
            user_id = Utils.get_input('user_id')
            api_token = Utils.get_input('api_token')
            passphrase = Utils.get_input('passphrase')

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
                'message' : str(e)
            }, 400
        else:
            return {
                'error' : False,
                'image_filename' : new_path,
                'image_id' : new_img_id,
                'message' : 'upload successful'
            }, 200
