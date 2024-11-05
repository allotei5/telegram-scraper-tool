from configparser import ConfigParser

# get config attributes
def get_config_attributes():
    path = './config/config.ini'

    # config parser
    config = ConfigParser()
    config.read(path)

    # telegram api credentials
    attributes = config['Telegram API credentials']
    return dict(attributes)

def make_social_media_post_dict(platform_id, message, date_sent, date_edited, channel_name, event_type_id):
    return {
        "platform_id": platform_id,
        "message": message,
        "date_sent": date_sent,
        "date_edited": date_edited,
        "channel_name": channel_name,
        "event_type_id": event_type_id
    }

def separate_grouped_messages(messages):
    # loop through the messages to group them by grouped_id
    sorted_messages = {
        "grouped_messages" : [],
        "single_messages" : []
    }
    grouped_messages = {}
    single_messages = []
    for message in messages:
        if message.grouped_id:
            if message.grouped_id not in grouped_messages:
                grouped_messages[message.grouped_id] = []
            grouped_messages[message.grouped_id].append(message)
        else:
            # is a single message
            single_messages.append(message)
    return grouped_messages, single_messages
    return {
        "grouped_messages" : grouped_messages,
        "single_messages": single_messages
    }

