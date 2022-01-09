from utils import Utils
from crypt import RSA, AES

import auth, requests, json

class UploadImage:
    def __init__(self, ip = '127.0.0.1', port = '5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)
        self.__aes = AES()

    def get_public_key(self):
        url = self.__default_url + '/publickey'

        response = requests.post(url, params = {
            'author_id' : auth.user_id,
            'guess_id' : auth.user_id,
            'api_token' : auth.api_token
        })

        response = json.loads(response.text)

        if response["error"]:
            raise Exception(response["error"])
        else:
            return response["public_key"], response["key_length"]

    def upload_image(self, image_path):
        url = self.__default_url + '/upload'
        
        encrypted_file, real_name, key = self.__aes.encrypt(image_path)

        print(encrypted_file, real_name, key)

        public_key, key_length = self.get_public_key()

        key = RSA.encrypt(key, public_key, key_length)

        files=[('image', (encrypted_file, open(encrypted_file, 'rb'), 'image/png'))]

        response = requests.post(url, params = {
            'user_id' : auth.user_id,
            'api_token' : auth.api_token,
            'passphrase' : key,
            'real_name' : real_name
        }, files = files)

        response = json.loads(response.text)

        if response["error"]:
            raise Exception(response["message"])
        else:
            return response["message"]

class UploadUI:
    @staticmethod
    def main():
        Utils.clrscr()
        print('Upload a new file to server!')
        try:
           image_path = input("Path to the image: ")
           upload_status = UploadImage().upload_image(image_path)
        except Exception as e:
            print('Error: ' + str(e))
        else:
            print(upload_status)
            
        Utils.pause()