# from telethon import TelegramClient, events, sync
import asyncio

from helpers import ( get_config_attributes, separate_grouped_messages )
from api import ( get_connection, get_posts, get_entity_attrs, download_media_from_message )
from remote_server import ( get_telegram_channels, upload_to_laravel )




# login to telegram (done) 
# fetch all profiles from vindex (done)
# for each profile
    # download messages
    # for each messages
        # download media
        # upload to vindex
        # attach to messages
    # send messages to vindex

'''
Get Config Attributes
'''
args = get_config_attributes()


'''
Fill API Keys
'''
sfile = 'session_file'
api_id = args['api_id']
api_hash = args['api_hash']
phone = args['phone']


def main():
    loop = asyncio.get_event_loop()

    # login to telegram
    client = loop.run_until_complete(
        get_connection(sfile, api_id, api_hash, phone)
    )

    # get telegram channels to scrape
    channels = get_telegram_channels()

    if channels != None:
        for channel in channels:
            entity_attrs = loop.run_until_complete(
                get_entity_attrs(client, channel["username"])
            )
            
            if entity_attrs:
                # Get channel id
                channel_id = entity_attrs.id

                # check if already scrapped before
                if channel["latest_social_media_post"]:
                    # scrape from min id
                    posts = loop.run_until_complete(
                        get_posts(client, channel_id, min_id=int(channel['latest_social_media_post']['platform_id']))
                    )
                else :
                    posts = loop.run_until_complete(
                        get_posts(client, channel_id)
                    )
                
                data = posts.to_dict()
                # separate grouped messages from single messages
                grouped_messages, single_messages = separate_grouped_messages(posts.messages)
                
                for grouped_message in grouped_messages.values():
                    laravel_dict = {
                        "platform_id": None,
                        "message": None,
                        "date_sent": None,
                        "date_edited": None,
                        "channel_name": None,
                        "grouped_id": None,
                        "media": []
                    }
                    for message in grouped_message:
                        if message.message != "":
                            laravel_dict["platform_id"] = message.id
                            laravel_dict["message"] = message.message
                            laravel_dict["date_sent"] = message.date.timestamp()
                            laravel_dict["date_edited"] = message.edit_date.timestamp()
                            laravel_dict["grouped_id"] = message.grouped_id
                            laravel_dict["channel_name"] = channel["username"]
                        
                        laravel_dict["media"].append(loop.run_until_complete(download_media_from_message(client, message)))

                    print(laravel_dict)
                    # send this to the server to be stored
                    upload_to_laravel(laravel_dict)
                    return None
                # loop through grouped messages
                    # download each media
                    # group media and message and send to laravel server to be stored run ml server
                
                for single_message in single_messages:
                    laravel_dict = {
                        "platform_id": None,
                        "message": None,
                        "date_sent": None,
                        "date_edited": None,
                        "channel_name": None,
                        "grouped_id": None,
                        "media": []
                    }

                    laravel_dict["platform_id"] = single_message.id
                    laravel_dict["message"] = single_message.message
                    laravel_dict["date_sent"] = single_message.date.timestamp()
                    laravel_dict["date_edited"] = single_message.edit_date.timestamp()
                    laravel_dict["grouped_id"] = single_message.grouped_id
                    laravel_dict["channel_name"] = channel["username"]
                    laravel_dict["media"].append(loop.run_until_complete(download_media_from_message(client, single_message)))

                

main()