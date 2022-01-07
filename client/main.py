from auth import AuthenticationUI
from utils import Utils
import auth

def main():
    while 1:
        if not auth.logged_in:
            AuthenticationUI.Menu_UI()
        else:
            # This should be placed inside a class named MainUI?
            Utils.clrscr()
            print('Hello {0}'.format(auth.user_id))
            print('Your current choice is: ')
            print('1. Log out')

            try:
                ans = int(input('Your choice: '))

                if ans == 1:
                    AuthenticationUI.Logout_UI()
                else:
                    raise Exception('Invalid choice')
            except Exception as e:
                print('Error: ' + str(e))
                Utils.pause()
            

if __name__ == '__main__':
    main()