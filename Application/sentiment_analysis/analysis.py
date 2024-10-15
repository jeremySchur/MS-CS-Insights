from transformers import pipeline

def analyze_sentiments(messages_dict):
    """
        Analyze the sentiments of messages in each channel
        :param messages_dict: Dictionary containing messages for each channel
        :return: Dictionary containing sentiment scores for each channel
    """
    # Initialize the sentiment analysis pipeline with a specific model
    sentiment_pipeline = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

    sentiment_scores = {}  
    for channel_id, messages in messages_dict.items():
        total_sentiment = 0
        for message in messages:
            # Perform sentiment analysis on the message
            analysis = sentiment_pipeline(message)[0]
            # Convert sentiment label to a numerical score
            if analysis['label'] == 'POSITIVE':
                total_sentiment += analysis['score']
            else:
                total_sentiment -= analysis['score']
        
        # Calculate the average sentiment score for the channel
        if messages:
            sentiment_scores[channel_id] = total_sentiment / len(messages)
        else:
            sentiment_scores[channel_id] = 0.0
    
    return sentiment_scores


def categorize_sentiments(sentiment_scores):
    categorized_sentiments = {}
    for channel_id, score in sentiment_scores.items():
        if score > 0.05:
            categorized_sentiments[channel_id] = "POSITIVE"
        elif score < -0.05:
            categorized_sentiments[channel_id] = "NEGATIVE"
        else:
            categorized_sentiments[channel_id] = "NEUTRAL"
    
    return categorized_sentiments
