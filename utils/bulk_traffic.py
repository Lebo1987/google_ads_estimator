import requests
from requests.auth import HTTPBasicAuth
import json

USERNAME = "info@leboapi.com"
PASSWORD = "a5562c0cd95b0d37"

def get_traffic_estimate(domain):
    url = "https://api.dataforseo.com/v3/dataforseo_labs/google/bulk_traffic_estimation/live"
    
    # לפי התמיכה, הפורמט הנכון הוא לשלוח מערך (list) בלבד עם אובייקט אחד שמכיל "targets" ו-"location_code"
    payload = [
        {
            "targets": [domain],
            "location_code": 2840
        }
    ]
    
    print("PAYLOAD BEING SENT:", json.dumps(payload))
    
    try:
        response = requests.post(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), json=payload)
        print("RESPONSE STATUS:", response.status_code)
        print("RESPONSE TEXT:", response.text)
        if response.status_code == 200:
            data = response.json()
            print("API DATA RETURNED:", json.dumps(data, indent=2))
            return data
        else:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": response.text
            }
    except Exception as e:
        return {
            "error": True,
            "message": str(e)
        }

if __name__ == "__main__":
    # להריץ לבדיקה
    print(get_traffic_estimate("cnn.com"))








