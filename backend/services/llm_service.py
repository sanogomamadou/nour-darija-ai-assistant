import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from .prompts import SYSTEM_PROMPT, MEDICAL_INSTRUCTION, EMOTIONAL_INSTRUCTION, CRITICAL_ALERT

# Configuration for Local LLM (PC RTX 6GB)
MODEL_ID = "Qwen/Qwen2.5-3B-Instruct"

print(f"Loading LLM ({MODEL_ID}) on GPU...")

try:
    # 1. Quantization Config (4-bit to fit in 6GB VRAM)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )

    # 2. To avoid re-downloading, ensure you have >10GB disk space
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    model = AutoModelForCausalLM.from_pretrained(
        MODEL_ID,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True
    )
    print("LLM Model loaded successfully.")
except Exception as e:
    print(f"Error loading LLM: {e}")
    model = None
    tokenizer = None

async def generate_response(user_text: str, context: str = "", intent: str = "medical", history: list = []):
    if not model or not tokenizer:
        return {"text_fr": "Erreur Modèle", "text_darija": "Erreur Modèle", "user_fr": user_text}

    # Select Instruction
    if intent == "critical":
        instruction = CRITICAL_ALERT
    elif intent == "emotional":
        instruction = EMOTIONAL_INSTRUCTION
    else:
        instruction = MEDICAL_INSTRUCTION.format(context=context)

    # Prepare Messages (Chat Template)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "system", "content": instruction},
    ]
    
    # Inject History (Past interactions)
    for turn in history:
        messages.append(turn)

    # Append Current User Query
    messages.append({"role": "user", "content": user_text})

    try:
        # Apply Chat Template
        text_input = tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        model_inputs = tokenizer([text_input], return_tensors="pt").to("cuda")

        generated_ids = model.generate(
            **model_inputs,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1
        )
        
        # Decode only the new tokens
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]
        raw_output = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Parsing the structured output
        import re
        
        def extract_tag(text, tag):
            match = re.search(f"\[{tag}\](.*?)(\[|$)", text, re.DOTALL)
            return match.group(1).strip() if match else ""

        user_fr = extract_tag(raw_output, "USER_FR")
        text_fr = extract_tag(raw_output, "ASSISTANT_FR")
        text_darija = extract_tag(raw_output, "ASSISTANT_DARIJA")
        
        # Fallback if parsing fails (Model might have outputted raw text)
        if not text_darija:
            text_darija = raw_output # Assume raw output is Darija/Mix
            text_fr = raw_output # Fallback display
            
        return {
            "user_fr": user_fr,
            "text_fr": text_fr,
            "text_darija": text_darija,
            "raw": raw_output
        }

    except Exception as e:
        print(f"LLM Error (Local): {e}")
        return {
            "user_fr": user_text,
            "text_fr": "Erreur système.",
            "text_darija": "Smeh lia, wa9e3 chi mochkil.", 
            "raw": str(e)
        }
