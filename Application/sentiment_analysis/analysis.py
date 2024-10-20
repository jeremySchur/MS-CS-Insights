from transformers import pipeline

# Initialize the sentiment analysis pipeline with a specific model
# not ideal that this is global but better than creating it every time.
pipe = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
def calculate_sentiment(message):
    """
        Analyze the sentiment of a message
        :param message: string representing sentiment score of a message
        :return: Sentiment score
    """
    analysis = pipe(message)[0]
    # Convert sentiment label to a numerical score
    if analysis['label'] == 'POSITIVE':
        return analysis['score']
    else:
        return - analysis['score']

def analyze_sentiments(messages):
    """
        Analyze the sentiments of messages and add to message
        :param messages: list of dictionaries representing messages
        :return: None
    """
    for message in messages:
        # Perform sentiment analysis on the message
        sentiment = calculate_sentiment(message["text"])
        message["sentiment"] = sentiment

    return None

