from fastapi import FastAPI
from pydantic import BaseModel
import os
import asyncio
from starlette.responses import StreamingResponse
from llama_cpp import Llama

app = FastAPI()

# Define paths to GGUF models
MODEL_PATHS = {
    "Llama 3.2 1B fine-tuned q4": "models/Llama3.2-1B-Q4_K_M-ft.gguf",
    "Qwen 2.5 0.5B fine-tuned q4" : "models/QWEN2.5-0.5B-Q4_K_M-ft.gguf",
}

# Dictionary for storing loaded models (Lazy Loading)
loaded_models = {}

def get_model(model_name):
    """Load a locally stored GGUF model only if not already loaded."""
    if model_name not in loaded_models:
        if model_name in MODEL_PATHS:
            print(f"🔄 Loading GGUF model: {model_name} from {MODEL_PATHS[model_name]}")
            loaded_models[model_name] = Llama(
                model_path=MODEL_PATHS[model_name],
                n_ctx=2048,  # Context window size
                n_threads=8,  # Adjust based on your CPU cores
                n_batch=512  # Optimize based on system performance
            )
        else:
            raise ValueError(f"❌ Model {model_name} not found in MODEL_PATHS!")

    return loaded_models[model_name]

# Request format
class Query(BaseModel):
    prompt: str
    model: str

def format_prompt(user_input, model_name):
    """Formats user input to match Unsloth fine-tuned chat structure"""
    if model_name in MODEL_PATHS:
        if "llama" in model_name.lower():
               return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
                        You are a light automation assistant. Convert user commands into structured automation outputs.
                        <|eot_id|><|start_header_id|>user<|end_header_id|>
                        {user_input}
                        <|eot_id|><|start_header_id|>assistant<|end_header_id|>
                        """
        elif "qwen" in model_name.lower():
             return f"""<|im_start|>system
                        You are a light automation assistant. Convert user commands into structured automation outputs.<|im_end|>
                        <|im_start|>user {user_input}<|im_end|>
                        <|im_start|>assistant
                        """

async def generate_stream(prompt, model_name):
    """ Generate response token by token in a streaming fashion using GGUF model. """
    model = get_model(model_name)
    
    # Format prompt correctly before passing to model
    formatted_prompt = format_prompt(prompt, model_name)

    # Generate tokens using the model
    stream = model(
        formatted_prompt, 
        max_tokens=300,  # Adjust based on needs
        stream=True  # Enable streaming for real-time output
    )

    # Yield response token by token
    for output in stream:
        yield output["choices"][0]["text"]  # Extract generated text
        await asyncio.sleep(0.05)  # Small delay for smoother streaming

@app.post("/generate")
async def generate_text(query: Query):
    """ API endpoint for text generation using locally stored GGUF models. """
    if query.model not in MODEL_PATHS:
        return {"error": "Invalid model selected"}

    return StreamingResponse(generate_stream(query.prompt, query.model), media_type="text/plain")
