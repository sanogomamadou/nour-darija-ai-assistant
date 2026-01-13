import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configuration for STT (Separate Key)
GEMINI_STT_API_KEY = os.getenv("GEMINI_STT_API_KEY")

# If STT key is not present, fallback to main key or warn
if not GEMINI_STT_API_KEY:
    GEMINI_STT_API_KEY = os.getenv("GEMINI_API_KEY")
    if GEMINI_STT_API_KEY:
        print("INFO: GEMINI_STT_API_KEY not found, using GEMINI_API_KEY.")
    else:
        print("WARNING: No valid API KEY found for STT.")

if GEMINI_STT_API_KEY:
    # Configure a separate client instance? 
    # The global configuration might conflict if we want distinct keys for simultaneous usage with different configs.
    # However, google-generativeai v0.3+ usually relies on global `genai.configure`.
    # To support two keys safely in the same process with this SDK version, we might need to re-configure or use Client objects if available (v0.4+).
    # For now, we will re-configure before the call if needed, or assume the user might want same key if they copy-pasted.
    pass

async def transcribe_audio(file_path: str):
    """
    Transcribes audio using Gemini File API.
    """
    if not os.path.exists(file_path):
        return ""

    if not GEMINI_STT_API_KEY:
        print("STT Error: No API Key provided.")
        return ""

    try:
        # Re-configure with STT key just to be safe for this specific call context
        genai.configure(api_key=GEMINI_STT_API_KEY)
        
        print(f"Uploading audio for STT: {file_path}")
        audio_file = genai.upload_file(path=file_path)
        
        # Determine model - using 2.5 Flash for best speed/quality
        model = genai.GenerativeModel("gemini-2.5-flash")
        
        prompt = """
        Listen to this audio. It is a conversation in Moroccan Darija and/or French.
        Transcribe exactly what is said. 
        - Do NOT translate.
        - Output ONLY the transcription.
        - If the audio is silent or unintelligible, output empty string.
        """
        
        response = model.generate_content([prompt, audio_file])
        
        # Cleanup
        # audio_file.delete() # Optional: delete from Gemini servers if needed, usually auto-expiring or we can leave it.
        
        text = response.text.strip()
        print(f"STT Result: {text}")
        return text

    except Exception as e:
        print(f"STT Error (Gemini): {e}")
        return ""
