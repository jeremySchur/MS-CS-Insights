from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch
import torch.nn.functional as F

# Load the tokenizer and model for sentiment analysis
tokenizer = RobertaTokenizer.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')
model = RobertaForSequenceClassification.from_pretrained('cardiffnlp/twitter-roberta-base-sentiment')

def calculate_sentiment(message):
    """
    Analyze the sentiment of a message
    :param message: string representing the text of a message
    :return: Sentiment score
    """
    # Encode the message
    inputs = tokenizer(message, return_tensors='pt', truncation=True, padding=True, max_length=100)
    
    # Run the model to get predictions
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Apply softmax to get probabilities
    probabilities = F.softmax(outputs.logits, dim=1)[0]
    
    # Convert sentiment label to a numerical score
    # Define a scale: Negative = -1, Neutral = 0, Positive = 1
    if torch.argmax(probabilities).item() == 2:  # Assuming index 2 is 'Positive'
        return probabilities[2].item()
    else:
        return -probabilities[0].item()  # Assuming index 0 is 'Negative'

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

