import os
import re
import asyncio
from slack_sdk import WebClient
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
from postgres import insert_channel

SLACK_TOKEN = os.getenv("SLACK_TOKEN")  # User token
# client = WebClient(token=SLACK_TOKEN)
client = AsyncWebClient(token=SLACK_TOKEN)
CHANNEL_REGEX = r'^csca\d{4}$'

def update_public_channels(channels):
    """
        Update all public channels
        :param channels: List of channels of form {id, name, last_read_timestamp}
        :return: None
    """
    try:
        response = asyncio.run(client.conversations_list(types="public_channel"))
        for channel in response['channels']:
            if channel['id'] not in channels and re.search(CHANNEL_REGEX, channel['name']):
                insert_channel(channel['id'], channel['name'])
                channels[channel['id']] = {"name": channel['name']}
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
        :return: promise for response containing the messages
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
        :return: promise for response containing the replies
    """
    return client.conversations_replies(
        channel=channel_id,
        ts=thread_ts,
        cursor=cursor,
        limit=limit
    )

async def process_message(message, channel_id, messages_list):
    """
        Process the message and add it to the messages list
        :param message: Message object
        :param channel_id: Channel ID of the message
        :param messages_list: List to store the messages
        :return: None
    """
    if message.get('type') == 'message' and not message.get('subtype'):
        # Add the message to the messages list
        messages_list.append({"user_id": message.get('user', ''),
                              "channel_id": channel_id,
                              "text": message.get('text', ''),
                              "ts": message.get('ts', '')})
        # If the message has a thread, fetch and add replies
        if 'thread_ts' in message:
            await fetch_and_add_replies(channel_id, message['thread_ts'], messages_list)

    return None

async def fetch_and_add_replies(channel_id, thread_ts, messages_list):
    """
        Fetch and add replies to the messages list
        :param channel_id: Channel ID of the thread
        :param thread_ts: Timestamp of the thread
        :param messages_list: List to store the messages
        :return: None
    """
    reply_cursor = None
    while True:
        replies_response = await fetch_replies(channel_id, thread_ts, reply_cursor)
        for reply in reversed(replies_response.get('messages', [])):
            # Skip the first message (original thread message)
            if reply == replies_response.get('messages', [])[0]:
                continue
            if reply.get('type') == 'message' and not reply.get('subtype'):
                messages_list.append({"user_id": reply.get('user', ''),
                                      "channel_id": channel_id,
                                      "text": reply.get('text', ''),
                                      "ts": reply.get('ts', '')})

        if not replies_response.get('has_more', False):
            break
        reply_cursor = replies_response['response_metadata'].get('next_cursor', None)

    return None

async def get_channel_messages(channel_id, channel):
    """
        Get all messages for the specified channel and add the last timestamp to channel
        :param channel_id: channel_id to fetch from
        :param channel: channel data
        :returns: (channel_id, messages(list of messages including replies from channel), timestamp)
    """
    messages = []
    try:
        cursor = None
        while True:
            response = await fetch_channel_messages(
                channel_id=channel_id,
                cursor=cursor,
                oldest=channel.get('last_read_timestamp')
            )
            # print(response)

            # Process and store messages
            for message in response.get('messages', []):
                await process_message(message, channel_id, messages)

            # Pagination: break if there's no next cursor
            if not response.get('has_more', False):
                break
            cursor = response['response_metadata'].get('next_cursor', None)
    except SlackApiError as e:
        print(f"Error fetching messages from channel {channel_id}: {e.response['error']}")
    return channel_id, messages, (messages[0]['ts'] if len(messages) > 0 else None)

async def get_all_messages(channels):
    """
        Get all messages from the specified channels
        :param channel: dictionary of channels to fetch messages from
        :return: list of messages from all channels
    """
    channel_promises = []
    messages = []
    for channel_id, new_messages, ts in await asyncio.gather(*[
            get_channel_messages(channel_id, channel) for channel_id, channel in channels.items()]):
        # Update the timestamp of the last message fetched
        channels[channel_id]['last_read_timestamp'] = ts
        messages.extend(new_messages)

    return messages
