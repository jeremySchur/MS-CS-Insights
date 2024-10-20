import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

SLACK_TOKEN = os.getenv("SLACK_TOKEN")  # User token
client = WebClient(token=SLACK_TOKEN)

def update_public_channels(channels):
    """
        Update all public channels
        :param channels: List of channels of form {id, name, last_read_timestamp}
        :return: None
    """
    try:
        response = client.conversations_list(types="public_channel")
        for channel in response['channels']:
            channels[channel['id']] = {"id": channel['id'], 
                                       "name": channel['name'], 
                                       "last_read_timestamp": channels.get(channel['id'], {}).get('last_read_timestamp', 0)}
        # channels = [{"id": channel['id'], "name": channel['name'], "last_read_timestamp": 0} for channel in response['channels']]
        # Filter these by name to get specific course related channels (ask Dustin about naming conventions)
        return None
    except SlackApiError as e:
        print(f"Error fetching channel list: {e.response['error']}")
        return None

def fetch_channel_messages(channel_id, cursor=None, oldest=0, limit=200):
    """
        Fetch messages from a given channel
        :param channel_id: Channel ID to fetch messages from
        :param cursor: Pagination cursor
        :param oldest: Timestamp of the oldest message to fetch
        :param limit: Number of messages to fetch
        :return: Response containing the messages
    """
    return client.conversations_history(
        channel=channel_id,
        cursor=cursor,
        oldest=oldest,
        limit=limit
    )

def fetch_replies(channel_id, thread_ts, cursor=None, limit=200):
    """
        Fetch replies from a given thread
        :param channel_id: Channel ID of the thread
        :param thread_ts: Timestamp of the thread
        :param cursor: Pagination cursor
        :param limit: Number of replies to fetch
        :return: Response containing the replies
    """
    return client.conversations_replies(
        channel=channel_id,
        ts=thread_ts,
        cursor=cursor,
        limit=limit
    )

def process_message(message, channel_id, messages_list):
    """
        Process the message and add it to the messages list
        :param message: Message object
        :param channel_id: Channel ID of the message
        :param messages_list: List to store the messages
        :return: None
    """
    if message.get('type') == 'message' and not message.get('subtype'):
        # If the message has a thread, fetch and add replies
        if 'thread_ts' in message:
            fetch_and_add_replies(channel_id, message['thread_ts'], messages_list)
        # Add the message to the messages list
        messages_list.append({"user": message.get('user', ''),
                              "text": message.get('text', ''),
                              "ts": message.get('ts', '')})

    return None

def fetch_and_add_replies(channel_id, thread_ts, messages_list):
    """
        Fetch and add replies to the messages list
        :param channel_id: Channel ID of the thread
        :param thread_ts: Timestamp of the thread
        :param messages_list: List to store the messages
        :return: None
    """
    reply_cursor = None
    while True:
        replies_response = fetch_replies(channel_id, thread_ts, reply_cursor)
        for reply in reversed(replies_response.get('messages', [])):
            # Skip the first message (original thread message)
            if reply == replies_response.get('messages', [])[0]:
                continue
            if reply.get('type') == 'message' and not reply.get('subtype'):
                messages_list.append({"user": reply.get('user', ''),
                                      "text": reply.get('text', ''),
                                      "ts": reply.get('ts', '')})

        if not replies_response.get('has_more', False):
            break
        reply_cursor = replies_response['response_metadata'].get('next_cursor', None)

    return None

def get_all_messages(channels):
    """
        Get all messages from the specified channels
        :param channel_ids: List of channel IDs to fetch messages from
        :return: Dictionary containing the messages from each channel
    """
    messages = []
    try:
        for channel_id, channel in channels.items():
            prev_len = len(messages)
            cursor = None

            while True:
                response = fetch_channel_messages(
                    channel_id=channel_id,
                    cursor=cursor,
                    oldest=channel.get('last_read_timestamp')
                )

                # Process and store messages
                for message in response.get('messages', []):
                    process_message(message, channel_id, messages)

                # Pagination: break if there's no next cursor
                if not response.get('has_more', False):
                    break
                cursor = response['response_metadata'].get('next_cursor', None)

            # Update the timestamp of the last message fetched
            if prev_len < len(messages):
                channel['last_read_timestamp'] = messages[prev_len]['ts']


    except SlackApiError as e:
        print(f"Error fetching messages from channel {channel_id}: {e.response['error']}")

    return messages
