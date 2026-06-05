import os
import requests
import json
import time
from openai import OpenAI

# Configuration
PAGE_ACCESS_TOKEN = "EAASdREpsBg4BRJLmKbsgKmF1bKZCzOTTAST7nZAcYwHrhMx9r9Bd16K6ZA8E6pq8fjM3UR4MUfQFhMmZC6j8ZB0B3VILG7WyJucMKICDiktPCeFShW42WCXcKmINDcDZCieuS5tDmZC7IYpH3ws7IvQYOtpiPuoCb6Ig7OZBoHj2LA5RZANhvcY5waXaB1uYAZCZCNxQ5lPHHC5"
PAGE_ID = "589535454754591"
CANVA_DESIGN_ID = "DAGnnTGbqYQ"  # "Instagram Post - IT LINK CCTV Installation"

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

def get_canva_image_url():
    """Export the Canva design and return the download URL."""
    try:
        # We'll use the manus-mcp-cli to call the Canva MCP
        cmd = f"manus-mcp-cli tool call export-design --server canva --input '{{\"design_id\": \"{CANVA_DESIGN_ID}\", \"format\": {{\"type\": \"png\", \"pages\": [1]}}, \"user_intent\": \"Export design for Facebook post\"}}'"
        result_output = os.popen(cmd).read()
        
        # The result is saved to a JSON file, we need to find it
        # Based on previous logs, it's in /home/ubuntu/.mcp/tool-results/
        import glob
        list_of_files = glob.glob('/home/ubuntu/.mcp/tool-results/*canva_export-design.json')
        if not list_of_files:
            return None
            
        latest_file = max(list_of_files, key=os.path.getctime)
        with open(latest_file, 'r') as f:
            data = json.load(f)
            
        if data.get("job", {}).get("status") == "success":
            urls = data["job"].get("urls", [])
            if urls:
                return urls[0]
        return None
    except Exception as e:
        print(f"Error getting Canva image: {e}")
        return None

def post_to_page(message, image_url=None):
    if image_url:
        # Post with photo
        url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/photos"
        payload = {
            "caption": message,
            "url": image_url,
            "access_token": PAGE_ACCESS_TOKEN
        }
    else:
        # Post text only
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
    if not content:
        print("Failed to generate content.")
        exit(1)
        
    print("Exporting Canva design...")
    image_url = get_canva_image_url()
    
    if image_url:
        print(f"Image exported successfully: {image_url}")
    else:
        print("Failed to export Canva image, posting text only.")
        
    print("Posting to Facebook Page...")
    post_to_page(content, image_url)
