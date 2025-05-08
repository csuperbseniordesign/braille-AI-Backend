from pydantic import BaseModel

class ParagraphSchema(BaseModel):
    title: str
    paragraph: str
    word_count : int
    atos: float
    q1: str
    q1a1: str
    q1a2: str
    q1a3: str
    q1a4: str
    q2: str
    q2a1: str
    q2a2: str
    q2a3: str
    q2a4: str
    interest: str

class StudentSchema(BaseModel):
    q1_result: int
    q2_result: int
    cr1_result : int
    cr2_result : int
    cr3_result : int
    cr4_result : int
    cr5_result : int
    cr6_result : int
    cr7_result : int
    cr8_result : int
    modified_paragraph_id : int


class StudentSchemaInital(BaseModel):
    grade : str
    reading_grade : str
    gender : str
    ethnicity : str
    ethnicity_subgroup : str
    from_NA : int
    born : str
    year : int
    region : str
    interest : str

class ModifiedParagraphSchema(BaseModel):
    paragraph : str
    atos : float
    used : int
    cr_avg: float
    ethnicity :str
    gender : str
    q1 : str
    q1a1 : str
    q1a2 : str
    q1a3 : str
    q1a4 : str
    q2 : str
    q2a1 : str
    q2a2 : str
    q2a3 : str
    q2a4 : str
    interest : str

class StudentModifiedParagraphSchema(BaseModel):
    student_id : int
    modified_paragraph_id : int