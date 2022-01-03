from flask import request
from flask_restful import Resource

from .Models.Image import ImageModel
from .Models.User import UserModel

import os

class DownloadImages(Resource):
    def __init__(self):
        self.__UA = UserModel()
        self.__im = ImageModel()
    
    def get_api_token(self):
        api_token = request.args.get('api_token')

        if api_token == None:
            raise Exception('Missing api_token')
        else:
            return api_token

    def get_user_id(self):
        user_id = request.args.get('user_id')

        if user_id == None:
            raise Exception('Missing user_id')
        else:
            return user_id

    def get_image_id(self):
        image_id = request.args.get('img_id')

        if image_id == None:
            raise Exception('Missing img_id')
        else:
            return image_id

    def get(self):
        if request.endpoint == 'viewall':
            return self.user_images()
        if request.endpoint == 'passphrase':
            return self.image_passphrase()
        return None, 204

    def user_images(self):
        try:
            user_id = self.get_user_id()
            api_token = self.get_api_token()
            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')
            
            else:
                img_list = []
                for row in self.__im.get_images_of_user(user_id):
                    _, filename = os.path.split(row[1])
                    img_list.append((row[0], filename))
        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }, 500
        else:
            return {
                'error' : False,
                'total_img' : len(img_list),
                'img_list' : img_list,
                'message' : 'request successful'
            }, 200

    def image_passphrase(self):
        try:
            img_id = self.get_image_id()
            user_id = self.get_user_id()
            api_token = self.get_api_token()

            if not self.__UA.check_api_token(user_id, api_token):
                raise Exception('Permission denied: either user_id or api_token is wrong')

            elif not self.__im.check_img_exist(user_id, img_id):
                raise Exception('Image not found')
            
            else:
                passphrase = self.__im.get_img_passphrase(user_id, img_id)

                return {
                    'error' : False,
                    'passphrase' : passphrase
                }, 200

        except Exception as e:
            print(e)
            return {
                'error' : True,
                'message' : str(e)
            }
