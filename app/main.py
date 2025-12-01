from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
import random
from fastapi.params import Header
from app.model.models import Paragraph, Student, ModifiedParagraph, StudentCodeId
from app.schema.schemas import ParagraphSchema, StudentSchema, ModifiedParagraphSchema, StudentSchemaInital, StudentCodeIdSchema
from sqlalchemy.orm import Session
from app.utils.data_formater import format_to_paragraph_object
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from app.database.database_service import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware


# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        with engine.connect() as connection:
            connection.execute(text('SELECT 1'))
        print("Connect to DB on startup")
    
    except OperationalError as e:
        print('Could not connect to DB')
        raise RuntimeError("DB not reachable") from e
    
    yield 

    # Shutdown login if needed
    print("Shutting down backend")

# Base.metadata.create_all(bind=engine)
app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://production.d28lo1xwcra81p.amplifyapp.com"],
    allow_credentials=True,
    allow_methods=["*"],                   
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# Dependency to verify code_id
def verify_code_id(student_code_id: str = Header(...), db: Session = Depends(get_db)):
    exists = db.query(StudentCodeId).filter(StudentCodeId.code_id == student_code_id).first()

    if not exists:
        raise HTTPException(status_code=404, detail="Invalid code_id")
    
    return student_code_id

# takes a json and upload it to the paragraphs table in mysql. Look at schemas.py for proper json entries
@app.post("/paragraphs/")
def create_paragraph(paragraph: ParagraphSchema, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    db_paragraph = Paragraph(**paragraph.model_dump())
    db.add(db_paragraph)
    db.commit()
    db.refresh(db_paragraph)
    return db_paragraph

## this is primarily the first endpoint when subject enter the student demographic form fields
## get json paragraph or modified paragraph based on interest and atos
## check modified paragraph table first and if used is < 3. otherwise, select from paragraph table
@app.get("/paragraphs/{interest}/{mainlabel}/{sublabel}/{min_atos}/{max_atos}/{ethnicity}/{gender}")
def read_paragraph(interest: str,mainlabel: str, sublabel: str,min_atos: float, max_atos : float, ethnicity : str, gender : str, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    # modified_query = db.query(ModifiedParagraph).filter(
    #     ModifiedParagraph.interest == interest,
    #     ModifiedParagraph.ethnicity == ethnicity,
    #     ModifiedParagraph.gender == gender,
    #     ModifiedParagraph.minAtos <= max_atos,
    #     ModifiedParagraph.maxAtos >= min_atos,
    #     # ModifiedParagraph.used < 3
    # ).all()
    # if modified_query:
    #     random_modified = random.choice(modified_query)
    #     return {"source" : "modified_paragraph", "data" : random_modified}         
                
    query = db.query(Paragraph)
    query = query.filter(Paragraph.atos.between(min_atos, max_atos))
    query = query.filter(Paragraph.interest == interest)
    query = query.filter(Paragraph.mainlabel == mainlabel)
    query = query.filter(Paragraph.sublabel == sublabel)
    paragraph = query.all()
    if not paragraph:
        raise HTTPException(status_code=404, detail="Paragraph not found")
    return {"source" : "paragraph", "data" : random.choice(paragraph)}
  

# Returns questions from a specific paragraph with the requested name
@app.get("/paragraph/{paragraph_id}/{name}")
def get_paragraph(paragraph_id: int, name: str, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    paragraph = db.query(Paragraph).filter(Paragraph.id == paragraph_id).first()
    
    if not paragraph:
        print(f"Paragraph with ID {paragraph_id} not found.")  # Logs the issue
        raise HTTPException(status_code=404, detail=f"Paragraph {paragraph_id} not found")
    
    print(f'paragraph {paragraph.paragraph}')
    print(f'name {name}')
    formatted_paragraph = format_to_paragraph_object(paragraph, name)
    
    
    return formatted_paragraph

# used in demographic form
# check StudentSchemaInital from schemas.py to know which json field to pass
@app.post("/students/")
def create_student_initial(student: StudentSchemaInital, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    # create student entry
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student.id

# add in the rest of the student entry for student table.check studentSchema in models.py.
# increment the modify paragraph using the id "used" value.
# add entry for student_modified_paragraph table. 
# takes a json and upload it to the students table in mysql. Look at schemas.py for proper json entries
@app.put("/students/{student_id}")
def update_student_partial(student_id: int, update_data : StudentSchema, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    student = db.query(Student).filter(Student.id == student_id).first()

    if not student:
        raise HTTPException(status_code=404, detail="Student not Found")
    
    for key, value in update_data.model_dump().items():
        setattr(student, key, value)
    
    
    modified_paragraph = db.query(ModifiedParagraph).filter_by(id=student.modified_paragraph_id).first()
    if modified_paragraph:
        modified_paragraph.used += 1

        if modified_paragraph.used == 1:
            modified_paragraph.cr_avg = student.cr_avg
        
        else:
            modified_paragraph.cr_avg = ((modified_paragraph.cr_avg * (modified_paragraph.used-1)) + student.cr_avg) / modified_paragraph.used
        db.add(modified_paragraph)

    db.commit()
    db.refresh

    
    
    # student = db.query(Student).filter(Student.id == student_id).first()
    # if not student:
    #     raise HTTPException(status_code=404, detail="Student not found")
    
    # for key, value in update_data.model_dump().items():
    #     setattr(student, key, value)
    # # create student_modified_paragraph entry based on the two id from student
    # link = StudentModifiedParagraph(
    #     student_id = student.id,
    #     modified_paragraph_id = student.modified_paragraph_id
    # )
    # db.add(link)
    # # update the used value for the modified paragraph along with cr_avg
    # modified = db.query(ModifiedParagraph).filter_by(id=student.modified_paragraph_id).first()
    # if modified:
    #     modified.used += 1
    #     if modified.used == 1:
    #         modified.cr_avg = (student.cr1_result + student.cr2_result + student.cr3_result + student.cr4_result +
    #                         student.cr5_result + student.cr6_result + student.cr7_result + student.cr8_result) / 8
    #     else:
    #         next_avg = (student.cr1_result + student.cr2_result + student.cr3_result + student.cr4_result +
    #                         student.cr5_result + student.cr6_result + student.cr7_result + student.cr8_result) /8
    #         modified.cr_avg = ((modified.cr_avg * (modified.used-1)) + next_avg) / modified.used
    #     db.add(modified)
    # db.commit()
    # db.refresh
    

@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# second endpoint to be used. store the modify paragraph entry
# takes a json and upload it to the modified_paragraphs table in mysql. Look at schemas.py for proper json entries
@app.post("/modified_paragraphs/")
def create_modified_paragraph(modified_paragraph: ModifiedParagraphSchema, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    db_modified_paragraph = ModifiedParagraph(**modified_paragraph.model_dump(exclude={"modified_paragraph_links"}))
    db.add(db_modified_paragraph)
    db.commit()
    db.refresh(db_modified_paragraph)
    return db_modified_paragraph

@app.get("/modified_paragraphs/{modified_paragraph_id}")
def read_modified_paragraph(modified_paragraph_id: int, db: Session = Depends(get_db), code_id: str = Depends(verify_code_id)):
    modified_paragraph = db.query(ModifiedParagraph).filter(ModifiedParagraph.id == modified_paragraph_id).first()
    if not modified_paragraph:
        raise HTTPException(status_code=404, detail="Modified Paragraph not found")
    return modified_paragraph

# #########################################################################################
# # helper function to work with @app.post("/link_student_modified_paragraphs/")
# def link_student_and_paragraph(student_id: int, paragraph_id: int, db: Session):
#     link = StudentModifiedParagraph(
#         student_id=student_id,
#         modified_paragraph_id=paragraph_id
#     )
#     db.add(link)
#     db.commit()
#     db.refresh(link)
#     return link

# # take a json and upload it to modified_paragraph_student table in mysql.
# @app.post("/link_student_modified_paragraphs/")
# def link_student_paragraph(link: StudentModifiedParagraphSchema, db: Session = Depends(get_db)):
#     return link_student_and_paragraph(link.student_id, link.modified_paragraph_id, db)

# #################################################################################################
