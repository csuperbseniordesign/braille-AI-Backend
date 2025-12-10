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
    primarylabel: str
    sublabel: str

class StudentSchema(BaseModel):
    question1: str
    question2: str
    question3 : str
    characterQuestion1 : str
    characterQuestion2 : str
    characterQuestion3 : str
    characterQuestion4 : str
    experienceQuestion1 : str
    endingQuestion1 : str
    endingQuestion2 : str
    endingQuestion3 : str
    endingQuestion4 : str
    feedback : str
    teacher_question1 : str
    teacher_question2 : str
    teacher_question3: str
    teacher_question4: str
    teacher_question5: str
    teacher_question6: str
    teacher_question7: str
    teacher_feedback: str
    cr1_question: str
    cr1_result: int
    cr1_user_answer: str
    cr1_correct_answer: str
    cr2_question: str
    cr2_result: int
    cr2_user_answer: str
    cr2_correct_answer: str
    comprehension_score: int
    timeInSeconds: int
    modified_paragraph_id: int
    cr_avg: float
 



class StudentSchemaInital(BaseModel):
    code_id: str
    gradeLevel : str
    readingLevel : str
    ethnicity : str
    ethnic_subgroup : str
    gender: str
    hispanic_latino_origin : str
    birthPlace: str
    region: str
    primaryInterest: str
    mainlabel: str
    sublabel: str
    languages: str
    country: str
    vision: str
    preferredMedia: str
    appAccess: str
    digitalTextAccess: str
    year: str
    timeStamp: str
    

class ModifiedParagraphSchema(BaseModel):
    paragraph : str
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
    mainlabel : str
    sublabel : str
    code_id: str
    used: int
    cr_avg: int
    minAtos: float
    maxAtos: float
    original_paragraph_id: int

class StudentModifiedParagraphSchema(BaseModel):
    student_id : int
    modified_paragraph_id : int

class StudentCodeIdSchema(BaseModel):
    code_id: str