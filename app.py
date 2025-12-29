from flask import Flask, render_template, request
from textblob import TextBlob
import webbrowser
import os

app = Flask(__name__)

history = []

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
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

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

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        message = request.form["message"]
        category = classify_message(message)
        sentiment = analyze_sentiment(message)
        reply = generate_reply(category)
        result = {
            "message": message,
            "category": category,
            "sentiment": sentiment,
            "reply": reply
        }
        history.append(result)
    return render_template("index.html", result=result, history=history)

# -----------------------
# Single browser tab fix
# -----------------------
if __name__ == "__main__":
    # Only open browser in the main process, not reloader
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)
