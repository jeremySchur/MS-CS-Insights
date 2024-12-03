from slack import update_public_channels, get_all_messages
from analysis import analyze_sentiments
from postgres import insert_messages, update_timestamps, get_channels, update_avg_sentiments
from time import sleep, time, ctime
import schedule
import asyncio
# import json

def job():
    """
        Main function to run the message fetching and sentiment analysis
        :param None
        :return: None
    """
    start_time = time()
    # Get all public channels
    channels = get_channels()
    # Update the public channels
    update_public_channels(channels)
    # print(json.dumps(channels, indent=2, default=str)) # Uncomment to see all channels

    # Get all messages from the public channels
    messages = asyncio.run(get_all_messages(channels))
    analyze_sentiments(messages)
    # put messages in to db
    insert_messages(messages)
    # update timestamps to latest
    update_timestamps(channels)
    # update average sentiments
    update_avg_sentiments()

    end_time = time()
    # print(json.dumps(messages, indent=4)) # Uncomment to see all messages
    print("Processed " + str(len(messages)) + " messages in " + str(end_time - start_time) + " seconds")
    return None

# Main function
if __name__ == '__main__':
    job()
    schedule.every(60).seconds.do(job) # SET THIS TO 1 DAY OR MORE FOR ACTUAL USE (60 seconds is for testing purposes).
    while True:
        schedule.run_pending()
        sleep(1)
