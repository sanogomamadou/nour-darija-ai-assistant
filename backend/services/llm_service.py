import os
import google.generativeai as genai
from .prompts import SYSTEM_PROMPT, MEDICAL_INSTRUCTION, EMOTIONAL_INSTRUCTION, CRITICAL_ALERT
from dotenv import load_dotenv
import re

load_dotenv()

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_ID = "gemini-2.5-flash"

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"Gemini API configured with model: {MODEL_ID}")
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

async def generate_response(user_text: str, context: str = "", intent: str = "medical", history: list = []):
    if not GEMINI_API_KEY:
        return {"text_fr": "Clé API manquante", "text_darija": "Kayn mochkil f system.", "user_fr": user_text}

    # Select Instruction
    if intent == "critical":
        instruction = CRITICAL_ALERT
    elif intent == "emotional":
        instruction = EMOTIONAL_INSTRUCTION
    else:
        instruction = MEDICAL_INSTRUCTION.format(context=context)

    # Combine System Prompts
    full_system_instruction = f"{SYSTEM_PROMPT}\n\n{instruction}"

    try:
        model = genai.GenerativeModel(
            model_name=MODEL_ID,
            system_instruction=full_system_instruction,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                top_p=0.9,
                max_output_tokens=1024,
            )
        )

        # Convert History to Gemini Format
        chat_history = []
        for turn in history:
            role = "user" if turn["role"] == "user" else "model"
            # Ensure content is string
            content = str(turn.get("content", ""))
            chat_history.append({"role": role, "parts": [content]})

        # Start Chat Session
        chat = model.start_chat(history=chat_history)
        
        # specific instructions for format can be reinforced in the prompt if needed, 
        # but are already in system prompt.
        response = await chat.send_message_async(user_text)
        raw_output = response.text

        # Parsing the structured output
        def extract_tag(text, tag):
            match = re.search(r"\[{}\](.*?)(\[|$)".format(tag), text, re.DOTALL)
            return match.group(1).strip() if match else ""

        user_fr = extract_tag(raw_output, "USER_FR")
        text_fr = extract_tag(raw_output, "ASSISTANT_FR")
        text_darija = extract_tag(raw_output, "ASSISTANT_DARIJA")
        
        # Fallback if parsing fails
        if not text_darija:
            # Try to see if the model outputted just text or failed format
            text_darija = raw_output
            text_fr = raw_output 
            
        return {
            "user_fr": user_fr if user_fr else user_text,
            "text_fr": text_fr,
            "text_darija": text_darija,
            "raw": raw_output
        }

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return {
            "user_fr": user_text,
            "text_fr": "Service indisponible momentanément.",
            "text_darija": "Samhi liya, kayn mochkil f reseau.", 
            "raw": str(e)
        }
