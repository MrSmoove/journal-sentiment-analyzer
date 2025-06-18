# ✨ PulseNote: Journal Sentiment Analyzer 🧠📝

A reflective journaling tool that uses AI to analyze the **emotion**, **tone**, and **key phrases** in your writing. Built with a full **AWS serverless stack** and a modern React frontend.

---

## 🌍 Live Demo

👉 **Try it here**: [http://pulse-note-frontend.s3-website.us-east-2.amazonaws.com/](http://pulse-note-frontend.s3-website.us-east-2.amazonaws.com/)

No installation needed. Just write, reflect, and grow.

---

## ⚙️ For Developers

Want to customize or contribute? Follow the steps below to run locally.

### 1. Clone the Repo

git clone https://github.com/MrSmoove/journal-sentiment-analyzer.git
cd journal-sentiment-analyzer/frontend
### 2. Install Dependencies
bash
Copy
Edit
npm install
### 3. Create Your .env File
Inside frontend/, add a .env file with:

env
Copy
Edit
VITE_API_URL=https://your-api-id.execute-api.us-east-2.amazonaws.com/dev/analyze
### 4. Run Locally
bash
Copy
Edit
npm run dev

### 🌐 Live Deployment
Your site is hosted on AWS S3 with public access and static website hosting enabled.
To build and deploy manually:

bash
Copy
Edit
npm run build
Then upload the contents of frontend/dist/ to your S3 bucket.

🤖 GitHub Actions (CI/CD)
Automatically deploy to S3 on push to main branch. Configure your .github/workflows/deploy.yml like this:

yaml
Copy
Edit
# Sample setup (replace with your actual S3 bucket + AWS secrets)
[You can find the full deploy.yml in the .github/workflows directory.]

🧪 Testing & Feedback
🧪 Test API responses using test_data/test_request.py

✅ All requests validated against AWS Comprehend’s expected payload

🗂️ Errors and timeouts handled gracefully with clear messages

✨ Future Features
📈 Mood trend chart with DynamoDB

🎯 Prompt suggestions based on sentiment

📲 Mobile-first design polish
