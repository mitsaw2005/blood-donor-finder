import streamlit as st
import mysql.connector
import datetime
from twilio.rest import Client
import google.generativeai as genai  # For Chatbot
import random  # For AI Donor Matching

# Database Config
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "123456789",
    "database": "blood_donor_db"
}

# Twilio Config
TWILIO_SID = "AC65885d3658f8eeb042874b60c4b5d8c2"
TWILIO_AUTH_TOKEN = "fe32230c4e92b4f780a7d7a9ad1828fc"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

# Google Gemini AI Config (For Chatbot)
GEMINI_API_KEY = "AIzaSyCCcfIRu4Tp3HylB7ppS7Js9VkwBrhRVB4"
genai.configure(api_key=GEMINI_API_KEY)

def connect_db():
    return mysql.connector.connect(**DB_CONFIG)

def register_donor(name, age, blood_group, phone, city, last_donation):
    conn = connect_db()
    cursor = conn.cursor()
    query = """INSERT INTO donors (name, age, blood_group, phone, city, last_donation) 
                VALUES (%s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, (name, age, blood_group, phone, city, last_donation))
    conn.commit()
    conn.close()

def ai_find_best_donor(blood_group, city, min_age, max_age):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    three_months_ago = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime('%Y-%m-%d')
    
    query = """SELECT * FROM donors 
                WHERE blood_group = %s AND city = %s AND last_donation <= %s 
                AND age BETWEEN %s AND %s"""
    cursor.execute(query, (blood_group, city, three_months_ago, min_age, max_age))
    donors = cursor.fetchall()
    conn.close()
    
    if not donors:
        return []
    
    # AI-Powered Ranking (randomized for now, can be ML-based)
    return sorted(donors, key=lambda x: random.random())

def send_whatsapp_message(donor_phone, requester_name, blood_group, location):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    message = f"Urgent: {requester_name} needs {blood_group} blood in {location}. If you can donate, please reply!"
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=f"whatsapp:+91{donor_phone}"
    )

def ai_chatbot_response(user_query):
    model = genai.GenerativeModel("gemini-1.5-pro-latest")
    response = model.generate_content(user_query)
    return response.text.strip()

st.set_page_config(page_title="eBloodConnect", page_icon="❤️", layout="wide")

st.markdown('<h1 style="text-align:center; color:#d9534f;">eBloodConnect</h1>', unsafe_allow_html=True)
st.markdown('<h4 style="text-align:center; color:#aaa;">AI-Powered Blood Donation Platform</h4>', unsafe_allow_html=True)

option = st.selectbox("Choose an action", ["Register as Donor", "Find a Donor", "Ask Blood Donation Chatbot"], index=0)

if option == "Register as Donor":
    st.header("Register as a Blood Donor")
    name = st.text_input("Full Name")
    age = st.number_input("Age", min_value=18, max_value=60, step=1)
    blood_group = st.selectbox("Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    phone = st.text_input("Phone Number (without +91)")
    city = st.text_input("City")
    last_donation = st.date_input("Last Donation Date")
    
    if st.button("Register", key="register"):
        if name and blood_group and phone and city and last_donation:
            register_donor(name, age, blood_group, phone, city, last_donation)
            st.success(f"Thank you, {name}! You have been successfully registered as a donor.")
        else:
            st.warning("Please fill in all the details.")

elif option == "Find a Donor":
    st.header("Find a Blood Donor")
    requester_name = st.text_input("Your Name")
    blood_group = st.selectbox("Required Blood Group", ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"])
    location = st.text_input("City")
    
    # Age Preference
    min_age = st.number_input("Minimum Donor Age", min_value=18, max_value=60, value=18, step=1)
    max_age = st.number_input("Maximum Donor Age", min_value=18, max_value=60, value=60, step=1)
    
    if st.button("Find Donors", key="find"):
        if requester_name and location:
            donors = ai_find_best_donor(blood_group, location, min_age, max_age)
            if donors:
                st.write(f"### Best AI-Suggested Donors in {location} for {blood_group} blood:")
                for donor in donors[:3]:
                    st.markdown(f"""
                        <div style='background-color: #ffffff; padding: 10px; margin-bottom: 10px; color: black; font-weight: bold; border-radius: 5px;'>
                            <strong>Name:</strong> {donor['name']}<br>
                            <strong>Age:</strong> {donor['age']}<br>
                            <strong>Phone:</strong> {donor['phone']}
                        </div>
                    """, unsafe_allow_html=True)
                    send_whatsapp_message(donor['phone'], requester_name, blood_group, location)
                st.success("Top donors have been notified via WhatsApp!")
            else:
                st.warning("No eligible donors found in this area. Try adjusting the age range.")
        else:
            st.warning("Please provide your name and location.")

elif option == "Ask Blood Donation Chatbot":
    st.header("Blood Donation Chatbot 🤖")
    user_query = st.text_area("Ask me anything about blood donation!")
    if st.button("Ask AI", key="chatbot"):
        if user_query:
            response = ai_chatbot_response(user_query)
            st.write("### AI Response:")
            st.write(response)
        else:
            st.warning("Please enter a question.")