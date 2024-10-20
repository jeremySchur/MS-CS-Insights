from slack import update_public_channels, get_all_messages
from analysis import analyze_sentiments
from postgres import insert_messages, update_timestamps, get_channels, update_avg_sentiments
from time import sleep
import json

# Main function
if __name__ == '__main__':
    # Get all public channels
    channels = get_channels()
    while True:
        # Update the public channels
        update_public_channels(channels)
        # print(json.dumps(channels, indent=4)) # Uncomment to see all channels
        # Get all messages from the public channels
        messages = get_all_messages(channels)
        analyze_sentiments(messages)
        # put messages in to db
        insert_messages(messages)
        # update timestamps to latest
        update_timestamps(channels)
        # update average sentiments
        update_avg_sentiments()

        print(json.dumps(messages, indent=4))
        sleep(60)  # Sleep for 60 seconds

