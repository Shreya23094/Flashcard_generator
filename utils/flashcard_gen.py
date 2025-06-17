import os
import json
import re
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def build_prompt(content: str, subject: str = "General") -> str:
    return f"""
You are an educational assistant generating flashcards for studying.

Generate exactly 10 flashcards from the given content.
Each flashcard should have a "question" and an "answer".

Return the flashcards in a valid JSON array format like:
[
  {{"question": "What is ...?", "answer": "..."}},
  ...
]

Subject: {subject}
Content:
{content}
"""

def generate_flashcards(content: str, subject: str = "General"):
    try:
        output = chain.invoke({"content": content, "subject": subject})
        text = output["text"] if isinstance(output, dict) else output
        print("=== Raw LLM Output ===\n", text)

        # Try extracting valid JSON array
        match = re.search(r"\[\s*{.*?}\s*]", text, re.DOTALL)
        if match:
            json_str = match.group(0).replace("“", "\"").replace("”", "\"").replace("‘", "'").replace("’", "'")
            return json.loads(json_str)

        # Fallback: Extract multiple {"question": "...", "answer": "..."} blocks
        items = re.findall(r'\{\s*"question"\s*:\s*".+?",\s*"answer"\s*:\s*".+?"\s*\}', text, re.DOTALL)
        flashcards = [json.loads(item.replace("“", "\"").replace("”", "\"")) for item in items]

        if flashcards:
            return flashcards
        else:
            print("No valid flashcards found.")
            return []

    except Exception as e:
        print("Flashcard generation failed:", e)
        return []
