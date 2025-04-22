from app.utils.auth import verify_api_key, fetch_model_api_key
from app.utils.sys_check import run_system_check
from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.security.api_key import APIKeyHeader
import httpx
import json
import random
from app.models import Base, Paragraph, Student, ModifiedParagraph, StudentModifiedParagraph, engine, SessionLocal
from app.schemas import ParagraphSchema, StudentSchema, ModifiedParagraphSchema, StudentModifiedParagraphSchema
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.utils.data_formater import format_to_paragraph_object

run_system_check()
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Allow only this origin (frontend)
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow only these methods
    allow_headers=["*"],  # Allow any headers
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

@app.get("/secure-data")
def secure_data(api_key: str = Depends(verify_api_key)):
    return {"message": "You have access to secure data"}

@app.get("/generate")
async def generate_text(request: Request):
    # extract raw json data
    data = await request.json()
    

    # check if prompt exist
    prompt = data.get("prompt")

    # if prompt doesn't exist
    # return error notify no prompt is given
    if not prompt:
        return {"error" : "Prompt is required"}
    
    json_data = json.dumps(data)
    model_key = fetch_model_api_key()
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(model_key, data=json_data)

            if response.status_code != 200:
                return {"response" : response.status_code}
            
        except:
            return {"error" : "unable to connect to local model"}

        # convert response.text to json from string
        response_json = json.loads(response.text)

        return response_json

# takes a json and upload it to the paragraphs table in mysql. Look at schemas.py for proper json entries
@app.post("/paragraphs/")
def create_paragraph(paragraph: ParagraphSchema, db: Session = Depends(get_db)):
    db_paragraph = Paragraph(**paragraph.model_dump())
    db.add(db_paragraph)
    db.commit()
    db.refresh(db_paragraph)
    return db_paragraph

## this is primarily the first endpoint when subject enter the student demographic form fields
## get json paragraph or modified paragraph based on interest and atos
## check modified paragraph table first and if used is < 3. otherwise, select from paragraph table
@app.get("/paragraphs/{interest}/{min_atos}/{max_atos}/{ethnicity}/{gender}")
def read_paragraph(interest: str,min_atos: float, max_atos : float, ethnicity : str, gender : str, db: Session = Depends(get_db)):
    modified_query = db.query(ModifiedParagraph).filter(
        ModifiedParagraph.interest == interest,
        ModifiedParagraph.ethnicity == ethnicity,
        ModifiedParagraph.gender == gender,
        ModifiedParagraph.atos.between(min_atos,max_atos),
        ModifiedParagraph.used < 3
    ).all()
    if modified_query:
        random_modified =random.choice(modified_query)
        return {"source" : "modified_paragraph", "data" : random_modified}         
                
    query = db.query(Paragraph)
    query = query.filter(Paragraph.atos.between(min_atos, max_atos))
    query = query.filter(Paragraph.interest == interest)
    paragraph = query.all()
    if not paragraph:
        raise HTTPException(status_code=404, detail="Paragraph not found")
    return {"source" : "paragraph", "data" : random.choice(paragraph)}
  

@app.get("/paragraph/{paragraph_id}/{name}/{gender}")
def get_paragraph(paragraph_id: int, db: Session = Depends(get_db)):
    paragraph = db.query(Paragraph).filter(Paragraph.id == paragraph_id).first()
    
    if not paragraph:
        print(f"Paragraph with ID {paragraph_id} not found.")  # Logs the issue
        raise HTTPException(status_code=404, detail=f"Paragraph {paragraph_id} not found")

    formatted_paragraph = format_to_paragraph_object(paragraph)
    
    
    return formatted_paragraph

# 3rd endpoint to be used
# add in student entry for student table. increment the modify paragraph using the id "used" value.
# add entry for student_modified_paragraph table. 
# takes a json and upload it to the students table in mysql. Look at schemas.py for proper json entries
@app.post("/students/")
def create_student(student: StudentSchema, db: Session = Depends(get_db)):
    # create student entry
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    # create student_modified_paragraph entry based on the two id from student
    link = StudentModifiedParagraph(
        student_id = db_student.id,
        modified_paragraph_id = db_student.modified_paragraph_id
    )
    db.add(link)
    # update the used value for the modified paragraph along with cr_avg
    modified = db.query(ModifiedParagraph).filter_by(id=student.modified_paragraph_id).first()
    if modified:
        modified.used += 1
        if modified.used == 1:
            modified.cr_avg = (db_student.cr1_result + db_student.cr2_result + db_student.cr3_result + db_student.cr4_result +
                            db_student.cr5_result + db_student.cr6_result + db_student.cr7_result + db_student.cr8_result) /8
        else:
            next_avg = (db_student.cr1_result + db_student.cr2_result + db_student.cr3_result + db_student.cr4_result +
                            db_student.cr5_result + db_student.cr6_result + db_student.cr7_result + db_student.cr8_result) /8
            modified.cr_avg = ((modified.cr_avg * (modified.used-1)) + next_avg) / modified.used
        db.add(modified)
    db.commit()
    db.refresh


@app.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# second endpoint to be used. store the modify paragraph entry
# takes a json and upload it to the modified_paragraphs table in mysql. Look at schemas.py for proper json entries
@app.post("/modified_paragraphs/")
def create_modified_paragraph(modified_paragraph: ModifiedParagraphSchema, db: Session = Depends(get_db)):
    db_modified_paragraph = ModifiedParagraph(**modified_paragraph.model_dump())
    db.add(db_modified_paragraph)
    db.commit()
    db.refresh(db_modified_paragraph)
    return db_modified_paragraph

@app.get("/modified_paragraphs/{modified_paragraph_id}")
def read_modified_paragraph(modified_paragraph_id: int, db: Session = Depends(get_db)):
    modified_paragraph = db.query(ModifiedParagraph).filter(ModifiedParagraph.id == modified_paragraph_id).first()
    if not modified_paragraph:
        raise HTTPException(status_code=404, detail="Modified Paragraph not found")
    return modified_paragraph

#########################################################################################
# helper function to work with @app.post("/link_student_modified_paragraphs/")
def link_student_and_paragraph(student_id: int, paragraph_id: int, db: Session):
    link = StudentModifiedParagraph(
        student_id=student_id,
        modified_paragraph_id=paragraph_id
    )
    db.add(link)
    db.commit()
    db.refresh(link)
    return link

# take a json and upload it to modified_paragraph_student table in mysql.
@app.post("/link_student_modified_paragraphs/")
def link_student_paragraph(link: StudentModifiedParagraphSchema, db: Session = Depends(get_db)):
    return link_student_and_paragraph(link.student_id, link.modified_paragraph_id, db)

#################################################################################################
