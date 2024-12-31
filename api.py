from telethon import TelegramClient, types
from telethon.tl.functions.channels import GetChannelsRequest, \
	GetFullChannelRequest, GetParticipantsRequest
from telethon.tl.functions.messages import GetHistoryRequest, \
	GetDiscussionMessageRequest, GetWebPageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.photos import GetUserPhotosRequest
from telethon.tl.functions.stats import GetBroadcastStatsRequest

import os
from datetime import datetime

# get connection
async def get_connection(session_file, api_id, api_hash, phone):
    '''
    Connects to Telegram API
    '''

    client = TelegramClient(session_file, api_id, api_hash)
    await client.connect()
    if await client.is_user_authorized():
        print('> Authorized!')
    else:
        print('> Not Authorized! Sending code request...')
        await client.send_code_request(phone)
        await client.sign_in(
            phone,
            input('Enter the code: ')
        )
    
    return client

async def get_posts(client, source, min_id=0, offset_id=0, offset_date=0):
    '''
    Fetches 1000 posts from the channel
    '''
    return await client(
        GetHistoryRequest(
            peer=source,
            hash=0,
            limit=1000,
            max_id=0,
            min_id=min_id,
            offset_id=offset_id,
            add_offset=0,
            offset_date=offset_date
        )
    )

# get telegram channel main attrs
async def get_entity_attrs(client, source):
    try:
        value = await client.get_entity(source)
    except ValueError:
        value = False
    
    return value

async def download_media_from_message(client, message):
    allowed_size = 50 * 1024 * 1024
    if message.media:
        print('here')
        filename = f"{message.id}_"
        # file_extension = get_file_extension
       
        if message.document:
            size = message.document.size
            if size < allowed_size:
                file_path = await client.download_media(message, file=f"downloads/{filename}")
                return file_path
            else:
                return None
            
        file_path = await client.download_media(message, file=f"downloads/{filename}")
        return file_path