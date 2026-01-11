import os
from faster_whisper import WhisperModel

# Configuration
MODEL_SIZE = "small" # "tiny", "base", "small", "medium", "large-v3"
DEVICE = "cuda" # or "cpu"
COMPUTE_TYPE = "float16" # "int8" for CPU

# Initialize Model (Lazy loading or persistent)
# For POC, we initialize it globally to avoid reloading delays
print(f"Loading Faster-Whisper ({MODEL_SIZE}) on {DEVICE}...")
try:
    model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
    print("STT Model loaded successfully.")
except Exception as e:
    print(f"Error loading STT Model: {e}")
    model = None

async def transcribe_audio(file_path: str):
    """
    Transcribes audio using local Faster-Whisper.
    """
    if not model:
        print("STT Model not initialized.")
        return ""

    if not os.path.exists(file_path):
        return ""

    try:
        segments, info = model.transcribe(file_path, beam_size=5)
        
        # Merge segments into one string
        full_text = " ".join([segment.text for segment in segments])
        return full_text.strip()

    except Exception as e:
        print(f"STT Error (Local): {e}")
        return ""
