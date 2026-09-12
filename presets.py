from typing import Dict
from schemas import ExamSkeleton, ExamSection, QuestionSlot, SubQuestionSlot

# 1. Standard 3-Section University Exam (100 Marks)
STANDARD_THREE_SECTION = ExamSkeleton(
    title="Standard University Exam",
    total_marks=100,
    time_allowed="3 HRS",
    instructions="Answer ALL questions in Section A and B. Answer ANY TWO questions in Section C.",
    sections=[
        ExamSection(
            section_name="Section A: Multiple Choice Questions",
            total_marks=20,
            questions=[
                QuestionSlot(question_number=f"Q{i}", total_marks=2, question_type="mcq")
                for i in range(1, 11)
            ]
        ),
        ExamSection(
            section_name="Section B: Short Answer Questions",
            total_marks=30,
            questions=[
                QuestionSlot(question_number=f"Q{i}", total_marks=6, question_type="short_answer")
                for i in range(1, 6)
            ]
        ),
        ExamSection(
            section_name="Section C: Essay & Analytical Questions",
            total_marks=50,
            questions=[
                QuestionSlot(
                    question_number="Q1",
                    total_marks=25,
                    question_type="essay",
                    sub_questions=[
                        SubQuestionSlot(label="a", marks=10),
                        SubQuestionSlot(label="b", marks=15)
                    ]
                ),
                QuestionSlot(
                    question_number="Q2",
                    total_marks=25,
                    question_type="essay",
                    sub_questions=[
                        SubQuestionSlot(label="a", marks=10),
                        SubQuestionSlot(label="b", marks=15)
                    ]
                )
            ]
        )
    ]
)

# 2. All Multiple Choice Exam (100 Marks)
ALL_MCQ = ExamSkeleton(
    title="Comprehensive MCQ Assessment",
    total_marks=100,
    time_allowed="1 HR 30 MINS",
    instructions="Select the single best answer for each question.",
    sections=[
        ExamSection(
            section_name="Multiple Choice Section",
            total_marks=100,
            questions=[
                QuestionSlot(question_number=f"Q{i}", total_marks=4, question_type="mcq")
                for i in range(1, 26)
            ]
        )
    ]
)

# 3. Comprehensive Essay Exam (100 Marks)
ALL_ESSAY = ExamSkeleton(
    title="Comprehensive Essay Examination",
    total_marks=100,
    time_allowed="3 HRS",
    instructions="Answer all 4 main essay questions. Ensure detailed explanations and diagrams where applicable.",
    sections=[
        ExamSection(
            section_name="Main Essay Section",
            total_marks=100,
            questions=[
                QuestionSlot(
                    question_number=f"QUESTION {i}",
                    total_marks=25,
                    question_type="essay",
                    sub_questions=[
                        SubQuestionSlot(label="a", marks=10),
                        SubQuestionSlot(label="b", marks=15)
                    ]
                )
                for i in range(1, 5)
            ]
        )
    ]
)

# 4. Quick Assessment Quiz (20 Marks)
QUICK_QUIZ = ExamSkeleton(
    title="Topic Mastery Quiz",
    total_marks=20,
    time_allowed="30 MINS",
    instructions="Answer all short answer questions briefly and concisely.",
    sections=[
        ExamSection(
            section_name="Short Quiz",
            total_marks=20,
            questions=[
                QuestionSlot(question_number=f"Q{i}", total_marks=4, question_type="short_answer")
                for i in range(1, 6)
            ]
        )
    ]
)

# Preset Library Mapping
PRESETS: Dict[str, ExamSkeleton] = {
    "standard_three_section": STANDARD_THREE_SECTION,
    "all_mcq": ALL_MCQ,
    "all_essay": ALL_ESSAY,
    "quick_quiz": QUICK_QUIZ,
}