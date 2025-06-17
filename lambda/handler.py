import json
import boto3
import base64
from datetime import datetime

# AWS clients
comprehend = boto3.client('comprehend')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("JournalMoodLogs")

# helper functions

def analyze_sentiment(text):
    return comprehend.detect_sentiment(Text=text, LanguageCode='en')

# Function to extract key phrases from the text
def extract_key_phrases(text):
    result = comprehend.detect_key_phrases(Text=text, LanguageCode='en')
    return [p['Text'] for p in result['KeyPhrases']]

# Function to generate feedback based on sentiment and key phrases
def generate_feedback(sentiment, phrases):
    messages = {
        "POSITIVE": "You seemed upbeat today.",
        "NEGATIVE": "You seemed a bit low today.",
        "NEUTRAL": "Your tone today was pretty balanced.",
        "MIXED": "You seem to have mixed feelings right now."
    }
    phrase_snippet = ", ".join(phrases[:3]) if phrases else "nothing specific"
    prompt = f"Want to reflect more on '{phrases[0]}'?" if phrases else "What stood out to you today?"

    return {
        "summary": messages.get(sentiment, "Interesting tone."),
        "prompt": prompt,
        "top_phrases": phrase_snippet
    }

# Function to log the journal entry to DynamoDB
def log_entry(user_id, date_str, text_source, sentiment, feedback):
    table.put_item(Item={
        "entry_date": date_str,
        "user_id": user_id,
        "input_type": text_source,
        "sentiment": sentiment,
        "summary": feedback["summary"],
        "prompt": feedback["prompt"],
        "top_phrases": feedback["top_phrases"]
    })

# Function to decode a base64 encoded file
def decode_base64_file(file_b64):
    try:
        decoded = base64.b64decode(file_b64).decode('utf-8')
        return decoded
    except Exception as e:
        raise ValueError(f"Invalid base64 file: {e}")

# This is the entry point for the AWS Lambda function

def lambda_handler(event, context):
    try:
        body = event.get("body")
        if isinstance(body, str):
            body = json.loads(body)  # in case it's a raw string from API Gateway

        user_id = body.get("user_id", "anonymous")
        today = datetime.utcnow().strftime("%Y-%m-%d")

        # Detect input type
        if "text" in body:
            journal_text = body["text"]
            text_source = "typed"
        elif "file" in body:
            journal_text = decode_base64_file(body["file"])
            text_source = "uploaded"
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({"error": "No 'text' or 'file' field found."})
            }

        # Analyze
        sentiment_data = analyze_sentiment(journal_text)
        phrases = extract_key_phrases(journal_text)
        sentiment = sentiment_data["Sentiment"]
        feedback = generate_feedback(sentiment, phrases)

        # Log to DynamoDB
        log_entry(user_id, today, text_source, sentiment, feedback)

        # Response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'sentiment': sentiment,
                'sentiment_score': sentiment_data['SentimentScore'],
                'summary': feedback['summary'],
                'prompt': feedback['prompt'],
                'key_phrases': phrases
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
