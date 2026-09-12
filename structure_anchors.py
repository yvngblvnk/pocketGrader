import re
from typing import Dict, List, Any, Optional
from pydantic import BaseModel

class RawAnchor(BaseModel):
    anchor_type: str  # 'section', 'question', 'sub_question'
    matched_text: str
    line_number: int
    associated_marks: Optional[int] = None   # Marks tied directly to this anchor
    type_hint: Optional[str] = None          # 'mcq', 'essay', 'short_answer', or None

SECTION_RE = re.compile(r'(SECTION|PART)\s+([A-Z\d]+)', re.IGNORECASE)
QUESTION_RE = re.compile(r'^\s*(QUESTION\s+\d+|\d+\.)', re.IGNORECASE)
# Excludes "e.g." / "i.e." style false positives via negative lookahead on common abbreviations
SUB_Q_RE = re.compile(r'^\s*(\([a-z]\)|\([ivx]+\)|\d+\.[a-z]\b)(?!\.\s?[a-z]\.)', re.IGNORECASE)
MARKS_RE = re.compile(r'\[\s*(\d+)\s*marks?\s*\]|\(\s*(\d+)\s*marks?\s*\)|\b(\d+)\s*marks?\b', re.IGNORECASE)

# Heuristic type hints — evidence for the model to lean on
MCQ_HINT_RE = re.compile(r'\b[A-D]\)\s|\bchoose\s+the\s+correct\b|\bselect\s+one\b', re.IGNORECASE)
ESSAY_HINT_RE = re.compile(r'\bdiscuss\b|\bexplain\s+in\s+detail\b|\bcritically\s+evaluate\b|\bessay\b', re.IGNORECASE)
SHORT_HINT_RE = re.compile(r'\bdefine\b|\bstate\b|\blist\b|\bname\b', re.IGNORECASE)

def _extract_marks(line: str) -> Optional[int]:
    m = MARKS_RE.search(line)
    if not m:
        return None
    return int(next(g for g in m.groups() if g is not None))

def _extract_type_hint(line: str) -> Optional[str]:
    if MCQ_HINT_RE.search(line):
        return "mcq"
    if ESSAY_HINT_RE.search(line):
        return "essay"
    if SHORT_HINT_RE.search(line):
        return "short_answer"
    return None

def scan_structural_anchors(raw_text: str) -> Dict[str, Any]:
    lines = raw_text.splitlines()
    anchors: List[RawAnchor] = []
    detected_questions_count = 0
    last_owning_anchor: Optional[RawAnchor] = None  # tracks the most recent question/sub_question

    for idx, line in enumerate(lines, start=1):
        clean = line.strip()
        if not clean:
            continue

        marks_on_this_line = _extract_marks(clean)

        if SECTION_RE.search(clean):
            anchor = RawAnchor(anchor_type='section', matched_text=clean, line_number=idx)
            anchors.append(anchor)
            last_owning_anchor = None  # sections don't "own" marks directly

        elif QUESTION_RE.search(clean):
            detected_questions_count += 1
            anchor = RawAnchor(
                anchor_type='question', matched_text=clean, line_number=idx,
                associated_marks=marks_on_this_line,
                type_hint=_extract_type_hint(clean)
            )
            anchors.append(anchor)
            last_owning_anchor = anchor

        elif SUB_Q_RE.search(clean):
            anchor = RawAnchor(
                anchor_type='sub_question', matched_text=clean, line_number=idx,
                associated_marks=marks_on_this_line,
                type_hint=_extract_type_hint(clean)
            )
            anchors.append(anchor)
            last_owning_anchor = anchor

        elif marks_on_this_line is not None and last_owning_anchor is not None:
            # Marks appeared on their own line — attach to the most recent question/sub-question
            if last_owning_anchor.associated_marks is None:
                last_owning_anchor.associated_marks = marks_on_this_line

    return {
        "anchors": [a.model_dump() for a in anchors],
        "estimated_question_count": detected_questions_count
    }