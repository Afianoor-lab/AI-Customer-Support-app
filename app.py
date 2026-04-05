import streamlit as st
from textblob import TextBlob

# ===============================
# 🎨 UI Styling (Like your Screenshot)
# ===============================
st.markdown("""
    <style>
    /* Main background from your image */
    .stApp {
        background-color: #6366f1; 
    }
    
    /* Result Box (Dark like input box) */
    .result-box {
        background-color: #262730; /* Dark background like selectbox/input */
        border-left: 10px solid #8b5cf6;
        padding: 25px;
        border-radius: 15px;
        margin-top: 25px;
        color: #ffffff; /* Text color forced to white for visibility */
        box-shadow: 0px 10px 20px rgba(0,0,0,0.4);
    }
    
    /* Labels in result box should be visible on dark */
    .result-box b {
        color: #ffffff !important;
    }

    h1 {
        color: white;
        text-align: center;
        font-family: 'Segoe UI', Tahoma, sans-serif;
        margin-bottom: 30px;
    }
    
    label {
        color: white !important;
        font-weight: bold;
    }
    
    textarea {
        border-radius: 10px !important;
        border: 2px solid transparent !important;
        background-color: #262730 !important; /* Forces dark input */
        color: #ffffff !important;
    }

    .stButton>button {
        background-color: #8b5cf6 !important;
        color: white !important;
        border-radius: 10px !important;
        width: 100%;
        border: none !important;
        height: 50px;
        font-size: 18px;
        font-weight: bold;
    }
    
    /* --- DARK HISTORY SECTION --- */
    div[data-testid="stNotification"] {
        background-color: #262730 !important; /* Dark like input box */
        color: #ffffff !important; /* White text for info box */
        border-radius: 10px;
        border: 1px solid #475569;
    }
    
    div[data-testid="stNotification"] div {
        color: #ffffff !important;
    }

    div[data-testid="stNotification"] svg {
        fill: #ffffff !important; /* Information icon color */
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
# 🖥️ Frontend Layout (Updated with Dark Boxes)
# ===============================
st.markdown("<h1>AI Customer Support System</h1>", unsafe_allow_html=True)

# Input field direct background par hai (CSS forces it dark)
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

        # --- Display Result Box (Now Dark with White Text) ---
        st.markdown(f"""
            <div class="result-box">
                <p style="font-size: 18px;"><b>Input:</b> {message}</p>
                <p style="font-size: 18px;"><b>Category:</b> <span style="color: #6366f1; font-weight: bold;">{category}</span></p>
                <p style="font-size: 18px;"><b>Sentiment:</b> {sentiment}</p>
                <hr style="border-top: 1px solid #475569;">
                <p style="font-size: 18px;"><b>Auto-Reply:</b> <br><i>{reply}</i></p>
            </div>
        """, unsafe_allow_html=True)

# --- Message History Section (Styled Dark) ---
if st.session_state.history:
    st.markdown("<h3 style='color:white; margin-top:40px;'>Message History</h3>", unsafe_allow_html=True)
    for h in reversed(st.session_state.history):
        # Using st.info which is now styled as dark with white text
        st.info(f"**{h['message']}** → {h['category']}")
