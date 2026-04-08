import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def classify_result(result):
    expected = result["expected"]
    actual = result["actual"]

    prompt = f"""You are an AI evaluation expert. Given an expected answer and an actual answer, determine if the actual answer is correct and classify any hallucination.

Expected answer: {expected}
Actual answer: {actual}

Classify the result as one of:
- CORRECT: The actual answer contains the expected answer
- FACTUAL_ERROR: The answer is confidently wrong
- WRONG_DETAIL: Right topic but wrong specific detail
- CONFIDENT_WRONGNESS: Wrong answer stated with high confidence and no uncertainty
- MADE_UP_SOURCE: References a source that likely doesn't exist

Respond only in this JSON format with no extra text or newlines inside values:
{{"classification": "CORRECT or one of the error types", "explanation": "one sentence explanation"}}"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.choices[0].message.content.strip()
    
    # Strip markdown code blocks if present
    raw = re.sub(r'```json|```', '', raw).strip()
    
    # Remove control characters
    raw = re.sub(r'[\x00-\x1f\x7f]', ' ', raw)

    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback if JSON still fails
        parsed = {
            "classification": "CORRECT" if result["expected"].lower() in result["actual"].lower() else "FACTUAL_ERROR",
            "explanation": "Auto-classified due to JSON parse error"
        }

    return {
        **result,
        "classification": parsed["classification"],
        "explanation": parsed["explanation"]
    }

def classify_all(results):
    classified = []
    for result in results:
        print(f"Classifying {result['id']}...")
        classified.append(classify_result(result))
    return classified