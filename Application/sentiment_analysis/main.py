from slack import update_public_channels, get_all_messages
from analysis import analyze_sentiments, categorize_sentiments
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

        print(json.dumps(messages, indent=4))
        sleep(60)  # Sleep for 60 seconds
    
