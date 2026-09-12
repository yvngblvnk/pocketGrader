import sys
from structure_parser import extract_exam_skeleton, StructureExtractionError

if len(sys.argv) < 2:
    print("Usage: python test_structure_parser.py <path_to_exam_pdf>")
    sys.exit(1)

file_path = sys.argv[1]

try:
    skeleton = extract_exam_skeleton(file_path)
    print("\n--- Extracted Exam Skeleton ---")
    print(skeleton.model_dump_json(indent=2))
except StructureExtractionError as e:
    print(f"\n[FAILED] Structure extraction failed for '{file_path}': {e}")