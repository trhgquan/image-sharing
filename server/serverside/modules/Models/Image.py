from flask import current_app
from serverside.db import get_db

import os

class ImageModel:
    def __init__(self):
        self.__db = get_db()

    def create_absolute_image_name(self, img):
        '''Create an absolute name for image.

        Input:
            - img : image
        
        Output:
            - new_filename : new image name (to store on server)
            - new_img_id : new ID
        '''
        filename = img.filename.split('.')[0]

        new_img_id = str(self.get_total_img() + 1)
        new_filename = img.filename.replace(filename, new_img_id)

        return new_filename, new_img_id

    def save_img_dir(self, img):
        '''Save image to directory (default in UPLOAD_FOLDER)

        Input:
            - img : image to save
        
        Output:
            - new_name : image name on server
            - new_img_id : image id
        '''
        new_name, new_img_id = self.create_absolute_image_name(img)

        if not os.path.isdir(os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])):
            os.mkdir(
                os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            )

        new_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], new_name)

        img.save(new_path)

        return new_name, new_img_id

    def save_img_record(self, user_id, img_id, passphrase, location, real_name, checksum):
        '''Adding records to image database.

        Input:
            - user_id
            - img_id
            - passphrase : Encrypted with RSA
            - location : Filename stored on server.
            - real_name : Original filename when uploaded.
            - checksum : Checksum
        '''
        # Add records to image database
        self.__db.execute(
            'INSERT INTO images (id, author_id, location, real_name, checksum) VALUES (?, ?, ?, ?, ?)',
            (img_id, user_id, location, real_name, checksum)
        )

        self.__db.commit()

        self.share_img_to_user(img_id, user_id, passphrase)

    def share_img_to_user(self, img_id, user_id, passphrase):
        '''Adding records to share to other user.

        Input:
            - img_id
            - user_id : ID to share
            - passphrase : new passphrase (Encrypted with RSA)
        '''
        self.__db.execute(
            'INSERT INTO sharing (image_id, user_id, passphrase) VALUES (?, ?, ?)',
            (img_id, user_id, passphrase)
        )

        self.__db.commit()

    def get_total_img(self):
        '''Count total images on server.

        Output:
            - total_images
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM images', ())
        
        row = db_exec.fetchone()
        return row[0]
    
    def get_images_of_user(self, user_id):
        '''Get images of user.

        Input:
            - user_id

        Output:
            - Many rows, each row has this format:
                - image_id : ID of the file on server.
                - image_real_name : Original filename
        '''
        db_exec = self.__db.execute(
            'SELECT images.id, images.real_name FROM images, sharing WHERE images.id = sharing.image_id AND sharing.user_id = ?',
            (user_id,)
        )

        rows = db_exec.fetchall()

        return rows

    def get_img_passphrase(self, user_id, img_id):
        '''Get image passphrase (for AES decryption)

        Input:
            - user_id : ID of the user who can download img_id
            - img_id : ID of the image.

        Output:
            - passphrase : Image passphrase to decrypt.
        '''
        db_exec = self.__db.execute(
            'SELECT passphrase FROM sharing WHERE user_id = ? AND image_id = ?',
            (user_id, img_id)
        )

        row = db_exec.fetchone()

        return row[0]
    
    def get_img_checksum(self, img_id):
        '''Get image checksum info

        Input:
            - img_id : ID of the image

        Output:
            - author_id : Author ID
            - image_checksum : Image checksum
        '''

        db_exec = self.__db.execute(
            'SELECT author_id, checksum FROM images WHERE id = ?',
            (img_id,)
        )

        row = db_exec.fetchone()

        return row[0], row[1]

    def check_img_exist(self, user_id, img_id):
        '''Check if img_id exist (aka user_id has permissions with it).

        Input:
            - user_id : ID of user
            - img_id : ID of image
        
        Return:
            - True if user has the right with it, False otherwise.
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM sharing WHERE user_id = ? AND image_id = ?',
            (user_id, img_id)
        )

        row = db_exec.fetchone()

        return row[0] != 0
    
    def get_img_filename(self, user_id, img_id):
        '''Get image filename (for download)

        Input:
            - user_id : User ID (has permissions)
            - img_id : Image ID

        Return:
            - image_location : Filename on server
            - image_realname : Original file name
        '''
        db_exec = self.__db.execute(
            'SELECT images.location, images.real_name FROM images, sharing WHERE sharing.user_id = ? AND sharing.image_id = ? AND sharing.image_id = images.id',
            (user_id, img_id)
        )

        row = db_exec.fetchone()

        return row[0], row[1]
    
    def is_author(self, user_id, img_id):
        '''Check if user is author (the-one-who-uploaded) of the image.

        Input:
            - user_id : ID of the author (to check)
            - img_id : ID of the image

        Return:
            - True if user is the author, False otherwise
        '''
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM images WHERE id = ? AND author_id = ?',
            (img_id, user_id)
        )

        row = db_exec.fetchone()
        
        return row[0] == 1
