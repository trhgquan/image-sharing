import os
from PIL import Image
from pathlib import Path

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
    
    @staticmethod
    def convert_to_encryptable(img_path):
        '''Convert an image of any type to encryptable type.

        Input:
            - img_path: path to the image
        
        Output:
            - converted image.
        '''

        encryptable_type = '{0}.png'

        filename = os.path.basename(img_path).split('.')[0]

        new_filename = encryptable_type.format(filename)

        with Image.open(img_path) as img:
            img.save(new_filename)

        return new_filename, os.path.basename(img_path)
    
    @staticmethod
    def convert_to_old_extension(img_path, old_filename):
        '''Convert any image to it's old name

        Input:
            - img_path : path to the image
            - old_filename : old filename (with old extension)
        
        Output:
            - New image saved.
        '''
        with Image.open(img_path) as img:
            img.save(old_filename)