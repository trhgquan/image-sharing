from utils import Utils

import requests, auth

class GetImageList:
    def __init__(self, ip = '127.0.0.1', port = '5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)

    def getImages(self, user_id, api_token):        
        url = self.__default_url + '/viewall'
        res = requests.post(url, params = {
            'user_id' : user_id,
            'api_token' : api_token
        })
        res = res.json()
        return res

class GetImageListUI:
    @staticmethod
    def GetImageList_UI():
        Utils.clrscr()
        try:
            res = GetImageList(auth.ip, auth.port).getImages(auth.user_id, auth.api_token)
            if not res['error']:
                numberOfImages = int(res['total_img'])
                if numberOfImages == 0:
                    print('Your image list is empty.')
                else:        
                    print('\n\t\t{0}\'s image list:\n'.format(auth.user_name))
                    print('\tImage ID:\t\t Image Name:\n')
                    
                    for i in range(numberOfImages):
                        img_id, img_name = res['img_list'][i]
                        print('\t',img_id,'\t\t\t', img_name)
            else:
                print(res['message'])
        except Exception as e:
            print('Error: ' + str(e))
        print('\n')
        Utils.pause()