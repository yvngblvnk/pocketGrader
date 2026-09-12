import json
import ollama
from parsers import parse_document
from schemas import ExamSkeleton

def extract_exam_skeleton(file_path: str, model_name: str = "gemma3:4b") -> ExamSkeleton:
    parsed_pages = parse_document(file_path)
    full_text = "\n\n".join([page["text"] for page in parsed_pages])

    prompt = f"""
You are a structural exam analyzer. Analyze the past exam text below and extract ONLY its structural blueprint.

STRICT INSTRUCTIONS:
1. Extract paper metadata: title ('CSC 4765 IT AUDIT AND CONTROLS'), time_allowed ('3 HRS'), total_marks (100), and general instructions.
2. Do NOT write or invent question text or descriptions.
3. Group all questions under 1 section named 'Main Section'.
4. Identify every question (QUESTION 1 through QUESTION 7) and extract the sub-question labels (e.g., '1a', '1b', '2a', '2b') and their mark allocations.

Exam Paper Text:
--------------------
{full_text}
--------------------
"""

    print(f"Extracting exam structure using model '{model_name}'...")

    response = ollama.chat(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        format=ExamSkeleton.model_json_schema(),
        options={"temperature": 0.0}
    )

    raw_json = response["message"]["content"]

    try:
        data = json.loads(raw_json)
        return ExamSkeleton(**data)
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw Ollama output was:\n{raw_json}")
        raise e