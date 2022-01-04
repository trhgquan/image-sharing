# Demo cach download file tu server.

import requests
import os
import shutil
import re

# Credentials
user_id = 1 # Thay bang user_id
image_id = 1 # Thay bang image_id
api_token = '391700f4341649854a73917125307fd1' # Thay bang access_token

# Request data
url = 'http://127.0.0.1:5000/download?user_id={0}&img_id={1}&api_token={2}'.format(user_id, image_id, api_token)
headers = {}
payload = {}

# Create a directory to save
save_dir = 'downloads'

if not os.path.isdir(save_dir):
    os.mkdir(save_dir)

# Vi trong response header co san filename,
# dung ham nay lay' cho nhanh.
def get_filename(cd):
    # cd = content-disposition
    if not cd:
        return None
    filename = re.findall('filename=(.+)', cd)

    if len(filename) == 0:
        return None
    return filename[0]

res = requests.post(url, stream = True)

cd = res.headers.get('content-disposition')
filename = get_filename(cd)

if res.status_code == 200:
    # Ten file o day co the thay bang ten da lay trong API call.
    with open('{0}/{1}'.format(save_dir, filename), 'wb') as f:
        res.raw.decode_content = True
        shutil.copyfileobj(res.raw, f)
else:
    print(res.text)
