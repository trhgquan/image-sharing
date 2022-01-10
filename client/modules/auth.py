from getpass import getpass
from modules.utils import Utils
from modules.crypt import RSA, PrimeGen

import requests, json

ip, port = None, None
logged_in = False
api_token, private_key = None, None
user_id, user_name = None, None

class Authentication:
    def __init__(self, ip = '127.0.0.1', port = '5000'):
        self.__ip = ip
        self.__port = port
        self.__default_url = 'http://{0}:{1}'.format(self.__ip, self.__port)
    
    def register(self, name, public_key, key_length):
        '''Register a new user.

        Input:
            - name: user name,
            - public_key: user public_key (generated)
            - key_length: user key length (n)

        Output:
            - user id
        
        Exception:
            - thrown if any errors occured.
        '''
        url = self.__default_url + '/register'

        res = requests.post(url, params = {
            'name' : name,
            'public_key' : public_key,
            'key_length' : key_length
        })

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
            key_length = fire_res["key_length"]

            verify_token = RSA.decrypt(verify_token, private_key, key_length)

            confirm_res = requests.post(url, params = {
                'user_id' : user_id,
                'verify_token' : verify_token
            })

            confirm_res = json.loads(confirm_res.text)

            if confirm_res["error"]:
                raise Exception('Wrong credentials')
            else:
                return confirm_res["api_token"], confirm_res["name"]
    
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
        print('\t1. Log in')
        print('\t2. Create a new account')
        print('\t3. Exit')

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
        pg = PrimeGen()        
        Utils.clrscr()

        print('Now we\'ll try to create a new account for you!')
        try:
            name = input('Your name: ')

            print('Choose your public & private pair:')

            while 1:
                p, q = pg.primeGen(16), pg.primeGen(16)

                key_length, public_key, private_key = RSA.generate(p, q)

                print('Key pair: ({0}, {1}), n = {2}'.format(public_key, private_key, key_length))
                ans = input('Accept (y) or generate a new pair (n): ')

                if ans == 'y':
                    break

            user_id = Authentication(ip, port).register(name, public_key, key_length)

        except Exception as e:
            print('Error: ' + str(e))
            Utils.pause()

        else:
            print('Register success, your new id is: {0}'.format(user_id))
            print('\nDo you want to export credentials to {0}/txt? (y/n) '.format(user_id))
            
            ans = input()

            if ans == 'y':
                with open('{0}.txt'.format(user_id), 'w+') as f:
                    print('ID: {0}'.format(user_id), file = f)
                    print('Public_key: {0}'.format(public_key), file = f)
                    print('Private_key: {0}'.format(private_key), file = f)
                print('Successfully exported to {0}.txt'.format(user_id))
            else:
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
        global user_name
        global api_token
        global private_key

        print('Log in with your ID and private_key!')

        try:
            user_id_ = input('Your ID: ')
            private_key_ = getpass('Your private_key: ')

            api_token_, user_name_ = Authentication(ip, port).login(user_id_, private_key_)

        except Exception as e:
            print('Error: Please check your credentials again')
            Utils.pause()

        else:
            api_token = api_token_
            private_key = private_key_
            user_id, user_name = user_id_, user_name_
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
            print('\t1. Yes')
            print('\t2. No')

            ans = int(input('What\'s your choice then? '))
            if ans == 1:
                Authentication(ip, port).logout(user_id, api_token)
            else:
                return False

        except Exception as e:
            print('Error: ' + str(e))

        else:
            private_key, user_id = None, None
            logged_in = False

            print('Logged out success.')
        
        Utils.pause()
