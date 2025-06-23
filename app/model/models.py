from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# table for preselected paragraph
class Paragraph(Base):
    __tablename__ = "paragraph"
    id = Column(Integer, primary_key=True, index=True,unique=True)
    title = Column(String(255), index=True)
    paragraph = Column(Text)
    word_count = Column(Integer)
    atos = Column(Float)
    q1 = Column(String(255))
    q1a1 = Column(String(255))
    q1a2 = Column(String(255))
    q1a3 = Column(String(255))
    q1a4 = Column(String(255))
    q2 = Column(String(255))
    q2a1 = Column(String(255))
    q2a2 = Column(String(255))
    q2a3 = Column(String(255))
    q2a4 = Column(String(255))
    interest = Column(String(255))

# table for student 
class Student(Base):
    __tablename__ = "student"

    id = Column(Integer, primary_key=True, index=True, unique=True, autoincrement=True)
    code_id = Column(String(255))
    gradeLevel = Column(String(255))
    readingLevel = Column(String(255))
    ethnicity = Column(String(255))
    gender = Column(String(255))
    familyBackground = Column(String(255))
    birthPlace = Column(String(255))
    region = Column(String(255))
    primaryInterest = Column(String(255))
    languages = Column(String(255))
    country = Column(String(255))
    vision = Column(String(255))
    preferredMedia = Column(String(255))
    appAccess = Column(String(255))
    digitalTextAccess = Column(String(255))
    year = Column(String(255))
    timeStamp = Column(String(255))

    question1 = Column(String(255))
    question2 = Column(String(255))
    question3 = Column(String(255))
    characterQuestion1 = Column(String(255))
    characterQuestion2 = Column(String(255))
    characterQuestion3 = Column(String(255))
    characterQuestion4 = Column(String(255))
    experienceQuestion1 = Column(String(255))
    endingQuestion1 = Column(String(255))
    endingQuestion2 = Column(String(255))
    endingQuestion3 = Column(String(255))
    endingQuestion4 = Column(String(255))
    blank = Column(String(255))
    teacher_question1 = Column(String(255))
    teacher_question2 = Column(String(255))
    teacher_question3 = Column(String(255))
    teacher_question4 = Column(String(255))
    teacher_question5 = Column(String(255))
    teacher_question6 = Column(String(255))
    teacher_question7 = Column(String(255))
    teacher_blank = Column(String(255))
    comprehension_score = Column(Integer)
    timeInSeconds = Column(Integer)     


# modified paragraph table
class ModifiedParagraph(Base):
    __tablename__ = "modified_paragraph"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    paragraph = Column(Text)
    # if used is 3, do not used this modified paragraph
    used = Column(Integer)
    cr_avg = Column(Float)
    ethnicity = Column(String(100))
    gender = Column(String(45))
    q1 = Column(String(255))
    q1a1 = Column(String(255))
    q1a2 = Column(String(255))
    q1a3 = Column(String(255))
    q1a4 = Column(String(255))
    q2 = Column(String(255))
    q2a1 = Column(String(255))
    q2a2 = Column(String(255))
    q2a3 = Column(String(255))
    q2a4 = Column(String(255)) 
    interest = Column(String(100))  
    code_id = Column(String(255))
    minAtos = Column(Float)
    maxAtos = Column(Float)
    original_paragraph_id = Column(Integer)