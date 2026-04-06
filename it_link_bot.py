import os
import json
import requests
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# --- Configuration ---
VERIFY_TOKEN = "itlink_verify_token_123"
PAGE_ACCESS_TOKEN = "EAASdREpsBg4BRJLmKbsgKmF1bKZCzOTTAST7nZAcYwHrhMx9r9Bd16K6ZA8E6pq8fjM3UR4MUfQFhMmZC6j8ZB0B3VILG7WyJucMKICDiktPCeFShW42WCXcKmINDcDZCieuS5tDmZC7IYpH3ws7IvQYOtpiPuoCb6Ig7OZBoHj2LA5RZANhvcY5waXaB1uYAZCZCNxQ5lPHHC5"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

PAGE_CONTEXT = """
You are an AI assistant for "IT Link CCTV,MATV,PABX" in Myanmar. 
Your goal is to reply to customer messages on Facebook in Myanmar (Burmese) language ONLY.

Company Information:
- Name: IT Link CCTV,MATV,PABX
- Services: CCTV, MATV, PABX, Fingerprint, Door Access, WiFi, Fire Alarm
- Location: No.56, Yangon-Pyay Road, Yangon, Myanmar
- Phone: +95 9 758 422758
- Email: technologyitlink@gmail.com
- Website: itlink.com

Instructions:
1. Always reply ONLY in Myanmar (Burmese) language.
2. Be polite and professional.
3. If the customer asks for prices, mention that prices depend on requirements.
4. If you don't know the answer, ask them to contact +95 9 758 422758.
"""

def get_ai_response(user_message):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": PAGE_CONTEXT},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error getting AI response: {e}")
        return "တောင်းပန်ပါတယ်၊ အခုလောလောဆယ် အဆင်မပြေဖြစ်နေလို့ ခဏနေမှ ပြန်မေးပေးပါခင်ဗျာ။"

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Send message response: {response.status_code} - {response.text}")
        return response.json()
    except Exception as e:
        print(f"Error sending message: {e}")
        return None

@app.route("/", methods=["GET"])
def verify():
    # Webhook verification
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print(f"Verification request: mode={mode}, token={token}, challenge={challenge}")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Verification successful!")
        return challenge, 200
    
    print("Verification failed!")
    return "Verification failed", 403

@app.route("/", methods=["POST"])
def webhook():
    data = request.json
    print(f"Webhook received: {json.dumps(data)}")
    
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                if messaging_event.get("message"):
                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text")
                    
                    if message_text:
                        print(f"Message from {sender_id}: {message_text}")
                        ai_reply = get_ai_response(message_text)
                        print(f"AI Reply: {ai_reply}")
                        send_message(sender_id, ai_reply)
        return "EVENT_RECEIVED", 200
    return "Not Found", 404

if __name__ == "__main__":
    app.run(port=8080, host="0.0.0.0")
