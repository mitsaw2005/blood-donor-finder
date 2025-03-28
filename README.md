eBloodConnect - AI-Powered Blood Donor Finder

A smart way to find blood donors quickly and efficiently!

🚀 About the Project

eBloodConnect is a web-based platform that connects blood donors with people in need. It uses AI-powered donor matching and automated WhatsApp notifications via Twilio to streamline the donation process.

✨ Features

✅ Register as a Blood Donor with age, blood group, location, and last donation date.

🔎 Find Donors Quickly using AI-powered best-match recommendations.

🤖 AI Chatbot to answer blood donation-related queries.

📲 WhatsApp Notifications to alert donors and requesters.

🛠️ Tech Stack

Frontend: Streamlit (Python-based UI framework)

Backend: MySQL (for storing donor/requester data)

AI Integration: Google Gemini API (for chatbot)

Messaging: Twilio WhatsApp API

📌 Installation & Setup

1️⃣ Clone the Repository

 git clone https://github.com/mitsaw2005/blood-donor-finder.git
 cd blood-donor-finder

2️⃣ Install Dependencies

Make sure you have Python installed. Then, run:

pip install -r requirements.txt

3️⃣ Configure Environment Variables

Rename .env.example to .env and add your API keys:

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=blood_donor_db
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
GEMINI_API_KEY=your_google_gemini_api_key

4️⃣ Run the Application

streamlit run app.py

🎯 How to Use

For Donors:

Open the app and click Register as Donor.

Fill in your details and submit.

You'll be notified if someone requests blood matching your profile.

For Requesters:

Select Find a Donor and enter details.

AI will suggest best-matching donors in your city.

Selected donors will receive WhatsApp notifications.

🚀 Deployment on Streamlit Cloud

Push Code to GitHub

git add .
git commit -m "Deploy update"
git push origin main

Go to Streamlit Cloud and select your repository.

Deploy & Enjoy! 🎉

🤝 Contributing

Want to contribute? Follow these steps:

Fork the project.

Create your feature branch: git checkout -b feature-name

Commit changes: git commit -m "Added new feature"

Push to GitHub: git push origin feature-name

Open a pull request.
