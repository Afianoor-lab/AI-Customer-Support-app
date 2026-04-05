import streamlit as st
from textblob import TextBlob

# ===============================
# 🎨 UI Styling (Like your Screenshot)
# ===============================
st.markdown("""
    <style>
    .stApp {
        background-color: #6366f1; /* Purple/Blue background from your image */
    }
    .main-container {
        background-color: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .result-box {
        background-color: #f8fafc;
        border-left: 5px solid #6366f1;
        padding: 20px;
        border-radius: 8px;
        margin-top: 20px;
        color: #1e293b;
    }
    h1 {
        color: white;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, sans-serif;
    }
    .stButton>button {
        background-color: #8b5cf6 !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ===============================
# 🧠 Backend Logic
# ===============================
if 'history' not in st.session_state:
    st.session_state.history = []

def classify_message(message):
    msg = message.lower()
    if any(word in msg for word in ["refund", "return", "money back"]):
        return "Refund / Return"
    elif any(word in msg for word in ["late", "delivery", "shipping", "order status"]):
        return "Delivery Question"
    elif any(word in msg for word in ["buy", "price", "cost", "purchase"]):
        return "Sales Inquiry"
    elif any(word in msg for word in ["error", "issue", "login", "bug", "technical"]):
        return "Account / Technical Issue"
    elif any(word in msg for word in ["complaint", "bad", "worst", "angry"]):
        return "Complaint"
    elif len(msg.strip()) < 5:
        return "Spam"
    else:
        return "General Query"

def analyze_sentiment(message):
    polarity = TextBlob(message).sentiment.polarity
    if polarity > 0.1:
        return "Positive 😊"
    elif polarity < -0.1:
        return "Negative 😡"
    else:
        return "Neutral 😐"

def generate_reply(category):
    replies = {
        "Complaint": "We’re sorry for the inconvenience. Our team will review your concern shortly.",
        "Refund / Return": "Thank you for contacting us. Our support team will assist you with the refund process.",
        "Sales Inquiry": "Thank you for your interest. Our sales team will provide you with the requested details.",
        "Delivery Question": "We are checking the status of your delivery and will update you soon.",
        "Account / Technical Issue": "Our technical team is working to resolve the issue. Thank you for your patience.",
        "General Query": "Thank you for reaching out. We will get back to you shortly.",
        "Spam": "Thank you for your message."
    }
    return replies.get(category, "Thank you for contacting us.")

# ===============================
# 🖥️ Frontend Layout
# ===============================
st.markdown("<h1>AI Customer Support System</h1>", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    message = st.text_area("Enter Customer Message:", placeholder="Type here...", height=100)
    
    if st.button("Process Message"):
        if message.strip() == "":
            st.warning("Please enter a message first!")
        else:
            category = classify_message(message)
            sentiment = analyze_sentiment(message)
            reply = generate_reply(category)
            
            result = {
                "message": message,
                "category": category,
                "sentiment": sentiment,
                "reply": reply
            }
            st.session_state.history.append(result)

            # Display Result
            st.markdown(f"""
                <div class="result-box">
                    <p><b>Input:</b> {message}</p>
                    <p><b>Category:</b> {category}</p>
                    <p><b>Sentiment:</b> {sentiment}</p>
                    <hr>
                    <p><b>Auto-Reply:</b> {reply}</p>
                </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# Message History Section
if st.session_state.history:
    st.markdown("<h3 style='color:white; margin-top:30px;'>Message History</h3>", unsafe_allow_html=True)
    for h in reversed(st.session_state.history):
        st.info(f"**{h['message']}** → {h['category']}")
