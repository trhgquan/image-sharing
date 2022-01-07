from getpass import getpass
from utils import Utils

import requests
import json
import random

logged_in = False
api_token, private_key = None, None
user_id = None

class Authentication:
    def __init__(self, ip = '127.0.0.1', port = '5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)
    
    def register(self, name, public_key):
        '''Register a new user.

        Input:
            - name: user name,
            - public_key: user public_key (generated)

        Output:
            - user id
        
        Exception:
            - thrown if any errors occured.
        '''
        url = self.__default_url + '/register'

        res = requests.post(
            url.format(self.__ip, self.__port, name, public_key), 
            params = {
                'name' : name,
                'public_key' : public_key
            }
        )

        res = json.loads(res.text)

        if res["error"]:
            raise Exception(res["message"])
        else:
            return res["user_id"]

    def login(self, user_id, private_key):
        '''Log user in.

        Input:
            - user_id : id of the user.
            - private_key: private key of that user.
        
        Output:
            - name: user's name,
            - api_token: user's api token for further actions.
        
        Exception:
        '''
        url = self.__default_url + '/login'

        fire_res =  requests.get(url, params = {
            'user_id' : user_id
        })

        fire_res = json.loads(fire_res.text)

        if fire_res["error"]:
            raise Exception(fire_res["message"])
        else:
            verify_token = fire_res["verify_token"]

            # print('Verify token: {0}'.format(verify_token))

            # verify_token = RSA.decrypt(verify_token, private_key)

            confirm_res = requests.post(url, params = {
                'user_id' : user_id,
                'verify_token' : verify_token
            })

            confirm_res = json.loads(confirm_res.text)

            if confirm_res["error"]:
                # raise Exception(confirm_res["message"])
                raise Exception('Wrong credentials')
            else:
                return confirm_res["api_token"]
    
    def logout(self, user_id, api_token):
        '''Log user out.

        Input:
            - user_id : user's id
            - api_token: user's api_token
        
        Output:
            - message (str)
        
        Exception:
            - thrown if any errors occurred.
        '''
        url = self.__default_url + '/logout'

        res = requests.post(url, params = {
            'user_id' : user_id,
            'api_token' : api_token
        })

        res = json.loads(res.text)

        if res["error"]:
            raise Exception(res["message"])
        else:
            return res["message"]

class AuthenticationUI:
    @staticmethod
    def Menu_UI():
        Utils.clrscr()
        print('Hi, welcome aboard! It seems like you\'re not logged in!')
        print('Now you can:')
        print('1. Log in')
        print('2. Create a new account')
        print('3. Exit')

        try:
            ans = int(input('What\'s your choice then? '))

            if ans == 1:
                AuthenticationUI().Login_UI()
            elif ans == 2:
                AuthenticationUI().Register_UI()
            elif ans == 3:
                print('Goodbye!')
                exit(0)
            else:
                raise Exception('Invalid choice!')
        except Exception as e:
            print('Error: ' + str(e))
            Utils.pause()

    @staticmethod
    def Register_UI():
        Utils.clrscr()
        try:
            name = input('Your name: ')

            public_key = random.randrange(1000, 9999)
            private_key = random.randrange(1000, 9999)

            user_id = Authentication().register(name, public_key)

        except Exception as e:
            print('Error: ' + str(e))
            Utils.pause()

        else:
            print('Register success, your new id is: {0}'.format(user_id))
            print('Remember your credentials:')
            print('ID: {0}'.format(user_id))
            print('Public_key: {0}'.format(public_key))
            print('Private_key: {0}'.format(private_key))
            Utils.pause()

    @staticmethod
    def Login_UI():
        Utils.clrscr()

        global logged_in
        global user_id
        global api_token
        global private_key

        try:
            user_id_ = input('Your ID: ')
            private_key_ = getpass('Your password: ')

            api_token_ = Authentication().login(user_id_, private_key_)

        except Exception as e:
            print('Error: ' + str(e))
            Utils.pause()

        else:
            api_token = api_token_
            private_key = private_key_
            user_id = user_id_
            logged_in = True

            print('Logged in success.')

            Utils.pause()
    
    @staticmethod
    def Logout_UI():
        Utils.clrscr()
    
        global user_id
        global api_token
        global logged_in
        global private_key
    
        try:
            print('Are you sure you want to log out?')
            print('1. Yes')
            print('2. No')

            ans = int(input('What\'s your choice then? '))
            if ans == 1:
                Authentication().logout(user_id, api_token)
            elif ans == 2:
                return False

        except Exception as e:
            print('Error: ' + str(e))

        else:
            private_key, user_id = None, None
            logged_in = False

            print('Logged out success.')
        
        Utils.pause()