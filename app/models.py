from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Text, Boolean, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# load from .env file
load_dotenv()

# database credentials
MYSQL_USER = "apcsa2020"# os.getenv("MYSQL_USER")
MYSQL_PASSWORD = "csulasuperb_2025"# os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = "47.33.78.253"# os.getenv("MYSQL_HOST")
MYSQL_DB = "Braille_AI"# os.getenv("MYSQL_DB")
MYSQL_PORT = 3306# os.getenv("MYSQL_PORT")

# database url
DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"

# set up SQLAlchemy
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)
Base = declarative_base()

# table for preselected paragraph
class Paragraph(Base):
    __tablename__ = "paragraphs"
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
    id = Column(Integer, primary_key=True,index=True,unique=True,autoincrement=True)
    grade = Column(String(45))
    ethnicity = Column(String(100))
    gender = Column(String(45))
    q1_result = Column(Boolean)
    q2_result = Column(Boolean)
    cr1_result = Column(Integer)
    cr2_result = Column(Integer)
    cr3_result = Column(Integer)
    cr4_result = Column(Integer)
    cr5_result = Column(Integer)
    cr6_result = Column(Integer)
    cr7_result = Column(Integer)
    cr8_result = Column(Integer)
    interest = Column(String(100))
    born = Column(String(255))
    region = Column(String(255))
    year = Column(Integer)
    modified_paragraph_id = Column(Integer)
    reading_grade = Column(String(45))
    from_SA = Column(Boolean)
    modified_paragraph_links = relationship(
        "StudentModifiedParagraph",
        back_populates = "student"
    )

# modified paragraph table
class ModifiedParagraph(Base):
    __tablename__ = "modified_paragraph"
    id = Column(Integer, primary_key=True, index=True, unique=True)
    paragraph = Column(Text)
    atos = Column(Float)
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

    student_links = relationship(
        "StudentModifiedParagraph",
        back_populates= "modified_paragraph"
    )

# modified paragraph and student table. many to many relationship table
class StudentModifiedParagraph(Base):
    __tablename__ = "student_modified_paragraph"
    student_id = Column(Integer, ForeignKey("student.id"), primary_key=True)
    modified_paragraph_id = Column(Integer, ForeignKey("modified_paragraph.id"), primary_key=True)
    student = relationship("Student", back_populates="modified_paragraph_links")
    modified_paragraph = relationship("ModifiedParagraph", back_populates="student_links")







