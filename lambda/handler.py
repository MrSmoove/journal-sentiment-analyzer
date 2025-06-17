import json
import boto3

def lambda_handler(event, context):
    bucket_name = 'journal-entries-mrsmoove'        
    object_key = 'journal_entry.txt'           

    # Create clients for S3 and Comprehend
    s3 = boto3.client('s3')
    comprehend = boto3.client('comprehend')

    try:
        # Read the journal entry from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        journal_text = response['Body'].read().decode('utf-8')

        # Detect sentiment
        sentiment_response = comprehend.detect_sentiment(
            Text=journal_text,
            LanguageCode='en'
        )

        # Extract key phrases
        key_phrases_response = comprehend.detect_key_phrases(
            Text=journal_text,
            LanguageCode='en'
        )

        # Return results as JSON (for now)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'Sentiment': sentiment_response['Sentiment'],
                'SentimentScore': sentiment_response['SentimentScore'],
                'KeyPhrases': [phrase['Text'] for phrase in key_phrases_response['KeyPhrases']]
            })
        }

    except Exception as e:
        # Return error if something goes wrong
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
