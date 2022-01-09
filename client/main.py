from auth import AuthenticationUI
from upload import UploadUI
from utils import Utils
import auth

def main(): 
    auth.ip = input('Server IP: ')
    auth.port = input('Port: ')

    while 1:
        if not auth.logged_in:
            AuthenticationUI.Menu_UI()
        else:
            # This should be placed inside a class named MainUI?
            Utils.clrscr()
            print('Hello {0}'.format(auth.user_name))
            print('Your current choice is: ')
            print('1. Log out')
            print('2. Upload a new image to server')

            try:
                ans = int(input('Your choice: '))

                if ans == 1:
                    AuthenticationUI.Logout_UI()
                elif ans == 2:
                    UploadUI.main()
                else:
                    raise Exception('Invalid choice')
            except Exception as e:
                print('Error: ' + str(e))
                Utils.pause()
            

if __name__ == '__main__':
    main()