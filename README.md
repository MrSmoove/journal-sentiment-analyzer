# Journal Sentiment Analyzer

A small AWS-powered app that analyzes the emotional tone of your journal entries using Amazon Comprehend. Built to explore serverless architecture, mental wellness tools, and hands-on ML services.

## 🔍 Features
- Upload journal text
- Sentiment analysis (Positive, Neutral, Negative, Mixed)
- Key phrase extraction
- Serverless architecture via AWS Lambda

## 🛠️ Built With
- AWS Lambda
- Amazon Comprehend
- Amazon S3
- IAM Roles & CloudWatch

## 🚀 How It Works
1. Upload or write a journal entry
2. Trigger a Lambda function (manually or via S3 event)
3. Lambda reads your entry and uses Comprehend to analyze:
   - Sentiment
   - Key phrases
4. Results are returned in JSON format

## 🧪 Example Output (as of the current version)
```json
{
  "Sentiment": "NEUTRAL",
  "Positive": 0.12,
  "Negative": 0.05,
  "Neutral": 0.81,
  "Mixed": 0.02,
  "KeyPhrases": ["meeting today", "feeling scattered", "progress"]
}

