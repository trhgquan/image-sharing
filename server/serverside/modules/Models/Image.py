from flask import current_app
from serverside.db import get_db

import os

class ImageModel:
    def __init__(self):
        self.__db = get_db()

    def create_absolute_image_name(self, img):
        filename = img.filename.split('.')[0]

        new_img_id = str(self.get_total_img() + 1)
        new_filename = img.filename.replace(filename, new_img_id)

        return new_filename, new_img_id

    def save_img_dir(self, img):
        new_name, new_img_id = self.create_absolute_image_name(img)

        if not os.path.isdir(os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])):
            os.mkdir(
                os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'])
            )

        new_path = os.path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], new_name)

        img.save(new_path)

        return new_name, new_img_id

    def save_img_record(self, user_id, img_id, passphrase, location):
        # Add records to image database
        self.__db.execute(
            'INSERT INTO images (id, author_id, location) VALUES (?, ?, ?)',
            (img_id, user_id, location)
        )

        self.__db.execute(
            'INSERT INTO sharing (image_id, user_id, passphrase) VALUES (?, ?, ?)',
            (img_id, user_id, passphrase)
        )

        self.__db.commit()

    def get_total_img(self):
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM images', ())
        
        row = db_exec.fetchone()
        return row[0]
    
    def get_images_of_user(self, user_id):
        db_exec = self.__db.execute(
            'SELECT images.id, images.location FROM images, sharing WHERE images.id = sharing.image_id AND sharing.user_id = ?',
            (user_id)
        )

        rows = db_exec.fetchall()

        return rows

    def get_img_passphrase(self, user_id, img_id):
        db_exec = self.__db.execute(
            'SELECT passphrase FROM sharing WHERE user_id = ? AND image_id = ?',
            (user_id, img_id)
        )

        row = db_exec.fetchone()

        return row[0]

    def check_img_exist(self, user_id, img_id):
        db_exec = self.__db.execute(
            'SELECT COUNT(*) FROM sharing WHERE user_id = ? AND image_id = ?',
            (user_id, img_id)
        )

        row = db_exec.fetchone()

        return row[0] != 0
    
    def get_img_filename(self, user_id, img_id):
        db_exec = self.__db.execute(
            'SELECT images.location FROM images, sharing WHERE sharing.user_id = ? AND sharing.image_id = ? AND sharing.image_id = images.id',
            (user_id, img_id)
        )

        row = db_exec.fetchone()

        return row[0]
