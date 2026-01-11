import os
import httpx

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = "EXAVITQu4vr4xnSDxMaL" # Example voice ID (Rachel) or similar

async def generate_audio(text: str, output_path: str):
    """
    Generates audio from text using ElevenLabs API.
    """
    if not ELEVENLABS_API_KEY:
        print("WARNING: ELEVENLABS_API_KEY not found. Skipping TTS.")
        return None

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=data, headers=headers, timeout=30.0)
            if response.status_code == 200:
                with open(output_path, "wb") as f:
                    f.write(response.content)
                return output_path
            else:
                print(f"TTS Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"TTS Exception: {e}")
            return None
