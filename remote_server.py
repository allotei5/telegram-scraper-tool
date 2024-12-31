import requests
import os

from helpers import ( get_config_attributes )

args = get_config_attributes()
url = args["laravel_api"]

def get_telegram_channels():
    '''
    Fetches telegram channels from my laravel server
    '''
    func_url = f"{url}get-telegram-channels"
    payload = ""
    headers = {}

    print('> getting channels')

    # make request
    response = requests.request("GET", func_url, headers=headers, data=payload)

    if response.status_code == 200:
        print('> got channels')
        channels = response.json()

        return channels
    
    else:
        print('error')
        return None
    
def upload_to_laravel(payload):
    '''
    Uploads to my laravel server
    '''
    func_url = f"{url}save-social-media-post"
    files = [ 
        ('media_files[]', (os.path.basename(file), open(file, 'rb'))) 
        for file in payload['media'] 
        if file is not None
    ]
    print(files)

    response = requests.post(func_url, data=payload, files=files)
    if response.status_code == 200:
        print("Successfully uploaded message and media files")
    else:
        print("Failed to upload message and media files")