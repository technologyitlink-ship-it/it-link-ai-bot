import os
import json
import requests
from flask import Flask, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file for local development
load_dotenv()

app = Flask(__name__)

# --- Configuration ---
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN", "itlink_verify_token_123")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PAGE_ID = os.environ.get("PAGE_ID", "589535454754591")

# Initialize OpenAI client
client = None
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    print("WARNING: OPENAI_API_KEY is not set. AI responses will use fallback.")

PAGE_CONTEXT = """
You are an AI assistant for "IT Link CCTV,MATV,PABX" in Myanmar. 
Your goal is to reply to customer messages on Facebook in Myanmar (Burmese) language ONLY.

Company Information:
- Name: IT Link CCTV,MATV,PABX
- Services: CCTV, MATV, PABX, Fingerprint, Door Access, WiFi, Fire Alarm
- Location: No.56, Yangon-Pyay Road, Yangon, Myanmar
- Phone: 09 425 298 539, 09 758 425 298 39
- Email: technologyitlink@gmail.com

Instructions:
1. Always reply ONLY in Myanmar (Burmese) language.
2. Be polite and professional.
3. If the customer asks for prices, mention that prices depend on requirements and ask them to call.
4. Always include contact numbers: 09 425 298 539 or 09 758 425 298 39
5. Keep replies concise (3-4 sentences max).
6. If you don't know the answer, ask them to contact the phone numbers above.
7. Reply to every message - whether it's a greeting, question, or anything else.
"""

def get_ai_response(user_message):
    """Generate AI response for customer message."""
    try:
        if not client:
            return get_fallback_response(user_message)
        
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": PAGE_CONTEXT},
                {"role": "user", "content": user_message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        reply = response.choices[0].message.content
        print(f"AI generated reply: {reply}")
        return reply
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return get_fallback_response(user_message)

def get_fallback_response(user_message):
    """Fallback response when AI is unavailable."""
    return ("မင်္ဂလာပါ! IT Link ကို ဆက်သွယ်ပေးတဲ့အတွက် ကျေးဇူးတင်ပါတယ်။ "
            "ကျွန်တော်တို့ Admin Team က အမြန်ဆုံး ပြန်ဖြေပေးပါမယ်။ "
            "အရေးကြီးနေတယ်ဆိုရင်တော့ "
            "09-425 298 539 ဒါမှမဟုတ် 09-758 425 298 39 ကို ဆက်သွယ်ပေးပါခင်ဗျာ။")

def send_message(recipient_id, message_text):
    """Send a message to a Facebook user."""
    if not PAGE_ACCESS_TOKEN:
        print("Error: PAGE_ACCESS_TOKEN is not set.")
        return None
    
    url = f"https://graph.facebook.com/v19.0/me/messages"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text},
        "messaging_type": "RESPONSE"
    }
    headers = {"Content-Type": "application/json"}
    params = {"access_token": PAGE_ACCESS_TOKEN}
    
    try:
        response = requests.post(url, json=payload, headers=headers, params=params, timeout=15)
        result = response.json()
        print(f"Send message response: {response.status_code} - {json.dumps(result)}")
        
        if response.status_code == 200:
            print(f"Successfully sent reply to {recipient_id}")
        else:
            print(f"Failed to send message: {result}")
        
        return result
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

@app.route("/", methods=["GET"])
def home():
    """Home endpoint - also handles webhook verification."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    # If this is a webhook verification request
    if mode and token and challenge:
        print(f"Verification request: mode={mode}, token={token}")
        if mode == "subscribe" and token == VERIFY_TOKEN:
            print("Webhook verification successful!")
            return challenge, 200
        print("Webhook verification failed!")
        return "Verification failed", 403
    
    # Normal home page
    return jsonify({
        "status": "running",
        "service": "IT Link Facebook Auto-Reply Bot",
        "version": "2.0.0"
    })

@app.route("/webhook", methods=["GET"])
def webhook_verify():
    """Webhook verification endpoint."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"Webhook verification: mode={mode}, token={token}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified!")
        return challenge, 200
    
    return jsonify({"error": "Verification failed"}), 403

@app.route("/webhook", methods=["POST"])
@app.route("/", methods=["POST"])
def webhook():
    """Handle incoming webhook events from Facebook."""
    data = request.json
    print(f"Webhook received: {json.dumps(data)}")
    
    if not data:
        return "No data", 400
    
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            # Handle messaging events
            messaging_events = entry.get("messaging", [])
            for messaging_event in messaging_events:
                handle_messaging_event(messaging_event)
            
            # Handle feed changes (comments)
            changes = entry.get("changes", [])
            for change in changes:
                handle_change_event(change)
        
        return "EVENT_RECEIVED", 200
    
    return "Not Found", 404

def handle_messaging_event(messaging_event):
    """Process a single messaging event and send auto-reply."""
    try:
        sender_id = messaging_event.get("sender", {}).get("id")
        
        # Skip if sender is the page itself (prevent echo loop)
        if sender_id == PAGE_ID:
            print(f"Skipping message from page itself: {sender_id}")
            return
        
        # Handle text messages
        if "message" in messaging_event:
            message = messaging_event["message"]
            
            # Skip echo messages (messages sent by the page)
            if message.get("is_echo"):
                print("Skipping echo message")
                return
            
            message_text = message.get("text")
            
            if message_text:
                print(f"Processing message from {sender_id}: {message_text}")
                
                # Generate AI response
                ai_reply = get_ai_response(message_text)
                print(f"AI Reply for {sender_id}: {ai_reply}")
                
                # Send the reply
                send_message(sender_id, ai_reply)
            else:
                # Handle non-text messages (stickers, images, etc.)
                print(f"Non-text message from {sender_id}, sending default reply")
                default_reply = get_fallback_response("hello")
                send_message(sender_id, default_reply)
        
        # Handle postbacks (button clicks)
        elif "postback" in messaging_event:
            postback_payload = messaging_event["postback"].get("payload", "")
            print(f"Postback from {sender_id}: {postback_payload}")
            ai_reply = get_ai_response(postback_payload)
            send_message(sender_id, ai_reply)
            
    except Exception as e:
        print(f"Error handling messaging event: {e}")

def handle_change_event(change):
    """Handle page change events like comments."""
    try:
        field = change.get("field")
        value = change.get("value", {})
        
        if field == "feed" and value.get("item") == "comment":
            comment_message = value.get("message", "")
            from_id = value.get("from", {}).get("id")
            
            # Don't reply to own comments
            if from_id == PAGE_ID:
                return
            
            if comment_message:
                print(f"Comment from {from_id}: {comment_message}")
                # For comments, we can send a private message
                ai_reply = get_ai_response(comment_message)
                send_message(from_id, ai_reply)
    except Exception as e:
        print(f"Error handling change event: {e}")

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "page_token_set": bool(PAGE_ACCESS_TOKEN),
        "openai_key_set": bool(OPENAI_API_KEY),
        "verify_token": VERIFY_TOKEN
    })

@app.route("/test-reply", methods=["POST"])
def test_reply():
    """Test endpoint to verify AI reply generation."""
    data = request.json or {}
    message = data.get("message", "hello")
    reply = get_ai_response(message)
    return jsonify({"input": message, "reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting IT Link Bot on port {port}")
    print(f"PAGE_ACCESS_TOKEN set: {bool(PAGE_ACCESS_TOKEN)}")
    print(f"OPENAI_API_KEY set: {bool(OPENAI_API_KEY)}")
    print(f"VERIFY_TOKEN: {VERIFY_TOKEN}")
    app.run(port=port, host="0.0.0.0", debug=False)
