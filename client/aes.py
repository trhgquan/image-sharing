import cv2
import numpy as np
from Crypto.Cipher import AES
from PIL import Image
import secrets 
import base64

class crypt_AES(object):

    def __init__(self):
        self.key = self.genKey()
        self.iv = b'0000000000000000'

    @staticmethod
    def getFilename(file_path):   #lay ten file tu duong dan VD: C:\\..\\filename
        return file_path[file_path.rfind("\\") + 1:]
    @staticmethod
    def genKey():
        return secrets.token_hex(8)

    def convertToPNG(self,file_path): #doi ten sang .png
        filename = self.getFilename(file_path)

        if ".png" in filename:
            Image.open(file_path).save(filename)
            return filename
        tmp = filename.split(".")
        new_filename = tmp[0] + ".png"
        Image.open(file_path).save(new_filename)
        return new_filename
    def encryptImage(self,file_path):
        filename = self.convertToPNG(file_path)
        encrypted_image = "encrypted_" + filename
        img = cv2.imread(filename)
        if img.size % 16 > 0:
            row = img.shape[0]
            pad = 16 - (row % 16)  # Number of rows to pad (4 rows)
            img = np.pad(img, ((0, pad), (0, 0), (0, 0)))  # Pad rows at the bottom  - new shape is (304, 451, 3) - 411312 bytes.
            img[-1, -1, 0] = pad  # Store the pad value in the last element4
        img_bytes = img.tobytes()
        enc_img_bytes = AES.new(self.key.encode(), AES.MODE_CBC, self.iv).encrypt(img_bytes)  # Encrypt the array of bytes.

        # Convert the encrypted buffer to NumPy array and reshape to the shape of the padded image (304, 451, 3)
        enc_img = np.frombuffer(enc_img_bytes, np.uint8).reshape(img.shape)

        #Save the image - Save in PNG format because PNG is lossless (JPEG format is not going to work).
        cv2.imwrite(encrypted_image, enc_img)
        return encrypted_image, filename, self.key
    
    def decryptImage(self,encrypted_image,filename,key):
        decrypted_image = filename
        enc_img = cv2.imread(encrypted_image)
        dec_img_bytes = AES.new(key.encode(), AES.MODE_CBC, self.iv).decrypt(enc_img.tobytes())

        dec_img = np.frombuffer(dec_img_bytes, np.uint8).reshape(enc_img.shape)  # The shape of the encrypted and decrypted image is the same (304, 451, 3)

        pad = int(dec_img[-1, -1, 0])  # Get the stored padding value   

        dec_img = dec_img[0:-pad, :, :].copy() 
        cv2.imwrite(decrypted_image, dec_img)
        return decrypted_image