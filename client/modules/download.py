from modules.getlist import GetImageList
from modules.crypt import RSA, AES
from modules.utils import Utils

import requests, os, shutil
import modules.auth as auth

class Download:
    def __init__(self, ip = '127.0.0.1', port = '5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)

    def getPassphrase(self, api_token, user_id, img_id):
        url = self.__default_url + '/passphrase'
        res = requests.post(url, params = {
            'api_token' : api_token,
            'user_id' : user_id,
            'img_id': img_id
        })
        res = res.json()
        return res

    def imageDownload(self, user_id, img_id, api_token):
        url = self.__default_url + '/download'
        res = requests.post(url, params = {
            'user_id' : user_id,
            'img_id': img_id,
            'api_token' : api_token
        }, stream = True)
        # Create a directory to save
        save_dir = 'downloads'

        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

        ppRes = self.getPassphrase(api_token, user_id, img_id) #ppRes: getPassphrase response
        
        if not ppRes['error']:
            filename = ppRes['real_name']
            passphrase = ppRes['passphrase']
            key_length = ppRes['key_length']

            aesKey = RSA().decrypt(passphrase,auth.private_key,key_length)

            if res.status_code == 200:
                with open('{0}/{1}_{2}'.format(save_dir, img_id, filename), 'wb') as f:
                    res.raw.decode_content = True

                    shutil.copyfileobj(res.raw, f)

                    encryptedImage = '{0}/{1}_{2}'.format(save_dir, img_id, filename)

                    AES().decrypt(encryptedImage, encryptedImage, aesKey)

                    print('Image download success: ', filename)                
            else:
                res = res.json()
                print(res['message'])
        else:
            print(ppRes['message'])

class DownloadUI:
    @staticmethod
    def downloadImage_UI():
        Utils.clrscr()
        try:
            print('<Download Image>\n')
            print('\t1. Download single image')
            print('\t2. Download all image\n')

            ans = int(input('What\'s your choice then? '))
            Utils.clrscr()
            if ans == 1:        
                print('<Download single image>\n')
                img_id = input('Image ID: ')
                Download(auth.ip,auth.port).imageDownload(auth.user_id, img_id, auth.api_token)

            elif ans == 2:
                res = GetImageList(auth.ip, auth.port).getImages(auth.user_id, auth.api_token)
                if not res['error']:
                    numberOfImages = int(res['total_img'])
                    if numberOfImages == 0:
                        print('Your image list is empty.')
                    else:                                
                        for i in range(numberOfImages):
                            img_id,__ = res['img_list'][i]
                            Download(auth.ip,auth.port).imageDownload(auth.user_id, img_id, auth.api_token)
                        print('Download success all image in your image list!')
                else:
                    print(res['message'])
            else:
                raise Exception('Invalid choice.')
        except Exception as e:
            print('Error: ' + str(e))

        Utils.pause()