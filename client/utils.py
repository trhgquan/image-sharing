import os

class Utils:
    @staticmethod
    def clrscr():
        '''Clear the screen
        '''
        os.system('clear') if os.name == 'posix' else os.system('cls')
    
    @staticmethod
    def pause():
        '''Pause the screen before clearing
        '''
        input('Press any key to continue..')