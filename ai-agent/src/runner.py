import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a precise factual assistant. Before answering, 
carefully consider whether the question contains any common misconceptions 
or misleading assumptions. Answer only with the specific fact requested."""

def run_test_case(test_case, use_system_prompt=True, retries=5):
    messages = []
    
    if use_system_prompt:
        messages.append({
            "role": "system",
            "content": SYSTEM_PROMPT
        })
    
    messages.append({
        "role": "user",
        "content": test_case["prompt"]
    })

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=messages
            )
            return {
                "id": test_case["id"],
                "prompt": test_case["prompt"],
                "expected": test_case["expected"],
                "actual": response.choices[0].message.content,
                "category": test_case["category"]
            }
        except Exception as e:
            wait = 2 ** attempt
            print(f"  Error on {test_case['id']} (attempt {attempt+1}): retrying in {wait}s...")
            time.sleep(wait)

    # If all retries fail return a placeholder
    return {
        "id": test_case["id"],
        "prompt": test_case["prompt"],
        "expected": test_case["expected"],
        "actual": "ERROR: could not get response after retries",
        "category": test_case["category"]
    }

def run_all_tests(test_cases, use_system_prompt=True):
    results = []
    for test in test_cases:
        print(f"Running {test['id']}...")
        result = run_test_case(test, use_system_prompt)
        results.append(result)
    return results