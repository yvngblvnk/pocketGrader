import json
import re as _re
import ollama
from parsers import parse_document
from schemas import ExamSkeleton
from structure_anchors import scan_structural_anchors

class StructureExtractionError(Exception):
    """Raised when exam structure extraction fails even after the retry attempt."""
    pass

def strip_json_fences(text: str) -> str:
    """Some models wrap JSON in ```json ... ``` even under schema constraints. Strip it defensively."""
    cleaned = text.strip()
    fence_match = _re.match(r'^```(?:json)?\s*(.*?)\s*```$', cleaned, _re.DOTALL)
    if fence_match:
        return fence_match.group(1).strip()
    return cleaned

def extract_exam_skeleton(file_path: str, model_name: str = "gemma3:4b") -> ExamSkeleton:
    parsed_pages = parse_document(file_path)
    full_text = "\n\n".join([f"[PAGE {p['page']}]\n{p['text']}" for p in parsed_pages])

    anchor_data = scan_structural_anchors(full_text)
    candidate_anchors = json.dumps(anchor_data["anchors"], indent=2)

    base_prompt = f"""
You are an exam structure validator. Your task is to CONFIRM and REFINE structural elements
that have already been detected — you are not inventing structure from scratch.

Raw Document Text:
--------------------
{full_text[:14000]}
--------------------

Pre-Detected Structural Anchors (Reference Ground Truth):
--------------------
{candidate_anchors}
--------------------

Each anchor may already include:
- "associated_marks": the marks value already correlated to that specific question/sub-question.
  Trust this value unless the raw text clearly contradicts it.
- "type_hint": a heuristic guess at question type ("mcq", "essay", "short_answer").
  Use this as a strong hint, but you may override it if the surrounding text clearly suggests otherwise.

INSTRUCTIONS:
1. Cross-reference the Raw Document Text with the Pre-Detected Anchors — do not invent anchors not supported by evidence.
2. Group question slots under the correct sections.
3. Use each anchor's "associated_marks" as the marks value unless clearly wrong.
4. Use each anchor's "type_hint" to inform "question_type" unless clearly wrong.
5. Ensure the sum of sub-question marks equals the parent question's total marks.
6. Do NOT generate, paraphrase, or summarize question text — structure only.
"""

    messages = [{"role": "user", "content": base_prompt}]

    response = ollama.chat(
        model=model_name,
        messages=messages,
        format=ExamSkeleton.model_json_schema(),
        options={"temperature": 0.0}
    )
    raw_json = response["message"]["content"]

    try:
        data = json.loads(strip_json_fences(raw_json))
        return ExamSkeleton(**data)
    except Exception as validation_error:
        print(f"\n[Validation Failed] Error: {validation_error}")
        print("Re-prompting model with specific error feedback for self-correction...")

        feedback_prompt = f"""
Your previous output failed validation with this exact error:
"{validation_error}"

Re-examine the document text and anchors, fix mark allocations or missing slots,
and respond with a corrected JSON object matching the schema.
"""
        messages.append({"role": "assistant", "content": raw_json})
        messages.append({"role": "user", "content": feedback_prompt})

        try:
            retry_response = ollama.chat(
                model=model_name,
                messages=messages,
                format=ExamSkeleton.model_json_schema(),
                options={"temperature": 0.0}
            )
            corrected_json = retry_response["message"]["content"]
            data = json.loads(strip_json_fences(corrected_json))
            return ExamSkeleton(**data)
        except Exception as retry_error:
            raise StructureExtractionError(
                f"Structure extraction failed after retry. "
                f"First error: {validation_error} | Retry error: {retry_error}"
            ) from retry_error