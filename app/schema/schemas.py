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
    blank : str
    teacher_question1 : str
    teacher_question2 : str
    teacher_question3: str
    teacher_question4: str
    teacher_question5: str
    teacher_question6: str
    teacher_question7: str
    teacher_blank: str
    comprehension_score: int
    timeInSeconds: int
    modified_paragraph_id: int
    cr_avg: float



class StudentSchemaInital(BaseModel):
    code_id: str
    gradeLevel : str
    readingLevel : str
    ethnicity : str
    gender: str
    familyBackground: str
    birthPlace: str
    region: str
    primaryInterest: str
    languages: str
    country: str
    vision: str
    preferredMedia: str
    appAccess: str
    otherAppAccess: str
    digitalTextAccess: str
    otherDigitalAccess: str
    year: str
    

class ModifiedParagraphSchema(BaseModel):
    paragraph : str
    atos : float
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