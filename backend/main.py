from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os
import shutil
import uuid

load_dotenv()

# Import Services
from services.stt_service import transcribe_audio
from services.llm_service import generate_response
from services.rag_service import retrieve_context
from services.tts_service import generate_audio

app = FastAPI(title="Nour Chatbot API", version="0.1.0")

# CORS Configuration
origins = [
    "http://localhost:5173", # Vite default port
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AUDIO_DIR = "audio_temp"
os.makedirs(AUDIO_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to Nour Chatbot API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# In-Memory Session Storage (For POC)
SESSION_MEMORY = {}

@app.post("/chat")
async def chat_endpoint(
    audio: UploadFile = File(...),
    session_id: str = Form(...) # Received from frontend
):
    # Retrieve History
    if session_id not in SESSION_MEMORY:
        SESSION_MEMORY[session_id] = []
    
    history = SESSION_MEMORY[session_id]

    # Generate temp file path
    unique_id = str(uuid.uuid4())
    input_audio_path = os.path.join(AUDIO_DIR, f"{unique_id}_input.wav")
    
    # Save Uploaded Audio
    with open(input_audio_path, "wb") as buffer:
        shutil.copyfileobj(audio.file, buffer)
    
    # 1. STT
    user_text = await transcribe_audio(input_audio_path)
    print(f"Transcription: {user_text}")
    
    if not user_text:
        return {"error": "Transcription failed or empty"}

    # 2. Intent & RAG
    context = retrieve_context(user_text)
    
    # 3. LLM Generation (with History)
    intent = "medical"
    if "fatigue" in user_text.lower() or "peur" in user_text.lower() or "khal3a" in user_text.lower():
        intent = "emotional"
    
    llm_output = await generate_response(user_text, context, intent=intent, history=history)
    
    # Handle structured output
    if isinstance(llm_output, dict):
        response_text_display = llm_output.get("text_fr", "")
        response_text_tts = llm_output.get("text_darija", "")
        user_text_display = llm_output.get("user_fr", user_text)
    else:
        response_text_display = str(llm_output)
        response_text_tts = str(llm_output)
        user_text_display = user_text

    # Update History (Append new turn)
    # We store the French version for better context retention in the LLM
    SESSION_MEMORY[session_id].append({"role": "user", "content": user_text_display}) 
    SESSION_MEMORY[session_id].append({"role": "assistant", "content": response_text_display})
    
    # Keep history manageable (last 10 turns)
    if len(SESSION_MEMORY[session_id]) > 10:
        SESSION_MEMORY[session_id] = SESSION_MEMORY[session_id][-10:]

    print(f"Response (Display): {response_text_display}")
    
    # 4. TTS (Use Darija Version)
    output_audio_path = os.path.join(AUDIO_DIR, f"{unique_id}_output.mp3")
    audio_file = await generate_audio(response_text_tts, output_audio_path)
    
    return {
        "user_text": user_text_display,
        "original_user_text": user_text,
        "response_text": response_text_display,
        "audio_url": f"/audio/{os.path.basename(output_audio_path)}" if audio_file else None
    }

@app.get("/audio/{filename}")
async def get_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return {"error": "File not found"}
