# Demo cach download file tu server.

import requests
import os
import shutil

# Credentials
user_id = 1 # Thay bang user_id
image_id = 1 # Thay bang image_id
api_token = 'eb2955a18bb2ddd8a04db5771fdbed2b' # Thay bang access_token

# Request data
url = 'http://127.0.0.1:5000/download?user_id={0}&img_id={1}&api_token={2}'.format(user_id, image_id, api_token)
headers = {}
payload = {}

# Create a directory to save
save_dir = 'downloads'

if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

print(url)

res = requests.post(url, stream = True)

if res.status_code == 200:
    # Ten file o day co the thay bang ten da lay trong API call.
    with open(save_dir + '/test.jpg', 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
else:
    print(res.text)
