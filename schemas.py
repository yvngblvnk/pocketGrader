from typing import List, Optional
from pydantic import BaseModel, Field

class SubQuestionSlot(BaseModel):
    label: str = Field(description="Sub-question label, e.g., '1a', '2b', '1.a'")
    marks: int = Field(description="Marks allocated for this specific sub-question")

class QuestionSlot(BaseModel):
    question_number: str = Field(description="Main question label, e.g., 'QUESTION 1'")
    total_marks: int = Field(description="Total marks for this question slot, e.g., 20")
    question_type: str = Field(description="Question style: 'short_answer', 'essay', or 'multiple_choice'")
    sub_questions: Optional[List[SubQuestionSlot]] = Field(default=None, description="List of sub-question mark allocations")

class ExamSection(BaseModel):
    section_name: str = Field(description="Section title or main grouping, e.g., 'Main Exam Paper'")
    total_marks: int = Field(description="Total marks allocated for this section")
    questions: List[QuestionSlot] = Field(description="List of question slots")

class ExamSkeleton(BaseModel):
    title: str = Field(description="Course or exam title")
    total_marks: int = Field(description="Total exam marks")
    time_allowed: Optional[str] = Field(description="Time limit, e.g., '3 HRS'")
    instructions: Optional[str] = Field(description="General exam instructions")
    sections: List[ExamSection] = Field(description="Sections breakdown")