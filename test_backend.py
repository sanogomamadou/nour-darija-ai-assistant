import requests
import os

URL = "http://127.0.0.1:8000/chat"
AUDIO_FILE = "backend/audio_temp/356c14df-2dd0-4f4f-ad44-4e2614907058_input.wav"

if not os.path.exists(AUDIO_FILE):
    print(f"Error: {AUDIO_FILE} not found.")
    # Try finding any wav
    import glob
    files = glob.glob("backend/audio_temp/*.wav")
    if files:
        AUDIO_FILE = files[0]
        print(f"Using alternate file: {AUDIO_FILE}")
    else:
        exit(1)

try:
    with open(AUDIO_FILE, "rb") as f:
        files = {"audio": ("test.wav", f, "audio/wav")}
        data = {"session_id": "debug_script"}
        print(f"Sending request to {URL}...")
        response = requests.post(URL, files=files, data=data)
    
    print(f"Status Code: {response.status_code}")
    print("Response Body:")
    print(response.text)
except Exception as e:
    print(f"Request failed: {e}")
