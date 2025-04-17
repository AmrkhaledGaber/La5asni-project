import json
import os
import re
from dotenv import load_dotenv
from groq import Groq
from app.models.schemas import AnalysisResponse

# ✅ Load environment variables from .env
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# ✅ Create Groq client
client = Groq(api_key=groq_api_key)

def analyze_document(text: str) -> AnalysisResponse:
    # 🧠 Prompt with fixed format instruction
    prompt = f"""
You are an expert instructional designer.

Analyze the following training document and return only a valid JSON in the following format:

{{
  "summary": "string",
  "key_points": ["point1", "point2", "..."],
  "training_modules": ["module1", "module2", "..."],
  "num_pages": integer,
  "useful_text_ratio": float (between 0 and 1),
  "num_key_points": integer,
  "estimated_minutes_per_module": [int, int, ...]  // same length as training_modules
}}

Document:
{text}
"""


    # 🔁 Call Groq model
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=2048,  # limit response size
    )

    raw_content = response.choices[0].message.content
    print("\n🟡 Groq LLM Raw Output:\n", raw_content)

    try:
        # ✅ Extract only the first JSON object (non-greedy)
        json_match = re.search(r"\{.*?\}", raw_content, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON block found in the response.")

        clean_json = json_match.group(0)
        parsed = json.loads(clean_json)

        # ✅ Return as Pydantic model
        return AnalysisResponse(**parsed)

    except Exception as e:
        print("❌ Error parsing Groq response:", e)
        raise RuntimeError("Failed to parse Groq response as valid JSON.")
