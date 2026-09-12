import sys
from structure_parser import extract_exam_skeleton

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_structure_parser.py <path_to_past_paper>")
        return

    file_path = sys.argv[1]
    print(f"Processing past paper: {file_path}...\n")

    skeleton = extract_exam_skeleton(file_path)

    print("\n=== Extracted Exam Skeleton ===")
    print(f"Title: {skeleton.title}")
    print(f"Total Marks: {skeleton.total_marks}")
    print(f"Time Allowed: {skeleton.time_allowed}")
    print(f"Instructions: {skeleton.instructions}")
    print(f"Number of Sections: {len(skeleton.sections)}\n")

    for section in skeleton.sections:
        print(f"[{section.section_name}] ({section.total_marks} Marks)")
        print(f"Question Count: {len(section.questions)}")
        for q in section.questions:
            print(f"  - {q.question_number} ({q.question_type}, {q.total_marks} marks total)")
            if q.sub_questions:
                for sub in q.sub_questions:
                    print(f"      * {sub.label}: {sub.marks} marks")
        print("-" * 40)

if __name__ == "__main__":
    main()