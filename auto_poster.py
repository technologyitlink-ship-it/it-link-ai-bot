import os
import requests
import json
from openai import OpenAI

# Configuration
PAGE_ACCESS_TOKEN = "EAASdREpsBg4BRJLmKbsgKmF1bKZCzOTTAST7nZAcYwHrhMx9r9Bd16K6ZA8E6pq8fjM3UR4MUfQFhMmZC6j8ZB0B3VILG7WyJucMKICDiktPCeFShW42WCXcKmINDcDZCieuS5tDmZC7IYpH3ws7IvQYOtpiPuoCb6Ig7OZBoHj2LA5RZANhvcY5waXaB1uYAZCZCNxQ5lPHHC5"
PAGE_ID = "589535454754591"

def generate_content():
    try:
        client = OpenAI()
        
        PROMPT = """
        You are a creative content writer for IT Link CCTV, MATV, PABX.
        Write a Facebook post in Myanmar language (Burmese) that is helpful and engaging for customers.
        The post should be about one of these topics:
        1. Benefits of installing CCTV for home security.
        2. Why businesses need a professional PABX phone system.
        3. The importance of Fire Alarm systems.
        4. Tips for better WiFi coverage in a large building.
        5. Why MATV systems are essential for hotels and apartments.

        Guidelines:
        - Use a warm, friendly, and professional tone.
        - Use honorifics like "ခင်ဗျာ".
        - Include relevant emojis.
        - Keep it concise but informative (3-5 paragraphs).
        - Include contact numbers: 09 425 298 539, 09 758 425 298 39.
        - Add relevant hashtags: #ITLink #CCTV #SecuritySystem #Myanmar.
        - Output ONLY the post content.
        """
        
        # Use a supported model: gpt-4.1-mini
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": PROMPT},
                {"role": "user", "content": "Generate a helpful Facebook post for today."}
            ],
            max_tokens=1000,
            temperature=0.8
        )
        
        if response and response.choices:
            return response.choices[0].message.content
        return None
    except Exception as e:
        print(f"Error generating content: {e}")
        return None

def post_to_page(message):
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/feed"
    payload = {
        "message": message,
        "access_token": PAGE_ACCESS_TOKEN
    }
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        print(f"Post response: {response.status_code} - {json.dumps(result)}")
        return result
    except Exception as e:
        print(f"Error posting to page: {e}")
        return None

if __name__ == "__main__":
    print("Generating content...")
    content = generate_content()
    if content:
        print("Content generated successfully:")
        print("-" * 30)
        print(content)
        print("-" * 30)
        print("Posting to Facebook Page...")
        post_to_page(content)
    else:
        print("Failed to generate content.")
