import os
import requests
import json

# Configuration
PAGE_ACCESS_TOKEN = "EAASdREpsBg4BRJLmKbsgKmF1bKZCzOTTAST7nZAcYwHrhMx9r9Bd16K6ZA8E6pq8fjM3UR4MUfQFhMmZC6j8ZB0B3VILG7WyJucMKICDiktPCeFShW42WCXcKmINDcDZCieuS5tDmZC7IYpH3ws7IvQYOtpiPuoCb6Ig7OZBoHj2LA5RZANhvcY5waXaB1uYAZCZCNxQ5lPHHC5"
PAGE_ID = "589535454754591"

def post_to_page(message):
    """Post a message to the Facebook Page feed."""
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
    # Test message in Myanmar language
    test_message = (
        "မင်္ဂလာပါ! IT Link CCTV, MATV, PABX မှ ကြိုဆိုပါတယ်ခင်ဗျာ။\n\n"
        "ကျွန်တော်တို့ IT Link အနေနဲ့ လူကြီးမင်းတို့ရဲ့ နေအိမ်နဲ့ လုပ်ငန်းခွင်တွေမှာ "
        "လုံခြုံရေးနဲ့ နည်းပညာပိုင်းဆိုင်ရာ လိုအပ်ချက်တွေကို အကောင်းဆုံး ဝန်ဆောင်မှု ပေးနေပါတယ်ခင်ဗျာ။\n\n"
        "ဝန်ဆောင်မှုများ -\n"
        "✅ CCTV Camera System\n"
        "✅ PABX Phone System\n"
        "✅ MATV Television System\n"
        "✅ Fingerprint & Door Access\n"
        "✅ WiFi & Networking\n"
        "✅ Fire Alarm System\n\n"
        "အသေးစိတ် သိရှိလိုပါက အောက်ပါဖုန်းနံပါတ်များသို့ ဆက်သွယ်စုံစမ်းနိုင်ပါတယ်ခင်ဗျာ။\n"
        "📞 09 425 298 539, 09 758 425 298 39\n\n"
        "#ITLink #CCTV #SecuritySystem #Myanmar #Technology"
    )
    
    print("Attempting to post to Facebook Page...")
    post_to_page(test_message)
