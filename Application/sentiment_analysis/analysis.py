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


# Example usage
if __name__ == "__main__":
    messages = {
        "course1": [
            "I love this course!",
            "The instructor is amazing!",
            "Great content and well explained.",
            "I'm learning so much.",
            "This is exactly what I needed.",
            "The examples are very helpful.",
            "I appreciate the detailed explanations.",
            "This course is worth every penny.",
            "I'm really enjoying the assignments.",
            "Fantastic course structure."
        ],
        "course2": [
            "I'm struggling with the material.",
            "The pace is too fast for me.",
            "I don't understand the last lecture.",
            "Can someone help me with the homework?",
            "I'm finding it hard to keep up.",
            "The quizzes are too difficult.",
            "I need more examples to understand.",
            "The instructor's accent is hard to follow.",
            "I'm feeling overwhelmed.",
            "I might need to drop this course."
        ],
        "course3": [
            "This course is okay.",
            "The content is decent.",
            "Not bad, but could be better.",
            "I'm learning, but it's slow.",
            "The instructor is alright.",
            "Some parts are confusing.",
            "The assignments are manageable.",
            "I wish there were more examples.",
            "The pace is moderate.",
            "Overall, it's an average course."
        ],
        "course4": [
            "This course is too easy.",
            "I finished all the assignments quickly.",
            "The content is too basic.",
            "I expected more advanced material.",
            "The quizzes are too simple.",
            "I'm not challenged enough.",
            "I need something more rigorous.",
            "The pace is too slow.",
            "I wish there were more difficult problems.",
            "This course is not for advanced learners."
        ],
        "course5": [
            "This course is too hard.",
            "I'm struggling to understand the concepts.",
            "The assignments are very challenging.",
            "I need more help from the instructor.",
            "The pace is too fast.",
            "The quizzes are very difficult.",
            "I'm feeling lost.",
            "I need more basic explanations.",
            "This course is not for beginners.",
            "I'm considering dropping out."
        ],
        "course6": [
            "The course content is outdated.",
            "The examples are not relevant.",
            "I wish the material was more current.",
            "The instructor needs to update the lectures.",
            "The assignments are based on old technologies.",
            "I'm not learning anything new.",
            "The quizzes are based on outdated information.",
            "I expected more up-to-date content.",
            "The course needs a refresh.",
            "I'm disappointed with the outdated material."
        ],
        "course7": [
            "The course is very interactive.",
            "I love the hands-on approach.",
            "The projects are very engaging.",
            "I'm learning by doing.",
            "The instructor encourages participation.",
            "The assignments are very practical.",
            "I appreciate the real-world examples.",
            "The course is very immersive.",
            "I'm enjoying the interactive sessions.",
            "This is a very engaging course."
        ],
        "course8": [
            "The course is very theoretical.",
            "I wish there were more practical examples.",
            "The content is too abstract.",
            "I'm struggling to apply the concepts.",
            "The assignments are very theoretical.",
            "I need more hands-on practice.",
            "The quizzes are too abstract.",
            "I wish the course was more practical.",
            "The lectures are very theoretical.",
            "I'm finding it hard to relate to the material."
        ],
        "course9": [
            "The instructor is very supportive.",
            "I appreciate the quick responses.",
            "The feedback on assignments is very helpful.",
            "The instructor is very approachable.",
            "I'm getting a lot of support.",
            "The instructor is very encouraging.",
            "I feel very supported in this course.",
            "The instructor is very knowledgeable.",
            "I'm learning a lot from the feedback.",
            "The instructor is very patient."
        ],
        "course10": [
            "The course platform is very user-friendly.",
            "I love the interface.",
            "The navigation is very intuitive.",
            "The course materials are easy to access.",
            "The platform is very responsive.",
            "I'm having a great experience with the platform.",
            "The course layout is very clear.",
            "The platform is very stable.",
            "I'm enjoying the user experience.",
            "The platform is very well designed."
        ]
    }
    
    sentiment_scores = analyze_sentiments(messages)
    print(sentiment_scores)
    categorized_scores = categorize_sentiments(sentiment_scores)
    print(categorized_scores)